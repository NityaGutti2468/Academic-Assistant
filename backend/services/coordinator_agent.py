from services.agent_registry import AGENT_TOOLS, list_agent_capabilities, select_tool
from services.llm_coordinator import (
    choose_tool_with_llm,
    get_llm_model,
    get_llm_provider,
    is_llm_enabled,
    summarize_tool_result_with_llm,
)


def _find_tool_by_name(tool_name):
    for tool in AGENT_TOOLS:
        if tool.name == tool_name:
            return tool
    return None


def route_query(query, student_id=1):
    trace = ["Coordinator Agent received query"]
    planner = "Rule-Based Planner"

    if is_llm_enabled():
        try:
            llm_decision = choose_tool_with_llm(query)
            tool = _find_tool_by_name(llm_decision.get("tool"))
            planner = "LLM Planner Agent"
            trace.append(f"LLM selected {llm_decision.get('agent')}")
            trace.append(llm_decision.get("reasoning", "LLM produced a routing decision"))
        except Exception as exc:
            tool = select_tool(query)
            trace.append(f"LLM planner unavailable, using rule fallback: {exc}")
    else:
        tool = select_tool(query)
        trace.append("LLM API key not set, using rule fallback")

    if not tool:
        return {
            "message": "Sorry, I could not understand the query. Please ask about attendance, marks, or fees.",
            "agent": "Coordinator Agent",
            "tool": None,
            "planner": planner,
            "trace": trace + ["No matching specialized agent found"],
        }

    response = tool.handler(int(student_id))

    if is_llm_enabled():
        try:
            response["message"] = summarize_tool_result_with_llm(query, response)
            trace.append("LLM generated final student-facing answer")
        except Exception as exc:
            trace.append(f"LLM summarizer unavailable, using tool message: {exc}")

    response.update({
        "agent": tool.agent_name,
        "tool": tool.name,
        "planner": planner,
        "trace": trace + [
            f"Selected {tool.agent_name}",
            f"Executed tool {tool.name}",
        ],
    })
    return response


def get_capabilities():
    return {
        "system": "Multi-Agent Academic Assistant",
        "coordinator": "Coordinator Agent",
        "llm_enabled": is_llm_enabled(),
        "llm_provider": get_llm_provider(),
        "llm_model": get_llm_model(),
        "planner": "LLM Planner Agent when a provider API key is set; rule fallback otherwise",
        "agents": list_agent_capabilities(),
        "integrations": {
            "database": "MongoDB",
            "api": "Flask REST",
            "filesystem": "Project docs and MCP manifest",
            "mcp": "backend/mcp_manifest.json",
            "framework_adapters": ["LangChain", "CrewAI", "AutoGen", "RAG", "n8n"],
        },
    }
