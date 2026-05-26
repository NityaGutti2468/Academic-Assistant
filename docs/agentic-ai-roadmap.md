# Agentic AI Alignment Roadmap

This project is now organized as a multi-agent academic assistant. The current implementation is intentionally lightweight and can later be upgraded to LangChain, CrewAI, AutoGen, or n8n without changing the user-facing routes.

## Level 5 Checklist

- Multi-agent systems: `Coordinator Agent` delegates to specialized attendance, academic, fee, mentor, notification, and voice agents.
- Multiple AI agents for complex tasks: every query returns the selected agent, tool used, and trace metadata.
- MCP: `backend/mcp_manifest.json` describes available tools, resources, and agent entry points in a Model Context Protocol style.
- Databases, APIs, and file systems: MongoDB is the primary resource; Flask exposes API routes; docs and manifests provide file-system context.
- Agentic AI frameworks: `backend/services/agent_registry.py` provides the adapter boundary for future LangChain, CrewAI, AutoGen, RAG, and n8n integrations.
- Real-world project: the app monitors attendance, fees, marks, mentors, notifications, and voice queries.

## Next Upgrade Path

1. Add RAG over college policies, fee circulars, and syllabus PDFs.
2. Add an MCP server wrapper around the registered tools.
3. Add LangChain or CrewAI adapters behind the registry.
4. Add n8n workflows for WhatsApp/SMS/email escalations.
5. Add tests for coordinator intent routing and agent tool outputs.
