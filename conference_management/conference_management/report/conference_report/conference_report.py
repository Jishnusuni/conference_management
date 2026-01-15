# Copyright (c) 2026, jishnusuni and contributors
# For license information, please see license.txt

# import frappe

import frappe

def execute(filters=None):
    """
    Script report to show:
    - Total attendees for each conference
    - Number of sessions per conference
    Optional filter: Conference
    """

    if filters is None:
        filters = {}

    # Define report columns
    columns = [
        {"fieldname": "conference", "label": "Conference", "fieldtype": "Link", "options": "Conference", "width": 250},
        {"fieldname": "total_sessions", "label": "Number of Sessions", "fieldtype": "Int", "width": 150},
        {"fieldname": "total_attendees", "label": "Total Attendees", "fieldtype": "Int", "width": 150}
    ]

    data = []

    # Build filters for conferences
    conf_filters = {
        "status": ["!=", "Cancelled"],  # Exclude cancelled conferences
        "docstatus": 0                   # Only non-submitted conferences
    }

    if filters.get("conference"):
        conf_filters["name"] = filters.get("conference")

    # Fetch conferences based on filter
    conferences = frappe.get_all(
        "Conference",
        filters=conf_filters,
        fields=["name", "conference_name"]
    )

    for conf in conferences:
        # Count sessions for this conference
        total_sessions = frappe.db.count("Session", {"conference": conf.name})

        # Count distinct attendees registered for this conference
        total_attendees = frappe.db.sql("""
            SELECT COUNT(DISTINCT attendee) 
            FROM `tabRegistration`
            WHERE conference=%s
        """, conf.name)[0][0] or 0

        data.append({
            "conference": conf.name,
            "total_sessions": total_sessions,
            "total_attendees": total_attendees
        })

    return columns, data
