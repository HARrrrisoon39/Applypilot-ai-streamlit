from langchain_core.tools import tool
from langchain_core.messages import HumanMessage


def make_create_interview_questions_tool(llm):
    @tool
    def create_interview_questions(job_description: str, cv_text: str) -> str:
        """Create likely interview questions with answer hints based on the role and candidate background.

        Args:
            job_description: Full text of the job posting.
            cv_text: Full text of the candidate's CV / resume.

        Returns:
            10 numbered interview questions each with a one-sentence answer hint.
        """
        prompt = (
            "Generate 10 interview questions for this role and candidate. Include:\n"
            "- 3 technical questions specific to the role's required skills\n"
            "- 4 behavioural (STAR-format) questions\n"
            "- 3 questions probing the candidate's identified skill gaps\n\n"
            "For each question, add a one-sentence answer hint that references something "
            "specific from the CV.\n\n"
            "Format as a numbered list: **Q1. [Question]** — *Hint: ...*\n\n"
            f"--- JOB DESCRIPTION ---\n{job_description}\n\n"
            f"--- CV ---\n{cv_text}"
        )
        return llm.invoke([HumanMessage(content=prompt)]).content

    return create_interview_questions
