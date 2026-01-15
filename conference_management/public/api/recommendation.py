# recommendation.py

import frappe
from frappe.utils import today

@frappe.whitelist(allow_guest=True)
def get_attendee_recommendations(attendee):
    """
    Fetch recommended sessions for an attendee based on their preferences.

    Args:
        attendee (str): Attendee DocType name

    Returns:
        dict: Recommended sessions
    """

    # Validate attendee exists
    if not attendee or not frappe.db.exists("Attendee", attendee):
        return {"status": "error", "message": "Attendee not found."}

    # Fetch attendee document
    attendee_doc = frappe.get_doc("Attendee", attendee)

    # Collect preferred sessions from the child table
    preferred_sessions = [row.session for row in (attendee_doc.preferences or [])]

    if not preferred_sessions:
        return {"status": "success", "recommendations": [], "message": "No preferences found."}

    # Fetch upcoming sessions with same speakers as preferred sessions
    preferred_speakers = frappe.get_all(
        "Session",
        filters={"name": ["in", preferred_sessions]},
        fields=["speaker"]
    )
    speakers = list(set([p.speaker for p in preferred_speakers if p.speaker]))

    # Recommended sessions: upcoming sessions by same speakers, exclude already preferred sessions
    recommended_sessions = frappe.get_all(
        "Session",
        filters={
            "speaker": ["in", speakers],
            "name": ["not in", preferred_sessions],
            "start_time": [">=", today()]
        },
        fields=[
            "name",
            "session_name",
            "speaker",
            "start_time",
            "end_time",
            "conference"
        ],
        order_by="start_time asc"
    )

    return {
        "status": "success",
        "attendee": attendee,
        "recommendations": recommended_sessions
    }
