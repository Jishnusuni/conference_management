# Copyright (c) 2026, jishnusuni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today,getdate

class Conference(Document):
    def validate(self):
        self.update_status()

    def update_status(self):
        if self.status == "Cancelled":
            return

        today_date = getdate(today())
        start_date = getdate(self.start_date)
        end_date = getdate(self.end_date)

        if today_date < start_date:
            self.status = "Upcoming"
        elif start_date <= today_date <= end_date:
            self.status = "Ongoing"
        else:
            self.status = "Completed"
