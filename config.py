import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "applypilot.db"

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o", temperature=0)

    # Default: Anthropic
    from langchain_anthropic import ChatAnthropic
    return ChatAnthropic(model="claude-opus-4-5", temperature=0)
