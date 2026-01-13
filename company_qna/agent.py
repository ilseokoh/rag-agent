import os

from google.adk.agents import Agent

from dotenv import load_dotenv
from company_qna import prompt
from company_qna.sub_agents.hr_qna import hr_agent
from company_qna.sub_agents.it_qna import it_agent

load_dotenv()

model_id = os.environ.setdefault("MODEL_ID", "gemini-2.5-flash")


root_agent = Agent(
    name="company_qna_agent",
    description="",
    model=model_id,
    instruction=prompt.COMPANY_QNA_INSTRUCTION,
    sub_agents=[
        hr_agent,
        it_agent
    ]
)
