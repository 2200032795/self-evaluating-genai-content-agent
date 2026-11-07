import streamlit as st
import json
import sqlite3
from pathlib import Path

from agent import run_content_agent
from memory import get_previous_feedback


st.set_page_config(
    page_title="GenAI Content Agent",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Self-Evaluating GenAI Content Agent")

st.write(
    "An AI-powered lesson generator that evaluates content, "
    "rejects errors, regenerates lessons, and remembers feedback."
)

st.divider()

topic = st.text_input(
    "Enter your lesson topic",
    value="Introduction to RAG"
)

live_tab, demo_tab, memory_tab = st.tabs([
    "Live AI Generation",
    "Offline Demonstration",
    "Persistent Memory"
])


# --------------------------------------------------
# TAB 1: LIVE AI GENERATION
# --------------------------------------------------

with live_tab:

    st.subheader("Generate a New Lesson")

    if st.button("Generate and Evaluate Lesson", type="primary"):

        if not topic.strip():
            st.warning("Please enter a topic.")

        else:

            with st.spinner("Generating and evaluating lesson..."):

                try:
                    result = run_content_agent(
                        topic.strip(),
                        demo_mode=False
                    )

                    if result is None:
                        st.error("Lesson generation was interrupted.")

                    elif result.get("status") == "EVALUATION_INTERRUPTED":
                        st.warning(
                            "Evaluation was interrupted. "
                            "The lesson has not been approved."
                        )

                    else:
                        st.success(
                            f"Final Status: {result['status']}"
                        )

                        evaluation = result["evaluation"]

                        st.subheader("Evaluation Summary")

                        col1, col2 = st.columns(2)

                        col1.metric(
                            "Overall Status",
                            evaluation["overall_status"]
                        )

                        col2.metric(
                            "Rejected Attempts",
                            len(result["rejection_log"])
                        )

                        st.subheader("Seven Evaluation Criteria")

                        for criterion, details in evaluation["checks"].items():

                            message = (
                                f"{criterion.replace('_', ' ').title()}: "
                                f"{details['status']} — {details['reason']}"
                            )

                            if details["status"] == "PASS":
                                st.success(message)
                            else:
                                st.error(message)

                        if evaluation["overall_status"] == "PASS":

                            st.subheader("Approved Lesson")
                            st.markdown(result["lesson"])

                            st.download_button(
                                "Download Approved Lesson",
                                result["lesson"],
                                file_name="final_lesson.md"
                            )

                        st.subheader("Rejection Log")
                        st.json(result["rejection_log"])

                except Exception as error:
                    st.error(f"Application error: {error}")


# --------------------------------------------------
# TAB 2: OFFLINE DEMONSTRATION
# --------------------------------------------------

with demo_tab:

    st.subheader("Offline Demonstration")

    st.info(
        "This section uses saved project results and does not "
        "make new Gemini API requests."
    )

    if st.button("Load Previously Approved Demonstration"):

        lesson_path = Path("outputs/final_lesson.md")
        evaluation_path = Path("outputs/evaluation.json")
        rejection_path = Path("outputs/rejection_log.json")

        if lesson_path.exists() and evaluation_path.exists():

            lesson = lesson_path.read_text(encoding="utf-8")

            with evaluation_path.open(
                "r",
                encoding="utf-8"
            ) as file:
                evaluation = json.load(file)

            st.session_state["demo_lesson"] = lesson
            st.session_state["demo_evaluation"] = evaluation

            if rejection_path.exists():
                st.session_state["demo_rejection"] = json.loads(
                    rejection_path.read_text(encoding="utf-8")
                )

        else:
            st.error("Saved lesson or evaluation file is missing.")

    if "demo_lesson" in st.session_state:

        st.subheader("Previously Saved Evaluation")

        evaluation = st.session_state["demo_evaluation"]

        st.metric(
            "Overall Status",
            evaluation["overall_status"]
        )

        for criterion, details in evaluation["checks"].items():

            message = (
                f"{criterion.replace('_', ' ').title()}: "
                f"{details['status']} — {details['reason']}"
            )

            if details["status"] == "PASS":
                st.success(message)
            else:
                st.error(message)

        st.subheader("Previously Approved Lesson")
        st.markdown(st.session_state["demo_lesson"])

        st.download_button(
            "Download Lesson",
            st.session_state["demo_lesson"],
            file_name="final_lesson.md"
        )

        st.subheader("Previous Rejection Log")

        st.json(st.session_state.get("demo_rejection", []))


# --------------------------------------------------
# TAB 3: PERSISTENT MEMORY
# --------------------------------------------------

with memory_tab:

    st.subheader("Agent Learning Memory")

    st.write(
        "The agent stores previous failures and retrieves "
        "them to guide future lesson generation."
    )

    if st.button("Retrieve Previous Learning"):

        feedback = get_previous_feedback(topic.strip())

        if feedback:

            st.success("Previous failure memory retrieved!")

            st.code(feedback)

        else:

            st.info("No previous failure records found for this topic.")

    st.subheader("Run History")

    database_path = Path("data/agent_memory.db")

    if database_path.exists():

        connection = sqlite3.connect(database_path)

        history = connection.execute("""
            SELECT topic, final_status, total_attempts, created_at
            FROM run_history
            ORDER BY id DESC
        """).fetchall()

        connection.close()

        if history:

            st.table([
                {
                    "Topic": row[0],
                    "Final Status": row[1],
                    "Attempts": row[2],
                    "Date": row[3]
                }
                for row in history
            ])

        else:
            st.info("No run history available yet.")

    else:
        st.info("Memory database has not been created yet.")


st.divider()

st.caption(
    "Powered by Google Gemini | Python | Streamlit | SQLite"
)
