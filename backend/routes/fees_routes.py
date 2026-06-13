from flask import Blueprint
from auth import require_role
from services.fees_service import check_fees

fees_bp = Blueprint("fees", __name__)

@fees_bp.route("/fee-reminders", methods=["POST"])
@require_role("admin")
def fees():

    reminders = check_fees()

    return {"reminders": reminders}
