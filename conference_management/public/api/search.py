# search.py

import frappe
from frappe.utils import getdate, today

@frappe.whitelist(allow_guest=True)
def search_conferences_sessions(keyword):
    """
    Search conferences and sessions by keyword.
    Searches in conference_name, description, session_name, and speaker.

    Args:
        keyword (str): Search term

    Returns:
        dict: Matching conferences and sessions
    """
    if not keyword:
        return {"status": "error", "message": "Keyword is required."}

    keyword = keyword.strip()

    # 1. Search conferences by name or description
    conferences = frappe.get_all(
        "Conference",
        filters={
            "status": ["!=", "Cancelled"],
            "start_date": [">=", getdate(today())]
        },
        fields=[
            "name",
            "conference_name",
            "start_date",
            "end_date",
            "location",
            "description",
            "status"
        ],
        order_by="start_date asc"
    )

    # Filter conferences containing the keyword
    matching_conferences = [
        conf for conf in conferences
        if keyword.lower() in (conf.conference_name or "").lower() or
           keyword.lower() in (conf.description or "").lower()
    ]

    # 2. Search sessions by session_name or speaker
    sessions = frappe.get_all(
        "Session",
        filters={
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

    matching_sessions = [
        sess for sess in sessions
        if keyword.lower() in (sess.session_name or "").lower() or
           keyword.lower() in (sess.speaker or "").lower()
    ]

    # 3. Build response
    return {
        "status": "success",
        "keyword": keyword,
        "conferences": matching_conferences,
        "sessions": matching_sessions
    }
