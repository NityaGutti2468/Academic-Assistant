from flask import Blueprint, request
from services.coordinator_agent import get_capabilities
from services.voice_service import process_query

voice_bp = Blueprint("voice", __name__)

@voice_bp.route("/voice-query")

def voice_query():

    query = request.args.get("q")
    student_id = request.args.get("student_id", 1)

    response = process_query(query, student_id=student_id)

    return {
        "query": query,
        "response": response
    }


@voice_bp.route("/agent-capabilities")
def agent_capabilities():
    return get_capabilities()
