# Copyright (c) 2026, jishnusuni and contributors
# For license information, please see license.txt

# import frappe

import frappe

def execute(filters=None):
    """
    Script report to show:
    - Session Name
    - Total Registrations
    - Remaining Capacity
    - Revenue (based on paid registrations, 100 per paid registration)
    Optional filters: Conference, Session
    """

    if filters is None:
        filters = {}

    # Report columns
    columns = [
        {"fieldname": "session", "label": "Session", "fieldtype": "Link", "options": "Session", "width": 250},
        {"fieldname": "conference", "label": "Conference", "fieldtype": "Link", "options": "Conference", "width": 200},
        {"fieldname": "total_registrations", "label": "Total Registrations", "fieldtype": "Int", "width": 150},
        {"fieldname": "remaining_capacity", "label": "Remaining Capacity", "fieldtype": "Int", "width": 150},
        {"fieldname": "revenue", "label": "Revenue (₹)", "fieldtype": "Currency", "width": 150},
    ]

    data = []

    # Build session filters
    session_filters = {}
    if filters.get("conference"):
        session_filters["conference"] = filters.get("conference")
    if filters.get("session"):
        session_filters["name"] = filters.get("session")

    # Fetch sessions
    sessions = frappe.get_all(
        "Session",
        filters=session_filters,
        fields=["name", "session_name", "conference", "max_attendees"],
        order_by="start_time asc"
    )

    for sess in sessions:
        # Count total registrations
        total_registrations = frappe.db.count("Registration", {"session": sess.name})

        # Count paid registrations for revenue
        paid_registrations = frappe.db.count("Registration", {"session": sess.name, "payment_status": "Paid"})

        # Remaining capacity
        max_capacity = sess.max_attendees or 0
        remaining_capacity = max_capacity - total_registrations

        # Revenue (₹100 per paid registration)
        revenue = paid_registrations * 100

        data.append({
            "session": sess.name,
            "conference": sess.conference,
            "total_registrations": total_registrations,
            "remaining_capacity": remaining_capacity,
            "revenue": revenue
        })

    return columns, data
