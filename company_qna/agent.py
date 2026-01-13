import os

from google.adk.agents import Agent

from dotenv import load_dotenv
from company_qna import prompts
from company_qna.sub_agents.hr_qna.agent import hr_agent
from company_qna.sub_agents.it_qna.agent import it_agent

load_dotenv()

model_id = os.environ.setdefault("MODEL_ID", "gemini-2.5-flash")


root_agent = Agent(
    name="company_qna_agent",
    description="인사(HR) 또는 IT 관련 질문에 답변하는 에이전트",
    model=model_id,
    instruction=prompts.COMPANY_QNA_INSTRUCTION,
    sub_agents=[
        hr_agent,
        it_agent
    ]
)
# 유연근무제도에 대해서 설명해줘