from langchain_core.tools import tool
from langchain_core.messages import HumanMessage


def make_generate_cover_letter_tool(llm):
    @tool
    def generate_cover_letter(job_description: str, cv_text: str) -> str:
        """Generate a tailored, professional cover letter for a job application.

        Args:
            job_description: Full text of the job posting.
            cv_text: Full text of the candidate's CV / resume.

        Returns:
            A complete cover letter (300-400 words) in business letter format.
        """
        prompt = (
            "Write a professional, tailored cover letter (300-400 words) for this role. "
            "Use formal business letter format. Start with 'Dear Hiring Manager,' and highlight "
            "the candidate's most relevant experience and genuine enthusiasm for the position.\n\n"
            f"--- JOB DESCRIPTION ---\n{job_description}\n\n"
            f"--- CV ---\n{cv_text}"
        )
        return llm.invoke([HumanMessage(content=prompt)]).content

    return generate_cover_letter
