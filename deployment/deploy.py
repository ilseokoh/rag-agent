import sys
import os

# Add the project root to sys.path so we can import company_qna
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp
import logging
from dotenv import set_key
from company_qna.agent import root_agent

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
AGENT_ENGINE_LOCATION = os.getenv("AGENT_ENGINE_LOCATION")
STAGING_BUCKET = os.getenv("STAGING_BUCKET")
# Define the path to the .env file relative to this script
ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))

vertexai.init(
    project=GOOGLE_CLOUD_PROJECT,
    location=AGENT_ENGINE_LOCATION,
    staging_bucket=STAGING_BUCKET,
)

# Function to update the .env file
def update_env_file(agent_engine_id, env_file_path):
    """Updates the .env file with the agent engine ID."""
    try:
        set_key(env_file_path, "AGENT_ENGINE_ID", agent_engine_id)
        print(f"Updated AGENT_ENGINE_ID in {env_file_path} to {agent_engine_id}")
    except Exception as e:
        print(f"Error updating .env file: {e}")

logger.info("deploying app...")
app = AdkApp(
    agent=root_agent,
    enable_tracing=True,
    display_name="Company QnA",
    description="HR, IT, IT System에 대한 질문에 답변해주는 Agent"
)

logging.debug("deploying agent to agent engine:")

remote_app = agent_engines.create(
    app,
    requirements=[
        "google-adk>=1.21.0",
        "python-dotenv",
        "google-auth>=2.45.0",
    ],
    extra_packages=[
        "./company_qna",
    ],
)

# log remote_app
logging.info(f"Deployed agent to Vertex AI Agent Engine successfully, resource name: {remote_app.resource_name}")

# Update the .env file with the new Agent Engine ID
update_env_file(remote_app.resource_name, ENV_FILE_PATH)