from services.agent_registry import list_agent_capabilities, select_tool


def route_query(query, student_id=1):
    tool = select_tool(query)

    if not tool:
        return {
            "message": "Sorry, I could not understand the query. Please ask about attendance, marks, or fees.",
            "agent": "Coordinator Agent",
            "tool": None,
            "trace": ["Coordinator Agent received query", "No matching specialized agent found"],
        }

    response = tool.handler(int(student_id))
    response.update({
        "agent": tool.agent_name,
        "tool": tool.name,
        "trace": [
            "Coordinator Agent received query",
            f"Selected {tool.agent_name}",
            f"Executed tool {tool.name}",
        ],
    })
    return response


def get_capabilities():
    return {
        "system": "Multi-Agent Academic Assistant",
        "coordinator": "Coordinator Agent",
        "agents": list_agent_capabilities(),
        "integrations": {
            "database": "MongoDB",
            "api": "Flask REST",
            "filesystem": "Project docs and MCP manifest",
            "mcp": "backend/mcp_manifest.json",
            "framework_adapters": ["LangChain", "CrewAI", "AutoGen", "RAG", "n8n"],
        },
    }
