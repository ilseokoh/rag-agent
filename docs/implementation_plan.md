# Implementation Plan: Company QnA Agent with ADK

## 1. Project Initialization & Dependencies
- Initialize a new `uv` project.
- Add `google-adk` dependency.

```bash
uv init .
uv add google-adk
```

## 2. Environment Configuration
- Create a `.env` file to store sensitive and environment-specific variables.
- **Required Variables**:
    - `RAG_CORPUS`: Vertex AI RAG Engine corpus name (format: `projects/{project}/locations/{location}/ragCorpora/{corpus}`).
    - `GOOGLE_CLOUD_PROJECT`: Google Cloud Project ID.
    - `GOOGLE_CLOUD_LOCATION`: Google Cloud Location (e.g., `us-central1`).

## 3. Directory Structure
We will use a modular structure as requested:

```
rag-agent/
├── .env                  # Environment variables
├── pyproject.toml        # Managed by uv
├── .python-version
├── company_qna/          # Main Agent Code
│   ├── __init__.py
│   └── agent.py          # Agent definition and configuration
├── deployment/           # Agent Engine deployment configurations
└── eval/                 # Agent Evaluation scripts/configs
```

## 4. Agent Implementation (`company_qna/agent.py`)
- **Imports**:
    - `os` (to read environment variables)
    - `google.adk.agents.LlmAgent`
    - `google.adk.tools.vertex_ai_rag_retrieval`
- **Logic**:
    1.  Load environment variables (`RAG_CORPUS`, etc.).
    2.  Configure the `vertex_ai_rag_retrieval` tool. It likely needs the `rag_corpus` resource name passed to it.
    3.  Define the `LlmAgent`:
        -   **Name**: `company_qna_agent`
        -   **Model**: `gemini-3.0-flash-preview`
        -   **Tools**: `[vertex_ai_rag_retrieval]`
        -   **Instructions**: "You are a helpful QnA assistant for HR and IT. Use the provided RAG tool to answer questions based on the retrieved context."

## 5. Testing
- Use the ADK Web UI for interactive testing.
- Command:
  ```bash
  uv run adk web company_qna/agent.py:company_qna_agent
  ```
  