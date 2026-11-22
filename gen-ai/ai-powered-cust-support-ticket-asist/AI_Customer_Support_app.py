"""
AI-Powered Customer Support Ticket Assistant (Streamlit app).
1. A support agent pastes a ticket, 
2. fine-tuned Qwen3-1.7B model predicts the type, queue, priority, and tags, and drafts a response. 
3. The agent reviews and edits the response, then approves it. The submission is saved to a local
ticket log (demo, no email is sent).

Run from the project folder:  streamlit run AI_Customer_Support_app.py
"""

import os
from datetime import datetime

import altair as alt
import pandas as pd
import streamlit as st

# Fully fine-tuned model
import AI_Customer_Support_Fine_Tuned_Model as tm

st.set_page_config(page_title="AI-Support Ticket Assistant", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.block-container, [data-testid="stMainBlockContainer"] {padding-top: 3.5rem;}
h1 {font-size: 2rem !important;}
textarea {font-size: 0.85rem !important;}
.st-key-version_line {margin-top: -1.2rem;}  /* pulls the version line closer to the line above */
</style>
""", unsafe_allow_html=True)

# Paths from project folder, folder of the .py files
TICKET_LOG_PATH = os.path.join(tm.BASE_DIR, "project_data", "ticket_log.csv")
TEST_SET_PATH = os.path.join(tm.BASE_DIR, "project_data", "test.csv")

# Technical help contact
TECH_CONTACT = "Rajesh Kumawat (app owner)"

# name of device the model runs
DEVICE_NAMES = {"mps": "Apple GPU (MPS)", "cuda": "NVIDIA GPU (CUDA)", "cpu": "CPU"}

# Column order oe ticket log
LOG_COLUMNS = ["ticket_id", "submitted_at", "subject", "body", "type", "queue", "priority",
               "tags", "final_response", "generation_seconds", "status", "edited_by_agent",
               "model_version"]


# Loading, cached, so it runs only once

@st.cache_resource
def get_model():
    # model stays in memory
    return tm.load_model()


@st.cache_data
def get_system_prompt():
    return tm.load_system_prompt()


@st.cache_data
def get_examples():
    # English and German test tickets for the demo
    test_df = pd.read_csv(TEST_SET_PATH, index_col="ticket_id")
    test_df["subject"] = test_df["subject"].fillna("")
    return test_df.groupby("language").sample(3, random_state=42)


def load_log():
    """Read ticket log, and add missing columns for tickets 
    and saved by an previous run.
    """
    if not os.path.exists(TICKET_LOG_PATH):
        return pd.DataFrame(columns=LOG_COLUMNS)
    log_df = pd.read_csv(TICKET_LOG_PATH)
    for column in LOG_COLUMNS:
        if column not in log_df.columns:
            log_df[column] = pd.NA
    log_df["status"] = log_df["status"].fillna("Open")
    return log_df[LOG_COLUMNS]


def save_log(log_df):
    log_df[LOG_COLUMNS].to_csv(TICKET_LOG_PATH, index=False)


# Stop with a clear message if model or the system prompt is missing
try:
    with st.spinner("Loading the fine-tuned model..."):
        model, tokenizer = get_model()
    system_prompt = get_system_prompt()
except OSError as error:
    st.error(f"Could not load the model or the system prompt: {error}")
    st.stop()

examples = get_examples()
example_labels = {
    f"#{ticket_id} ({row['language']}) {row['subject'][:60]}": ticket_id
    for ticket_id, row in examples.iterrows()
}


#  Session state, keeps values between clicks

defaults = {"subject": "", "body": "", "result": None, "raw_output": "", "seconds": 0.0,
            "response_edit": "", "true_labels": None, "submitted_id": None}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)


def load_example():
    """Fill the input fields with the selected test ticket."""
    choice = st.session_state["example_choice"]
    if choice == "None":
        return
    row = examples.loc[example_labels[choice]]
    st.session_state.update(
        subject=row["subject"], body=row["body"], result=None, submitted_id=None,
        true_labels={"type": row["type"], "queue": row["queue"], "priority": row["priority"]},
    )


def clear_ticket():
    """Reset the input fields and the results."""
    st.session_state.update(defaults)
    st.session_state["example_choice"] = "None"


#  Dialogs, pop-up windows

@st.dialog("About the model", width="large")
def show_about():
    st.markdown(f"""
**Model:** Qwen3-1.7B, fully fine-tuned (all 1.72 billion weights, no LoRA)

**Training data:** 2400 support tickets in English and German, balanced across 10 queues

**Training:** 3 epochs in 5.13 hours on an Apple GPU; the epoch 2 model was kept, because it had the lowest validation loss

**Main parameters:** learning rate 1e-5, effective batch size 8, Adafactor optimizer, maximum sequence length 2048, maximum output 512 tokens

**Test results (301 unseen tickets):**
- Type accuracy: 79.1%
- Queue accuracy: 29.6%
- Priority accuracy: 35.9%
- Valid JSON: 100%

**Version:** {tm.MODEL_VERSION} · **Last fine-tuned:** {tm.FINE_TUNED_DATE}
""")


@st.dialog("Help", width="large")
def show_help():
    st.markdown(f"""
**How to use:**
1. Paste the ticket subject (optional) and body (required), or load an example.
2. Click **Analyze ticket**.
3. Review the labels and **edit the draft response**.
4. Choose the status (Open or Closed), then click **Approve and submit** to save it to the ticket log.

**Tips:**
- Replace placeholders such as `<tel_num>` or `[Your Name]` before submitting.
- Check the queue and priority carefully, because they are less reliable.
- Generating a response takes about 6 seconds.
- **Cancel** discards the current ticket without saving it.
- The status of a submitted ticket can be changed in the **Submitted Tickets** tab.

**Technical help:** {TECH_CONTACT}
""")


@st.dialog("Responsible AI", width="large")
def show_responsible_ai():
    st.markdown("""
- **Human in the loop:** the model only drafts. An agent reviews, edits, and approves every response.
- **Privacy:** the model runs locally. Ticket text is not sent to any external service.
- **Limitations:** queue and priority predictions are less reliable. Responses can contain placeholders or general promises.
- **Hallucination:** the model may promise actions or details that the agent must verify.
- **Languages:** trained on English and German tickets only.
- **Transparency:** the system prompt and the raw model output are shown in the app.
- **Ticket log:** the local log contains ticket text, so it must be protected and not shared.
- **Demo:** submissions are saved locally. No email is sent.
""")

@st.dialog("System prompt", width="large")
def show_system_prompt():
    st.caption("The model was fine-tuned with exactly this prompt. The two examples in it are "
               "tickets from the training set of the public dataset, not customer data.")
    st.text(system_prompt)


# Header- title and dialog buttons 

col_title, col_buttons = st.columns([6, 3], vertical_alignment="center")
# Indigo robot icon to match the theme
col_title.title(":violet[:material/smart_toy:] AI-Powered Customer Support Ticket Assistant")
# col_title.title("🤖 AI-Powered Customer Support Ticket Assistant")

# three buttons side by side
with col_buttons.container(horizontal=True, horizontal_alignment="right", gap="small"):
    if st.button("About the model"):
        show_about()
    if st.button("Responsible AI"):
        show_responsible_ai()
    if st.button("Help"):
        show_help()

with st.container(horizontal=True, gap="small", vertical_alignment="center"):
    st.caption("Fine-tuned Qwen3-1.7B · English and German · drafts for human review ·", width="content")
    if st.button("System prompt", type="tertiary"):
        show_system_prompt()

with st.container(key="version_line"):
    st.caption(f"Model {tm.MODEL_VERSION} · fine-tuned on {tm.FINE_TUNED_DATE} · "
               f"🟢 Model loaded on {DEVICE_NAMES.get(tm.DEVICE, tm.DEVICE)}")

tab_analyze, tab_log, tab_analytics = st.tabs(["Analyze Ticket", "Submitted Tickets", "Analytics"])


# Analyze Ticket

with tab_analyze:

    # Ticket input
    st.subheader("1. New Ticket")
    st.selectbox("Load an example ticket from the test set (optional)",
                 ["None"] + list(example_labels), key="example_choice", on_change=load_example)
    st.text_input("Subject (optional)", key="subject")
    st.text_area("Body (required)", key="body", height=180)

    analyze_clicked = st.button("Analyze ticket", type="primary")

    if analyze_clicked:
        if not st.session_state["body"].strip():
            st.warning("Please enter the ticket body. The subject is optional.")
        else:
            # Shows each step while the AI assistant works on the ticket
            with st.status("The AI assistant is working on the ticket...", expanded=True) as status_box:
                st.write("Reading the ticket...")
                st.write("Classifying the ticket and drafting the response...")
                text, seconds = tm.generate(model, tokenizer, system_prompt,
                                            st.session_state["subject"], st.session_state["body"])
                st.write("Checking the output...")
                result = tm.parse_json(text)
                status_box.update(label=f"Done in {seconds:.1f} seconds", state="complete", expanded=False)
            st.session_state.update(raw_output=text, result=result, seconds=seconds,
                                    response_edit=str(result.get("response", "")), submitted_id=None)

    # Prediction and draft response
    result = st.session_state["result"]
    if result is not None:
        st.subheader("2. 🤖 AI Prediction")
        st.caption(f"Generated in {st.session_state['seconds']:.1f} seconds")

        if not result:
            st.error("The model output is not valid JSON. See the raw model output below.")
        else:
            col_type, col_queue, col_priority = st.columns(3)
            col_type.markdown(f"**Type**  \n{result.get('type', '-')}")
            col_queue.markdown(f"**Queue**  \n{result.get('queue', '-')}")
            col_priority.markdown(f"**Priority**  \n{result.get('priority', '-')}")

            tags = result.get("tags", [])
            if isinstance(tags, list) and tags:
                st.markdown("**Tags:** " + " · ".join(f"`{tag}`" for tag in tags))

            # Output validation
            label_warnings = tm.check_labels(result)
            if label_warnings:
                for warning in label_warnings:
                    st.warning(warning)
            else:
                st.success("Valid JSON · all labels are allowed values")

            # True labels, only for example tickets from the test set
            true_labels = st.session_state["true_labels"]
            if true_labels:
                st.info(f"True labels (test set): {true_labels['type']} · "
                        f"{true_labels['queue']} · {true_labels['priority']}")

            st.subheader("3. ✨ AI Draft Response (edit before submitting)")
            st.text_area("Response", key="response_edit", height=200, label_visibility="collapsed")

            placeholders = tm.find_placeholders(st.session_state["response_edit"])
            if placeholders:
                st.warning("Replace these placeholders before submitting: " + ", ".join(placeholders))

            # Status of ticket, can be changed later in the Submitted Tickets tab
            status = st.radio("Status", ["Open", "Closed"], horizontal=True)

            col_submit, col_cancel, col_download, _ = st.columns([1.2, 0.8, 1.2, 3])
            submit_clicked = col_submit.button("Approve and submit", type="primary",
                                               disabled=st.session_state["submitted_id"] is not None)
            # Cancel- clears the input, the prediction, and the draft
            col_cancel.button("Cancel", on_click=clear_ticket)
            col_download.download_button("Download response", st.session_state["response_edit"],
                                         file_name="response.txt")

            if submit_clicked:
                if not st.session_state["response_edit"].strip():
                    st.warning("The response is empty.")
                else:
                    log_df = load_log()
                    ticket_id = f"TCK-{len(log_df) + 1:04d}"

                    new_entry = pd.DataFrame([{
                        "ticket_id": ticket_id,
                        "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "subject": st.session_state["subject"],
                        "body": st.session_state["body"],
                        "type": result.get("type", ""),
                        "queue": result.get("queue", ""),
                        "priority": result.get("priority", ""),
                        "tags": ", ".join(tags) if isinstance(tags, list) else "",
                        "final_response": st.session_state["response_edit"],
                        "generation_seconds": round(st.session_state["seconds"], 2),
                        "status": status,
                        # Shows if agent changed the model draft
                        "edited_by_agent": st.session_state["response_edit"] != str(result.get("response", "")),
                        "model_version": tm.MODEL_VERSION,
                    }])
                    save_log(pd.concat([log_df, new_entry]))
                    st.session_state["submitted_id"] = ticket_id
                    st.rerun()

            if st.session_state["submitted_id"]:
                st.success(f"Ticket {st.session_state['submitted_id']} saved to the local ticket log "
                           f"(demo, no email is sent).")

        with st.expander("Raw model output (JSON)"):
            st.code(st.session_state["raw_output"], language="json")


# Submitted Tickets

with tab_log:
    st.subheader("Submitted Tickets")
    log_df = load_log()
    if log_df.empty:
        st.info("No tickets submitted yet.")
    else:
        st.caption("Only the status can be changed. Click **Save changes** to keep it.")
        edited_log = st.data_editor(
            log_df,
            hide_index=True,
            # Status as a dropdown, all other columns read-only
            column_config={"status": st.column_config.SelectboxColumn("status", options=["Open", "Closed"], required=True)},
            disabled=[column for column in LOG_COLUMNS if column != "status"],
        )
        col_save, col_csv, _ = st.columns([1, 1.5, 3])
        if col_save.button("Save changes"):
            save_log(edited_log)
            st.success("Status changes saved.")
        col_csv.download_button("Download ticket log (CSV)", edited_log.to_csv(index=False),
                                file_name="ticket_log.csv")


# Analytics

with tab_analytics:
    st.subheader("Analytics")
    log_df = load_log()
    if log_df.empty:
        st.info("No tickets submitted yet.")
    else:
        # Summary numbers
        times = pd.to_numeric(log_df["generation_seconds"], errors="coerce")
        edited = log_df["edited_by_agent"].astype(str).str.lower() == "true"
        open_count = (log_df["status"] == "Open").sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Tickets processed", len(log_df))
        col2.metric("Average generation time", f"{times.mean():.1f} s" if times.notna().any() else "-")
        col3.metric("Responses edited by agent", f"{edited.mean() * 100:.0f}%")
        col4.metric("Open / Closed", f"{open_count} / {len(log_df) - open_count}")

        # Tickets per day, dates as YYYY/MM/DD
        st.markdown("**Tickets processed per day**")
        per_day = (pd.to_datetime(log_df["submitted_at"]).dt.strftime("%Y/%m/%d")
                   .value_counts().sort_index().rename_axis("Date").reset_index(name="Tickets"))

        # Altair chart - horizontal dates
        chart = alt.Chart(per_day).mark_bar(size=40, color="#4F46E5").encode(
            x=alt.X("Date:N", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Tickets:Q", axis=alt.Axis(tickMinStep=1)),
        )
        st.altair_chart(chart)