// Copyright (c) 2026, jishnusuni and contributors
// For license information, please see license.txt

frappe.query_reports["Conference Report"] = {
    filters: [
        {
            fieldname: "conference",
            label: "Conference",
            fieldtype: "Link",
            options: "Conference",
            reqd: 0,  // Optional filter
            get_query: function() {
                // Only show non-cancelled conferences in the dropdown
                return {
                    filters: {
                        status: ["!=", "Cancelled"]
                    }
                };
            }
        }
    ]
};
