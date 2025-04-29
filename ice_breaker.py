from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from output_parsers import summary_parser
from third_parties.linkedin import scrape_linkedin_profile

os.environ["NO_PROXY"] = "localhost,127.0.0.1"
load_dotenv()


def ice_break(linkedin_profile_url: str):
    print(f"🔍 Using LinkedIn profile URL: {linkedin_profile_url}")

    # גריסת פרופיל לינקדאין
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url,
        mock=False
    )

    print("🔍 Scraped LinkedIn data:", linkedin_data)

    if not linkedin_data:
        print("⚠️ Error: No data returned from LinkedIn scraping.")
        return None, ""

    summary_template = """
Given the information about a person from LinkedIn {information},
create:
1. A short professional summary about the person.
2. Two interesting and specific facts about them based on their LinkedIn information.

{format_instructions}
"""
    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(
        input={"information": linkedin_data}
    )

    print("🔍 Final summary:", res)

    return res, ""


if __name__ == "__main__":
    print("Ice Breaker Enter")
    linkedin_url = "https://www.linkedin.com/in/harrison-chase-789123456/"  # דוגמה
    summary, profile_pic_url = ice_break(linkedin_url)
    print(summary.to_dict())
