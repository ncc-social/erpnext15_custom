
import frappe
from frappe import _
from frappe.utils import (
	formatdate,
)

def on_submit(self):
	if self.status in ["Open", "Cancelled"]:
		frappe.throw(
			_("Only Leave Applications with status 'Approved' and 'Rejected' can be submitted")
		)

	self.validate_back_dated_application()

	# notify leave applier about approval
	if frappe.db.get_single_value("HR Settings", "send_leave_notification"):
		self.notify_employee()

	self.create_leave_ledger_entry()
	self.reload()

def validate_back_dated_application(self):
    future_allocation = frappe.db.sql("""select name, from_date from `tabLeave Allocation`
			where employee=%s and leave_type=%s and docstatus=1 and from_date > %s
			and carry_forward=1""", (self.employee, self.leave_type, self.to_date), as_dict=1)

    if future_allocation:
        frappe.throw(_("Leave cannot be applied/cancelled before {0}, as leave balance has already been carry-forwarded in the future leave allocation record {1}")
            .format(formatdate(future_allocation[0].from_date), future_allocation[0].name))

def on_cancel(self):
		self.create_leave_ledger_entry(submit=False)
		# notify leave applier about cancellation
		if frappe.db.get_single_value("HR Settings", "send_leave_notification"):
			self.notify_employee()

		self.publish_update()