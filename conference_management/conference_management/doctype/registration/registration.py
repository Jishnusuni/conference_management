# Copyright (c) 2026, jishnusuni and contributors
# For license information, please see license.txt

# registration.py

import frappe
import random
from frappe.model.document import Document


class Registration(Document):

    def validate(self):
        """
        Main validation entry point.
        This method is automatically called before saving the document.
        """
        # Restrict overlapping session registrations for the same attendee
        self.validate_attendee_session_overlap()

        # Enforce session capacity limit
        self.validate_session_capacity()


    def validate_attendee_session_overlap(self):
        """
        Prevent an attendee from registering for more than one
        session scheduled at the same time.

        Overlap rule:
        new_start < existing_end AND new_end > existing_start
        """
        # Fetch the selected session details
        session = frappe.get_doc("Session", self.session)

        # Check for overlapping registrations for the same attendee
        overlapping = frappe.db.sql("""
            SELECT r.name
            FROM `tabRegistration` r
            INNER JOIN `tabSession` s ON r.session = s.name
            WHERE r.attendee = %s
              AND r.name != %s
              AND r.payment_status != 'Failed'
              AND (%s < s.end_time AND %s > s.start_time)
        """, (
            self.attendee,          # Same attendee
            self.name or "",        # Exclude current registration (edit case)
            session.start_time,     # New session start datetime
            session.end_time        # New session end datetime
        ))

        # If any overlapping session exists, block registration
        if overlapping:
            frappe.throw(
                "Attendee is already registered for another session "
                "scheduled during this time."
            )

    def validate_session_capacity(self):
        """
        Prevent registration if the session has reached
        its maximum attendee capacity.

        Only PAID registrations are counted.
        """
        # Get max attendee limit from Session
        max_attendees = frappe.db.get_value(
            "Session", self.session, "max_attendees"
        )

        # If no capacity limit is defined, allow registration
        if not max_attendees:
            return

        # Count confirmed (Paid) registrations
        current_count = frappe.db.count(
            "Registration",
            {
                "session": self.session,
                "payment_status": "Paid"
            }
        )

        # Block registration if capacity is exceeded
        if current_count >= max_attendees:
            frappe.throw(
                "This session has reached its maximum attendee capacity."
            )
