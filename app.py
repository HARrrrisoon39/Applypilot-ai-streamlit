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

# ── Session state defaults ────────────────────────────────────────────────────
if "cv_text" not in st.session_state:
    st.session_state.cv_text = ""
if "results" not in st.session_state:
    st.session_state.results = None

# ── Sidebar: CV upload ────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📄 Your CV")
    uploaded = st.file_uploader("Upload your CV (PDF)", type=["pdf"])
    if uploaded:
        st.session_state.cv_text = extract_pdf_text(uploaded.read())
        st.success("CV loaded ✓")
        with st.expander("Preview extracted text"):
            st.text(st.session_state.cv_text[:2000] + ("…" if len(st.session_state.cv_text) > 2000 else ""))

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

if analyze_clicked:
    if not st.session_state.cv_text:
        st.warning("Please upload your CV in the sidebar first.")
    elif not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        with st.spinner("ApplyPilot is working… (this may take 30–60 seconds)"):
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
                response = agent.invoke({"input": prompt, "chat_history": []})
                st.session_state.results = response["output"]
            except Exception as exc:
                st.error(f"Agent error: {exc}")

# ── Display results ───────────────────────────────────────────────────────────
if st.session_state.results:
    output: str = st.session_state.results

    # Try to split the output into three sections heuristically
    def _extract_section(text: str, markers: list[str]) -> str:
        for marker in markers:
            idx = text.lower().find(marker.lower())
            if idx != -1:
                return text[idx:]
        return text

    skills_section = _extract_section(
        output, ["## matching skills", "matching skills", "skill analysis", "skills"]
    )
    cover_section = _extract_section(
        output, ["## cover letter", "cover letter", "dear hiring"]
    )
    interview_section = _extract_section(
        output, ["## interview", "interview questions", "1."]
    )

    with st.expander("🎯 Skills Analysis", expanded=True):
        # Show the full output if we can't cleanly separate sections
        if cover_section == output and interview_section == output:
            st.markdown(output)
        else:
            end = min(
                len(output),
                output.lower().find("cover letter") if "cover letter" in output.lower() else len(output),
            )
            st.markdown(output[:end] if end < len(output) else output)

    with st.expander("✉️ Cover Letter", expanded=True):
        cl_start = output.lower().find("cover letter")
        cl_end = output.lower().find("interview")
        if cl_start != -1:
            snippet = output[cl_start: cl_end if cl_end > cl_start else len(output)]
            st.markdown(snippet)
            # Store for save form
            st.session_state["_cover_letter"] = snippet
        else:
            st.info("Cover letter section not distinctly separated — see full output below.")

    with st.expander("🎤 Interview Questions", expanded=True):
        iq_start = output.lower().find("interview")
        if iq_start != -1:
            st.markdown(output[iq_start:])
        else:
            st.info("Interview questions section not distinctly separated — see full output below.")

    with st.expander("📋 Full Agent Output"):
        st.markdown(output)

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
                    "cover_letter": st.session_state.get("_cover_letter", output),
                }
            )
            st.success(f"Saved **{job_title}** at **{company}** ✓")
