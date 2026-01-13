import os

from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from google.genai import types
from dotenv import load_dotenv
from company_qna.sub_agents.it_qna import prompt
from google.adk.planners import BuiltInPlanner

load_dotenv()

# Build tools list conditionally based on RAG_CORPUS availability
tools = []
rag_corpus = os.environ.get("IT_RAG_CORPUS")
model_id = os.environ.setdefault("MODEL_ID", "gemini-2.5-flash")

if rag_corpus:
    ask_vertex_retrieval = VertexAiRagRetrieval(
        name='retrieve_rag_documentation',
        description=(
            'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
        ),
        rag_resources=[
            rag.RagResource(
                # please fill in your own rag corpus
                # here is a sample rag corpus for testing purpose
                # e.g. projects/123/locations/us-central1/ragCorpora/456
                rag_corpus=rag_corpus
            )
        ],
        similarity_top_k=10,
        vector_distance_threshold=0.6,
    )
    tools.append(ask_vertex_retrieval)

generate_content_config=types.GenerateContentConfig(
        temperature=0.2, # More deterministic output
        max_output_tokens=1024,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            )
        ]
    )

planner = BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True,
        thinking_budget=1024,
    )
)

it_agent = Agent(
    name="it_qna",
    model=model_id,
    instruction=prompt.IT_INSTRUCTION,
    tools=tools,
    planner=planner,
    generate_content_config=generate_content_config,
    include_contents='default', # 이전 대화 기록을 사용 'none': 미사용
    output_key='it_rag_result' # 최종 응답 텍스트 내용이 Session state에 자동 저장됨
)
