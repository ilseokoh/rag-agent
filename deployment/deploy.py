# Google Cloud Docs: https://docs.cloud.google.com/agent-builder/agent-engine/deploy?hl=ko

import sys
import os

# Add the project root to sys.path so we can import company_qna
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import vertexai

from vertexai.preview.reasoning_engines import AdkApp
from dotenv import set_key
from company_qna.agent import root_agent

from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
AGENT_ENGINE_LOCATION = os.getenv("AGENT_ENGINE_LOCATION")
STAGING_BUCKET = os.getenv("STAGING_BUCKET")
RAG_CORPUS = os.getenv("RAG_CORPUS")
MODEL_ID = os.getenv("MODEL_ID")
# Define the path to the .env file relative to this script
ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))

DISPLAY_NAME= "company-qna"

# Function to update the .env file
def update_env_file(agent_engine_id, env_file_path):
    """Updates the .env file with the agent engine ID."""
    try:
        set_key(env_file_path, "AGENT_ENGINE_ID", agent_engine_id)
        print(f"Updated AGENT_ENGINE_ID in {env_file_path} to {agent_engine_id}")
    except Exception as e:
        print(f"Error updating .env file: {e}")

client = vertexai.Client(
    project=GOOGLE_CLOUD_PROJECT,
    location=AGENT_ENGINE_LOCATION,
)

def count_iterable(i):
    return sum(1 for e in i)

existed_agent = None
listed_agents = client.agent_engines.list(config={"filter": f'display_name={DISPLAY_NAME}',},)
for agent in listed_agents:
    existed_agent = agent
    break

if existed_agent: 
    print(f"Update agent engine:{agent.api_resource.name}")
    remote_agent = client.agent_engines.update(
        name=agent.api_resource.name,
        agent=root_agent,
        config = {
            "requirements": ["google-adk>=1.21.0",
                    "python-dotenv>=1.2.1",
                    "google-auth>=2.45.0",
                    "google-cloud-aiplatform>=1.132.0",
                    "cloudpickle>=3.1.2",
                    "pydantic>=2.12.5"
                ],
            "context_spec": {
                "memory_bank_config": {
                    "generation_config": {
                        "model": f"projects/{GOOGLE_CLOUD_PROJECT}/locations/global/publishers/google/models/gemini-2.5-flash"
                    }
                }
            },
            "extra_packages": ["./company_qna"],
            "display_name": DISPLAY_NAME,
            "description": "HR, IT, IT System에 대한 질문에 답변해주는 Agent",
            "min_instances": 0,
            "max_instances": 1,
            "resource_limits": {"cpu": "4", "memory": "8Gi"},
            "container_concurrency": 9,
            "agent_framework": "google-adk",
            "gcs_dir_name": "dev",
            "staging_bucket": STAGING_BUCKET,
            "env_vars": {
                "RAG_CORPUS": RAG_CORPUS,
                "MODEL_ID": MODEL_ID
            }
        }
    )
    print(f"Update agent to Vertex AI Agent Engine successfully, resource name: {remote_agent.api_resource.name}")


else:
    print(f"Deploying agent to agent engine: {GOOGLE_CLOUD_PROJECT} / {AGENT_ENGINE_LOCATION}")
    remote_agent = client.agent_engines.create(
        agent=root_agent,
        config = {
            "requirements": ["google-adk>=1.21.0",
                    "python-dotenv>=1.2.1",
                    "google-auth>=2.45.0",
                    "google-cloud-aiplatform>=1.132.0",
                    "cloudpickle>=3.1.2",
                    "pydantic>=2.12.5"
                ],
            "context_spec": {
                "memory_bank_config": {
                    "generation_config": {
                        "model": f"projects/{GOOGLE_CLOUD_PROJECT}/locations/global/publishers/google/models/gemini-2.5-flash"
                    }
                }
            },
            "extra_packages": ["./company_qna"],
            "display_name": DISPLAY_NAME,
            "description": "HR, IT, IT System에 대한 질문에 답변해주는 Agent",
            "min_instances": 0,
            "max_instances": 1,
            "resource_limits": {"cpu": "4", "memory": "8Gi"},
            "container_concurrency": 9,
            "agent_framework": "google-adk",
            "gcs_dir_name": "dev",
            "staging_bucket": STAGING_BUCKET,
            "env_vars": {
                "RAG_CORPUS": RAG_CORPUS,
                "MODEL_ID": MODEL_ID
            }
        }
    )
    # log remote_app
    print(f"Created agent to Vertex AI Agent Engine successfully, resource name: {remote_agent.api_resource.name}")

    # Update the .env file with the new Agent Engine ID
    update_env_file(remote_agent.api_resource.name, ENV_FILE_PATH)