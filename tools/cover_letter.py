from langchain_core.tools import tool


@tool
def generate_cover_letter(job_description: str, cv_text: str) -> str:
    """Generate a tailored, professional cover letter for a job application
    based on the job description and candidate's CV. Use this tool when the
    user needs a cover letter drafted.

    Args:
        job_description: Full text of the job posting.
        cv_text: Full text of the candidate's CV / resume.

    Returns:
        A complete, ready-to-send cover letter (300-400 words).
    """
    return (
        "Please write a professional, tailored cover letter (300-400 words) "
        "highlighting the candidate's relevant experience and enthusiasm for the role. "
        "Use a formal business letter format.\n\n"
        f"--- JOB DESCRIPTION ---\n{job_description}\n\n"
        f"--- CV ---\n{cv_text}"
    )
