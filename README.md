# Nexia Multi-Agent Academic Assistant

Nexia is an agentic AI academic assistant for attendance, marks, fees, mentor alerts, notifications, and voice-based student queries.

## Agentic AI Alignment

- Coordinator Agent routes every user query to the correct specialized agent.
- Attendance, Academic, Fee, Mentor, Notification, and Voice agents handle domain tasks.
- MongoDB provides database context, Flask provides API access, and project docs/manifests provide file-system context.
- `backend/mcp_manifest.json` documents an MCP-style interface for tools and resources.
- `backend/services/agent_registry.py` is the adapter point for LangChain, CrewAI, AutoGen, RAG, and n8n workflows.

## Run Locally

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Start MongoDB locally and seed the database if needed:

```bash
python database/seed_db.py
```

4. Start the Flask backend:

```bash
cd backend
python app.py
```

5. Open `frontend/index.html` in a browser.

## Useful Endpoints

- `GET /` - backend health message
- `GET /voice-query?q=show my attendance` - coordinator-driven query
- `GET /agent-capabilities` - agent registry and integration overview
- `GET /check-attendance` - scheduled attendance agent action
- `GET /mentor/<mentor_id>/students` - mentor dashboard data

## Version Control

The repository ignores virtual environments, caches, local env files, build outputs, and logs. Commit source files, docs, schemas, and configuration examples.
