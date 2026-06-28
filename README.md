# Nexia Multi-Agent Academic Assistant

Nexia is a Flask, MongoDB, and React-based academic assistant for student queries about attendance, marks, fees, mentor alerts, and notifications. It uses a Coordinator Agent to route each query to the right domain agent.

The app works without an LLM using rule-based routing. You can optionally enable Groq or OpenAI for smarter query planning and response summaries.

## Features

- Student assistant UI for academic queries
- Coordinator Agent with Attendance, Academic, and Fee tools
- Mentor/admin dashboard
- MongoDB-backed demo academic data
- Optional Groq or OpenAI LLM planner
- Optional SMTP and Twilio notification support
- Vercel-ready Flask entrypoint

## Project Structure

```text
backend/      Flask app, routes, services, auth, dashboard files
frontend/     React frontend served by Flask
database/     MongoDB seed script and schema reference
docs/         Agentic AI roadmap
app.py        Root app entrypoint
```

## Run Locally

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Start MongoDB locally and seed demo data:

```bash
python database/seed_db.py
```

4. Start the Flask app:

```bash
python app.py
```

5. Open:

```text
http://127.0.0.1:5000
```

Dashboard:

```text
http://127.0.0.1:5000/dashboard
```
