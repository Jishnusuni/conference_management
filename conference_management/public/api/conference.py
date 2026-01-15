# conference.py

import frappe
from frappe.utils import getdate, today


@frappe.whitelist(allow_guest=True)
def get_upcoming_conferences():
    """
    Public API to fetch all upcoming conferences
    along with their sessions.

    A conference is considered upcoming if:
    - start_date >= today
    """
    today_date = getdate(today())

    # Fetch upcoming conferences
    conferences = frappe.get_all(
        "Conference",
        filters={
            "start_date": [">=", today_date],
            "status": ["!=", "Cancelled"]
        },
        fields=[
            "name",
            "conference_name",
            "start_date",
            "end_date",
            "location",
            "status",
            "description"
        ],
        order_by="start_date asc"
    )

    response = []

    for conf in conferences:
        # Fetch sessions linked to the conference
        sessions = frappe.get_all(
            "Session",
            filters={
                "conference": conf.name
            },
            fields=[
                "name",
                "session_name",
                "speaker",
                "start_time",
                "end_time",
                "max_attendees"
            ],
            order_by="start_time asc"
        )

        response.append({
            "conference": conf,
            "sessions": sessions
        })

    return response
