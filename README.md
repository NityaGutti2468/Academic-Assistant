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
python app.py
```

5. Open `http://127.0.0.1:5000`. The frontend and API are served by the same Flask application.

The mentor and admin dashboard is available at `http://127.0.0.1:5000/dashboard`.

## Deploy on Vercel

The repository includes a root `app.py` WSGI entrypoint and root `requirements.txt`, so Vercel can detect and deploy the Flask application directly.

1. Create a MongoDB Atlas database and allow connections from Vercel.
2. Import this GitHub repository into Vercel.
3. Add these Vercel environment variables:

```bash
MONGO_URI=mongodb+srv://...
MONGO_DB=college_ai
ENABLE_SCHEDULER=false
SECRET_KEY=replace-with-a-long-random-value
DASHBOARD_ADMIN_PASSWORD=replace-with-a-strong-password
DASHBOARD_MENTOR_PASSWORD=replace-with-a-strong-password
```

4. Add optional Groq, OpenAI, Twilio, and SMTP variables only for the integrations you want to enable.
5. Seed the Atlas database once from a trusted local machine:

```bash
python database/seed_db.py
```

Vercel functions are request-driven, so the in-process APScheduler must remain disabled there. Use Vercel Cron or another external scheduler for recurring attendance and fee checks.

The included seed records are synthetic demo data. Do not place real student or parent information in a public deployment.

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

- `GET /` - student assistant frontend
- `GET /api/health` - backend health message
- `GET /voice-query?q=show my attendance` - coordinator-driven query
- `GET /agent-capabilities` - agent registry and integration overview
- `POST /check-attendance` - authenticated attendance agent action
- `GET /mentor/<mentor_id>/students` - mentor dashboard data
- `POST /marks/<student_id>/notify` - send a result notification

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

The frontend uses React with browser-loaded React scripts, plus CSS for styling. It does not require a build step.

- Flask serves `frontend/index.html` at `/` and frontend assets under `/frontend/`.
- `frontend/app.js` contains React components for voice input, agent display, responses, traces, and data cards.
- `frontend/style.css` controls the visual design.

When Node.js and npm are available, this can be upgraded to a Vite React app.

## Version Control

The repository ignores virtual environments, caches, local env files, build outputs, and logs. Commit source files, docs, schemas, and configuration examples.
