from dataclasses import dataclass
from typing import Callable

from services.attendance_service import get_student_attendance
from services.fees_service import get_student_fees
from services.marks_service import get_academic_report


@dataclass(frozen=True)
class AgentTool:
    name: str
    agent_name: str
    description: str
    keywords: tuple[str, ...]
    handler: Callable[[int], dict]
    framework_ready: tuple[str, ...]


def academic_summary_tool(student_id):
    report = get_academic_report(student_id)
    summary = report["summary"]
    insights = report.get("insights", {})

    message = f"Your current SGPA is {summary['sgpa']} and CGPA is {summary['cgpa']}."
    if insights.get("strongest"):
        message += f" You are doing great in {insights['strongest']}."
    if insights.get("weakest"):
        message += f" You need to pay more attention to {insights['weakest']}."

    return {"message": message, "data": summary, "report": report}


AGENT_TOOLS = (
    AgentTool(
        name="get_student_attendance",
        agent_name="Attendance Agent",
        description="Checks attendance status and low-attendance risk.",
        keywords=("attendance", "present", "absent", "classes"),
        handler=get_student_attendance,
        framework_ready=("LangChain Tool", "CrewAI Tool", "AutoGen Function"),
    ),
    AgentTool(
        name="get_academic_report",
        agent_name="Academic Agent",
        description="Analyzes marks, SGPA, CGPA, grade risk, and subject strengths.",
        keywords=("marks", "cgpa", "sgpa", "result", "score", "grade", "fail", "pass"),
        handler=academic_summary_tool,
        framework_ready=("LangChain Tool", "CrewAI Agent", "RAG Context Consumer"),
    ),
    AgentTool(
        name="get_student_fees",
        agent_name="Fee Agent",
        description="Checks pending fees, due dates, and late penalties.",
        keywords=("fee", "fees", "due", "pay", "pending", "amount", "rupees", "balance"),
        handler=get_student_fees,
        framework_ready=("LangChain Tool", "n8n Workflow Trigger", "AutoGen Function"),
    ),
)


def list_agent_capabilities():
    return [
        {
            "tool": tool.name,
            "agent": tool.agent_name,
            "description": tool.description,
            "keywords": list(tool.keywords),
            "framework_ready": list(tool.framework_ready),
        }
        for tool in AGENT_TOOLS
    ]


def select_tool(query):
    normalized_query = query.lower()
    for tool in AGENT_TOOLS:
        if any(keyword in normalized_query for keyword in tool.keywords):
            return tool
    return None
