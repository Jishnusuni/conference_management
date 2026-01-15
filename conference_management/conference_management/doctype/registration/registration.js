// Copyright (c) 2026, jishnusuni and contributors
// For license information, please see license.txt


frappe.ui.form.on('Registration', {
    
    conference(frm) {
        // Clear session when conference changes
        frm.set_value('session', null);

        // Filter sessions by selected conference
        frm.set_query('session', () => {
            return {
                filters: {
                    conference: frm.doc.conference
                }
            };
        });
    }
});
