// Copyright (c) 2026, jishnusuni and contributors
// For license information, please see license.txt

frappe.query_reports["Session Analysis Report"] = {
    filters: [
        {
            fieldname: "conference",
            label: "Conference",
            fieldtype: "Link",
            options: "Conference",
            reqd: 0,
            get_query: function() {
                // Only show non-cancelled conferences
                return {
                    filters: {
                        status: ["!=", "Cancelled"]
                    }
                };
            }
        },
        {
            fieldname: "session",
            label: "Session",
            fieldtype: "Link",
            options: "Session",
            reqd: 0,
            get_query: function() {
                // Get currently selected conference from report filter
                let selected_conference = frappe.query_report.get_filter_value("conference");
                let filters = {};
                if (selected_conference) {
                    filters["conference"] = selected_conference;
                }
                return { filters: filters };
            }
        }
    ]
};
