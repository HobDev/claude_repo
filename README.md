# Claude API Learning Repo
Python 3.14+ project with examples for Claude chat, MCP tool-calling, RAG, and prompt evaluation.
Setup: create venv and install deps with `python -m venv .venv && source .venv/bin/activate && pip install -e .`.
Create `.env` in the repo root (or copy `src/.env.example`) and add required secrets.
Required: `ANTHROPIC_API_KEY`, `CLAUDE_MODEL` (for Anthropic requests and MCP chat).
Required for RAG embeddings: `VOYAGE_API_KEY`.
Run MCP CLI chat: `cd src/mcp && python main.py` (set `USE_UV=1` to launch MCP servers with uv).
Code features: Claude request wrappers (`src/api_request.py`, `src/conversation.py`), tool schemas (`src/tool_use/`), code-execution/files API demo (`src/code_execution_and_files_api/`).
Data features: chunking + vector/BM25 retrieval + orchestration (`src/rag/`), and prompt dataset/evaluation/report scripts (`src/prompt_evaluation/`).
