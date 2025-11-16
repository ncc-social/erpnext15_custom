# import frappe
# import json

# @frappe.whitelist()
# def before_transition():
#     """
#     Check current state before we proceed to next state
#     """
#     doc = frappe._dict(json.loads(frappe.form_dict.doc))
#     transition = frappe._dict(json.loads(frappe.form_dict.transition))
#     frappe.db.set_value(doc.doctype, doc.name, 'custom_rejection_reason', doc.custom_rejection_reason)
#     return True

import frappe
import json

@frappe.whitelist()
def before_transition():
    """Save rejection reason field before workflow transition."""
    doc = frappe._dict(json.loads(frappe.form_dict.doc))
    transition = frappe._dict(json.loads(frappe.form_dict.transition))

    if doc.get("custom_rejection_reason"):
        frappe.db.set_value(
            doc.doctype,
            doc.name,
            "custom_rejection_reason",
            doc.custom_rejection_reason,
        )

    return True
