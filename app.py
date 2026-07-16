import os
import threading
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from config import get_llm
from db.database import init_db, save_application
from tools.pdf_extractor import extract_pdf_text
from agent.job_agent import build_agent

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ApplyPilot AI",
    page_icon="🚀",
    layout="wide",
)

init_db()

# ── API key guard ─────────────────────────────────────────────────────────────
provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
_key_var = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
if not os.getenv(_key_var):
    st.error(
        f"**{_key_var} is not set.** Create a `.env` file in the project root with "
        f"`{_key_var}=your-key-here` and restart the app."
    )
    st.stop()

# ── Session state defaults ────────────────────────────────────────────────────
for key, default in [
    ("cv_text", ""),
    ("cv_filename", ""),
    ("results", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar: CV upload ────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📄 Your CV")
    uploaded = st.file_uploader("Upload your CV (PDF)", type=["pdf"])
    if uploaded and uploaded.name != st.session_state.cv_filename:
        try:
            text = extract_pdf_text(uploaded.read())
            if not text.strip():
                st.warning("No text could be extracted from this PDF. It may be image-based.")
            else:
                st.session_state.cv_text = text
                st.session_state.cv_filename = uploaded.name
                st.success(f"CV loaded: {uploaded.name} ✓")
        except Exception as exc:
            st.error(f"Failed to read PDF: {exc}")

    if st.session_state.cv_text:
        st.caption(f"Loaded: **{st.session_state.cv_filename}**")
        with st.expander("Preview extracted text"):
            preview = st.session_state.cv_text
            st.text(preview[:2000] + ("…" if len(preview) > 2000 else ""))
        if st.button("Clear CV", use_container_width=True):
            st.session_state.cv_text = ""
            st.session_state.cv_filename = ""
            st.rerun()

    st.divider()
    st.caption("Navigate to **My Applications** to track your saved jobs.")

# ── Main area ─────────────────────────────────────────────────────────────────
st.title("🚀 ApplyPilot AI")
st.subheader("Your intelligent job application assistant")

job_description = st.text_area(
    "Paste the job description here",
    height=300,
    placeholder="Copy & paste the full job posting…",
)

analyze_clicked = st.button("✨ Analyze & Generate", type="primary", use_container_width=True)

AGENT_TIMEOUT = 120  # seconds

if analyze_clicked:
    if not st.session_state.cv_text:
        st.warning("Please upload your CV in the sidebar first.")
    elif not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        with st.spinner("ApplyPilot is working… (this may take up to 2 minutes)"):
            result_container = {}
            error_container = {}

            def _run_agent():
                try:
                    llm = get_llm()
                    agent = build_agent(llm)
                    prompt = (
                        "Here is the job description and the candidate's CV.\n\n"
                        f"JOB DESCRIPTION:\n{job_description}\n\n"
                        f"CV:\n{st.session_state.cv_text}\n\n"
                        "Please use all three tools (analyze_skills, generate_cover_letter, "
                        "create_interview_questions) and return the results."
                    )
                    result_container["response"] = agent.invoke(
                        {"input": prompt, "chat_history": []},
                        return_intermediate_steps=True,
                    )
                except Exception as exc:
                    error_container["error"] = exc

            t = threading.Thread(target=_run_agent)
            t.start()
            t.join(timeout=AGENT_TIMEOUT)

            if t.is_alive():
                st.error("The agent timed out after 2 minutes. Please try again.")
            elif "error" in error_container:
                st.error(f"Agent error: {error_container['error']}")
            else:
                response = result_container["response"]
                # Extract tool outputs from intermediate steps keyed by tool name
                tool_outputs = {}
                for action, observation in response.get("intermediate_steps", []):
                    tool_outputs[action.tool] = observation

                st.session_state.results = {
                    "skills": tool_outputs.get("analyze_skills", ""),
                    "cover_letter": tool_outputs.get("generate_cover_letter", ""),
                    "interview": tool_outputs.get("create_interview_questions", ""),
                    "full_output": response["output"],
                }

# ── Display results ───────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results

    with st.expander("🎯 Skills Analysis", expanded=True):
        st.markdown(r["skills"] or r["full_output"])

    with st.expander("✉️ Cover Letter", expanded=True):
        st.markdown(r["cover_letter"] or "*Cover letter not found in tool outputs — see full output below.*")

    with st.expander("🎤 Interview Questions", expanded=True):
        st.markdown(r["interview"] or "*Interview questions not found in tool outputs — see full output below.*")

    with st.expander("📋 Full Agent Output"):
        st.markdown(r["full_output"])

    # ── Save application form ─────────────────────────────────────────────────
    st.divider()
    st.subheader("💾 Save This Application")
    with st.form("save_form"):
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Job Title *")
            company = st.text_input("Company *")
        with col2:
            job_url = st.text_input("Job URL")
            deadline = st.date_input("Application Deadline")

        status = st.selectbox(
            "Status",
            ["applied", "interview", "offer", "rejected", "saved"],
        )
        save_clicked = st.form_submit_button("Save Application", type="primary")

    if save_clicked:
        if not job_title or not company:
            st.warning("Job title and company are required.")
        else:
            save_application(
                {
                    "job_title": job_title,
                    "company": company,
                    "job_url": job_url,
                    "deadline": str(deadline),
                    "status": status,
                    "skills_analysis": r["skills"],
                    "cover_letter": r["cover_letter"],
                    "interview_questions": r["interview"],
                }
            )
            st.success(f"Saved **{job_title}** at **{company}** ✓")
