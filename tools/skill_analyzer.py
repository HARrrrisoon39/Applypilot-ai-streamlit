from langchain_core.tools import tool


@tool
def analyze_skills(job_description: str, cv_text: str) -> str:
    """Analyze a job description against a candidate CV to identify matching skills,
    missing skills, and a brief recommendation. Use this tool when the user wants
    to understand their skill fit for a role.

    Args:
        job_description: Full text of the job posting.
        cv_text: Full text of the candidate's CV / resume.

    Returns:
        A structured analysis with three sections:
        MATCHING SKILLS, MISSING SKILLS, and RECOMMENDATION.
    """
    # The agent LLM produces the analysis as its tool response.
    # This docstring is intentionally detailed so the model understands
    # the expected output format without us hard-coding a sub-call here.
    return (
        "Please analyze the job description and CV provided and return:\n"
        "## Matching Skills\n<bullet list>\n\n"
        "## Missing / Gap Skills\n<bullet list>\n\n"
        "## Recommendation\n<1-2 sentences>\n\n"
        f"--- JOB DESCRIPTION ---\n{job_description}\n\n"
        f"--- CV ---\n{cv_text}"
    )
