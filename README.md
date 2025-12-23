# rag-agent
An Agent using Vertex RAG Engine 

## Setup 

### Get ADK Python Docs 

```bash
curl -o llms-full.txt https://raw.githubusercontent.com/google/adk-python/main/llms-full.txt
```

### Gemini CLI Auth 

```
export GOOGLE_CLOUD_PROJECT=
export GOOGLE_CLOUD_LOCATION=global
```

## Gemini CLI prompts

### Plan for Agent

```
I want to build an company QnA agent for HR, IT and IT system using ADK. The agent should be able to:
- Retreive the relavant information from Vertex AI RAG Engine. The tool name of ADK is vertex_ai_rag_retrieval.
- For the agent model, always use gemini-3.0-flash-preview 

This plan should follow ADK best practices, incluing:
- All necessary imports
- Use the .env file to set the environment variable. 
- Set the environment variables. 
    - RAG_CORPUS: Vertex AI RAG Engine corpus name which starts with projects.
    - GOOGLE_CLOUD_PROJECT
    - GOOGLE_CLOUD_LOCATION
- folder structure
    - deployment: for Agent Engine deployment
    - eval: for the Agent Evaluation
    - company_qna : the Agent folder
- It should create an ADK agent that can be run using adk web for testing.
- Use uv for package management, create a new uv project, and add all the relevant dependencies
- Tool functions with proper type hints and docstrings
- Agent configuration with tools
Create a simple implementation plan using Python ADK. any code yet, just create the plan. @docs/llms-full.txt
```

### Proceed the implementation 

```
Great! Proceed the implementation with the plan @docs/implementation_plan.md

@docs/llms-full.txt
```

## Deploying the Agent

다음 명령어를 사용하여 에이전트를 Vertex AI 에이전트 엔진에 배포할 수 있습니다.
```bash
uv run python deployment/deploy.py
```
에이전트 배포 후 다음과 같은 INFO 로그 메시지가 표시됩니다.
```
Deployed agent to Vertex AI Agent Engine successfully, resource name: projects/<PROJECT_NUMBER>/locations/us-central1/reasoningEngines/<AGENT_ENGINE_ID>
```

원격 에이전트 테스트에 필수적인 에이전트 엔진 리소스 이름을 기록해 두고 `.env` 파일을 업데이트하십시오.