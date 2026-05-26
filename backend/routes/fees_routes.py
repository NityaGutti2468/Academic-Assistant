from flask import Blueprint
from services.fees_service import check_fees

fees_bp = Blueprint("fees", __name__)

@fees_bp.route("/fee-reminders")
def fees():

    reminders = check_fees()

    return {"reminders": reminders}