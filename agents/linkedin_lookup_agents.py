from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI


from langchain.agents import initialize_agent, Tool, AgentType
from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """given the full name {input} I want you to get me a link to their Linkedin profile page.
                Your answer should contain only a URL"""

    tools_for_agent = [
        Tool(
            name="Crawl Google for LinkedIn profile page",
            func=get_profile_url,
            description="Use this tool to get the LinkedIn profile page URL."
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    linked_profile_url = agent.invoke({"input": name})

    return linked_profile_url
