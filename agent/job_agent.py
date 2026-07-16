from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools.skill_analyzer import make_analyze_skills_tool
from tools.cover_letter import make_generate_cover_letter_tool
from tools.interview_questions import make_create_interview_questions_tool

SYSTEM_PROMPT = """You are ApplyPilot, an expert AI career coach and job application assistant.

When given a job description and a candidate's CV, you MUST call ALL THREE tools in order:
1. analyze_skills    — identify matching and missing skills
2. generate_cover_letter — write a tailored cover letter
3. create_interview_questions — prepare interview questions

Always call all three tools and present their results clearly to the user.
Do not skip any tool. Be thorough, professional, and encouraging."""


def build_agent(llm) -> AgentExecutor:
    tools = [
        make_analyze_skills_tool(llm),
        make_generate_cover_letter_tool(llm),
        make_create_interview_questions_tool(llm),
    ]
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)
