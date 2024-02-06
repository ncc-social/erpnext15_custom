import frappe
from frappe.utils import today

@frappe.whitelist()
def get_upcoming_holidays(holiday_list_name, limit):
    # Fetch upcoming holidays without considering permissions
    holidays = frappe.get_all(
        "Holiday",
        filters={
            "parent": holiday_list_name,
            "parenttype": "Holiday List",
            "parentfield": "holidays",
            "description": ["not in", ("Saturday", "Sunday")],
            "holiday_date": [">", today()]
        },
        fields=["holiday_date", "description"],
        order_by="holiday_date",
        limit_page_length=limit
    )

    return holidays
