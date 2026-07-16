from langchain_core.tools import tool
from langchain_core.messages import HumanMessage


def make_analyze_skills_tool(llm):
    @tool
    def analyze_skills(job_description: str, cv_text: str) -> str:
        """Analyze a job description against a candidate CV to identify matching skills,
        missing skills, and a brief recommendation.

        Args:
            job_description: Full text of the job posting.
            cv_text: Full text of the candidate's CV / resume.

        Returns:
            Structured analysis with Matching Skills, Missing Skills, and Recommendation.
        """
        prompt = (
            "Analyze the job description against the candidate's CV and return:\n\n"
            "## Matching Skills\n- bullet list of skills the candidate already has\n\n"
            "## Missing / Gap Skills\n- bullet list of skills the candidate lacks\n\n"
            "## Recommendation\n1-2 sentence summary of overall fit.\n\n"
            f"--- JOB DESCRIPTION ---\n{job_description}\n\n"
            f"--- CV ---\n{cv_text}"
        )
        return llm.invoke([HumanMessage(content=prompt)]).content

    return analyze_skills
