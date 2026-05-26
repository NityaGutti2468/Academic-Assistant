from services.coordinator_agent import route_query


def process_query(query, student_id=1):
    if not query:
        return {"message": "No query provided."}

    # Process speech-to-text text if needed, then forward to Coordinator
    return route_query(query, student_id=student_id)
