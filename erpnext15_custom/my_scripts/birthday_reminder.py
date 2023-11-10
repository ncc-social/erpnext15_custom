import frappe
from frappe import _
from frappe.utils import comma_sep, today

from erpnext.setup.doctype.employee.employee import get_all_employee_emails, get_employee_email


# ------------------
# BIRTHDAY REMINDERS
# ------------------
def send_birthday_reminders():
	# Send Employee birthday reminders if no 'Stop Birthday Reminders' is not set.
	# to_send = int(frappe.db.get_single_value("HR Settings", "send_birthday_reminders"))
	# if not to_send:
	# 	return

	employees_born_today = get_employees_who_are_born_today()

	for company, birthday_persons in employees_born_today.items():
		employee_emails = get_all_employee_emails(company)
		birthday_person_emails = [get_employee_email(doc) for doc in birthday_persons]
		recipients = list(set(birthday_person_emails))
		#recipients = ["tj@ncc.gov.gh"]

		reminder_text, message = get_birthday_reminder_text_and_message(birthday_persons)
		send_birthday_reminder(recipients, reminder_text, birthday_persons, message)

		if len(birthday_persons) > 1:
			# special email for people sharing birthdays
			for person in birthday_persons:
				person_email = person["user_id"] or person["personal_email"] or person["company_email"]
				others = [d for d in birthday_persons if d != person]
				reminder_text, message = get_birthday_reminder_text_and_message(others)
				send_birthday_reminder(person_email, reminder_text, others, message)


def get_birthday_reminder_text_and_message(birthday_persons):
	if len(birthday_persons) == 1:
		birthday_person_text = birthday_persons[0]['name']
	else:
		# converts ["Jim", "Rim", "Dim"] to Jim, Rim & Dim
		person_names = [d['name'] for d in birthday_persons]
		birthday_person_text = comma_sep(person_names, frappe._("{0} & {1}"), False)

	reminder_text = _("{0}, today is your birthday 🎉").format(birthday_person_text)
	message = _("The Director-General and the entire staff of the Commission wish you a happy birthday.")
	message += "<br>"
	message += _("May GOD continue to bless you with long life and good health.")
	message += "<br>"
	message += _("Hope this special day brings you all that your heart desires.")

	return reminder_text, message


def send_birthday_reminder(recipients, reminder_text, birthday_persons, message):
	frappe.sendmail(
		recipients=recipients,
		subject=_("NACOC wishes you Happy Birthday"),
		template="birthday_reminder",
		args=dict(
			reminder_text=reminder_text,
			birthday_persons=birthday_persons,
			message=message,
		),
		header=_("Happy Birthday 🎂")
	)


def get_employees_who_are_born_today():
	"""Get all employee born today & group them based on their company"""
	return get_employees_having_an_event_today("birthday")


def get_employees_having_an_event_today(event_type):
	"""Get all employee who have `event_type` today
	& group them based on their company. `event_type`
	can be `birthday` or `work_anniversary`"""

	from collections import defaultdict

	# Set column based on event type
	if event_type == 'birthday':
		condition_column = 'date_of_birth'
	elif event_type == 'work_anniversary':
		condition_column = 'date_of_joining'
	else:
		return

	employees_born_today = frappe.db.multisql({
		"mariadb": f"""
			SELECT `personal_email`, `company`, `company_email`, `user_id`, `employee_name` AS 'name', `image`, `date_of_joining`
			FROM `tabEmployee`
			WHERE
				DAY({condition_column}) = DAY(%(today)s)
			AND
				MONTH({condition_column}) = MONTH(%(today)s)
			AND
				YEAR({condition_column}) < YEAR(%(today)s)
			AND
				`status` = 'Active'
		""",
		"postgres": f"""
			SELECT "personal_email", "company", "company_email", "user_id", "employee_name" AS 'name', "image"
			FROM "tabEmployee"
			WHERE
				DATE_PART('day', {condition_column}) = date_part('day', %(today)s)
			AND
				DATE_PART('month', {condition_column}) = date_part('month', %(today)s)
			AND
				DATE_PART('year', {condition_column}) < date_part('year', %(today)s)
			AND
				"status" = 'Active'
		""",
	}, dict(today=today(), condition_column=condition_column), as_dict=1)

	grouped_employees = defaultdict(lambda: [])

	for employee_doc in employees_born_today:
		grouped_employees[employee_doc.get('company')].append(employee_doc)

	return grouped_employees