# Nexia Multi-Agent Academic Assistant

Nexia is an agentic AI academic assistant for attendance, marks, fees, mentor alerts, notifications, and voice-based student queries.

## Agentic AI Alignment

- Coordinator Agent routes every user query to the correct specialized agent.
- Attendance, Academic, Fee, Mentor, Notification, and Voice Agents handle domain tasks.
- MongoDB provides database context, Flask provides API access, and project docs/manifests provide file-system context.
- `backend/mcp_manifest.json` documents an MCP-style interface for tools and resources.
- `backend/services/agent_registry.py` is the adapter point for LangChain, CrewAI, AutoGen, RAG, and n8n workflows.
- `backend/services/llm_coordinator.py` adds an optional LLM Planner Agent with Groq or OpenAI.

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

5. Open `frontend/index.html` in a browser. The frontend is now a React-based static app that calls the Flask API.

## Optional LLM Agent Mode

The app works without an API key using the rule-based coordinator. To enable the LLM-powered autonomous planner with Groq, add this to `.env`:

```bash
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile
GROQ_API_KEY=your_groq_api_key_here
```

OpenAI is also supported:

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

When enabled, the Coordinator Agent asks the LLM Planner Agent to choose the best tool, executes that tool, then asks the LLM to summarize the tool result for the student.

## Useful Endpoints

- `GET /` - backend health message
- `GET /voice-query?q=show my attendance` - coordinator-driven query
- `GET /agent-capabilities` - agent registry and integration overview
- `GET /check-attendance` - scheduled attendance agent action
- `GET /mentor/<mentor_id>/students` - mentor dashboard data

## Database

The MongoDB seed data includes richer academic profiles for realistic agent responses:

- Student demographics, mentor assignment, parent contact, learning profile, and risk tags
- Course catalog with credits, faculty, department, and semester
- Attendance totals plus optional subject-level breakdown
- Marks, SGPA, CGPA, credits earned, backlogs, and academic standing
- Semester-wise result tables with course code, course name, grade, grade points, credits, result, SGPA, and percentage
- Assignments, mentor notes, scholarships, fee payments, pending fees, and alert logs
- Parent result notification messages are generated from the latest semester result table

## Frontend

The frontend uses React with browser-loaded React scripts, plus CSS for styling. It does not require a build step yet.

- `frontend/index.html` loads React and the app root.
- `frontend/app.js` contains React components for voice input, agent display, responses, traces, and data cards.
- `frontend/style.css` controls the visual design.

When Node.js and npm are available, this can be upgraded to a Vite React app.

## Version Control

The repository ignores virtual environments, caches, local env files, build outputs, and logs. Commit source files, docs, schemas, and configuration examples.
