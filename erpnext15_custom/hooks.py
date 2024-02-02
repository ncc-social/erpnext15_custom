app_name = "erpnext15_custom"
app_title = "Erpnext15 Custom"
app_publisher = "NACOC"
app_description = "ERPNext 15 Customisations"
app_email = "social@ncc.gov.gh"
app_license = "mit"
required_apps = ["frappe/erpnext/hrms"]

fixtures = [
    {"dt": "Property Setter", "filters": [
        [
            "doc_type", "in", [
                "Employee",
                "Leave Application",
                "Leave Type",
                "Training Event",
                "Vehicle",
                "Notification",
                "Notification Recipient",
                "Print Format",
                "Issue",
                "User",
                "Report",
                "Workspace",
                "Dashboard",
                "Employee Transfer"
            ]
        ]
    ]},
    {"dt": "Custom Field", "filters": [
        [
            "dt", "in", [
                "Leave Application",
                "Vehicle",
                "Employee",
                "Notification",
                "Report",
                "Training Event"

            ]
        ]
    ]},
    {"dt": "Notification", "filters": [
        [
            "document_type", "in", [
                "Leave Application"
            ]
        ]
    ]},
    {"dt": "Client Script", "filters": [
        [
            "dt", "in", [
                "Employee",
                "Leave Application"
            ]
        ]
    ]},
    {"dt": "Workflow State"},
    {"dt": "Workflow Action Master"},
    {"dt": "Workflow", "filters": [
        [
            "document_type", "in", [
                "Leave Application"
            ]
        ]
    ]},
    {"dt": "Print Format", "filters": [
        [
            "doc_type", "in", [
                "Leave Application"
            ]
        ]
    ]},
    {"dt": "Workspace", "filters": [
        [
            "module", "in", [
                "Erpnext15 Custom"
            ]
        ]
    ]},
    {"dt": "Report", "filters": [
        [
            "ref_doctype", "in", [
                "Leave Application",
                "Employee"
            ]
        ]
    ]},
    {"dt": "Auto Email Report", "filters": [
        [
            "report", "in", [
                "Leaves started in the previous month"
            ]
        ]
    ]},
    {"dt": "Role"},
    {"dt": "Role Profile"},
    {"dt": "Module Profile", "filters": [
        [
            "module_profile_name", "in", [
                "Staff Profile"
            ]
        ]
    ]}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext15_custom/css/erpnext15_custom.css"
app_include_js = [
    "/assets/erpnext15_custom/js/custom/workflow.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/erpnext15_custom/css/erpnext15_custom.css"
# web_include_js = "/assets/erpnext15_custom/js/erpnext15_custom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "erpnext15_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "erpnext15_custom/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "erpnext15_custom.utils.jinja_methods",
#	"filters": "erpnext15_custom.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "erpnext15_custom.install.before_install"
# after_install = "erpnext15_custom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "erpnext15_custom.uninstall.before_uninstall"
# after_uninstall = "erpnext15_custom.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "erpnext15_custom.utils.before_app_install"
# after_app_install = "erpnext15_custom.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "erpnext15_custom.utils.before_app_uninstall"
# after_app_uninstall = "erpnext15_custom.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext15_custom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Employee": "erpnext15_custom.my_scripts.CustomEmployee.CustomEmployee"
}

# Document Events
# ---------------
# Hook on document methods and events

#doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
    # "Leave Application": {
	# 	"on_submit": "erpnext15_custom.my_scripts.leave_application.on_submit",
	# 	"on_cancel": "erpnext15_custom.my_scripts.leave_application.on_cancel",
	# }
#    "User": {
#        "validate": "erpnext15_custom.my_scripts.custom.validate"
#    }
#}

# Scheduled Tasks
# ---------------

scheduler_events = {
#	"all": [
#		"erpnext15_custom.tasks.all"
#	],
	"daily": [
		"erpnext15_custom.my_scripts.birthday_reminder.send_birthday_reminders"
	],
#	"hourly": [
#		"erpnext15_custom.tasks.hourly"
#	],
#	"weekly": [
#		"erpnext15_custom.tasks.weekly"
#	],
#	"monthly": [
#		"erpnext15_custom.tasks.monthly"
#	],
}

# Testing
# -------

# before_tests = "erpnext15_custom.install.before_tests"

# Overriding Methods
# ------------------------------
#
#override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "erpnext15_custom.event.get_events",
#   "frappe.core.doctype.user.user.set_full_name": "erpnext15_custom.my_scripts.custom.set_full_name"
#}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "erpnext15_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["erpnext15_custom.utils.before_request"]
# after_request = ["erpnext15_custom.utils.after_request"]

# Job Events
# ----------
# before_job = ["erpnext15_custom.utils.before_job"]
# after_job = ["erpnext15_custom.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"erpnext15_custom.auth.validate"
# ]
