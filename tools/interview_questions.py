from langchain_core.tools import tool


@tool
def create_interview_questions(job_description: str, cv_text: str) -> str:
    """Create a list of likely interview questions (with ideal answer hints) based
    on the job description and the candidate's background. Use this tool when the
    user wants to prepare for an interview.

    Args:
        job_description: Full text of the job posting.
        cv_text: Full text of the candidate's CV / resume.

    Returns:
        10 interview questions, each with a brief answer hint tailored to the
        candidate's background.
    """
    return (
        "Please generate 10 interview questions likely to be asked for this role, "
        "including 3 technical questions, 4 behavioural (STAR) questions, and "
        "3 questions about the candidate's specific experience gaps. "
        "For each question, add a 1-sentence answer hint referencing the CV.\n\n"
        f"--- JOB DESCRIPTION ---\n{job_description}\n\n"
        f"--- CV ---\n{cv_text}"
    )
