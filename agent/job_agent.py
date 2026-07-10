from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools.skill_analyzer import analyze_skills
from tools.cover_letter import generate_cover_letter
from tools.interview_questions import create_interview_questions

SYSTEM_PROMPT = """You are ApplyPilot, an expert AI career coach and job application assistant.

When given a job description and a candidate's CV, you MUST call ALL THREE tools in order:
1. analyze_skills    — identify matching and missing skills
2. generate_cover_letter — write a tailored cover letter
3. create_interview_questions — prepare interview questions

Always call all three tools and present their results clearly to the user.
Do not skip any tool. Be thorough, professional, and encouraging."""

_TOOLS = [analyze_skills, generate_cover_letter, create_interview_questions]


def build_agent(llm) -> AgentExecutor:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_tool_calling_agent(llm, _TOOLS, prompt)
    return AgentExecutor(agent=agent, tools=_TOOLS, verbose=True, max_iterations=10)
