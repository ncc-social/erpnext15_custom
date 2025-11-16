// // Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// // MIT License. See license.txt

// class WorkflowOverride extends frappe.ui.form.States {

// 	show_actions() {
// 		var added = false;
// 		var me = this;

// 		// if the loaded doc is dirty, don't show workflow buttons
// 		if (this.frm.doc.__unsaved === 1) {
// 			return;
// 		}

// 		function has_approval_access(transition) {
// 			let approval_access = false;
// 			const user = frappe.session.user;
// 			if (
// 				user === "Administrator" ||
// 				transition.allow_self_approval ||
// 				user !== me.frm.doc.owner
// 			) {
// 				approval_access = true;
// 			}
// 			return approval_access;
// 		}

// 		frappe.workflow.get_transitions(this.frm.doc).then((transitions) => {
// 			this.frm.page.clear_actions_menu();
// 			transitions.forEach((d) => {
// 				if (frappe.user_roles.includes(d.allowed) && has_approval_access(d)) {
// 					added = true;
// 					me.frm.page.add_action_item(__(d.action), function () {
// 						// Check if doctype is Leave Application and action clicked is Reject
//                         if (d.action == "Reject" && me.frm.doc.doctype == "Leave Application") {
//                             var leave_title = (me.frm.doc.leave_type === "Annual Leave - JD" || me.frm.doc.leave_type === "Annual Leave - SD") ? "Annual Leave" : me.frm.doc.leave_type;
//                             frappe.prompt([
//                                 {
//                                     fieldname: 'reject_reason',
//                                     label: 'Reason for rejection',
//                                     fieldtype: 'Small Text',
//                                     reqd: 1,
//                                 },
//                             ], (values) => {
//                                 // Set value of Rejection Reason in form
//                                 me.frm.set_value('custom_rejection_reason', values.reject_reason);
//                                 frappe.dom.freeze();
//                                 frappe
//                                     .xcall("erpnext15_custom.my_scripts.workflow.before_transition", {
//                                         doc: me.frm.doc,
//                                         transition: d
//                                     })
//                                     .then((res) => {
//                                         if (res) {
//                                             me.frm.selected_workflow_action = d.action;
//                                             me.frm.script_manager.trigger("before_workflow_action").then(() => {
//                                             frappe
//                                                 .xcall("frappe.model.workflow.apply_workflow", {
//                                                     doc: me.frm.doc,
//                                                     action: d.action,
//                                                 })
//                                                 .then((doc) => {
//                                                     frappe.model.sync(doc);
//                                                     me.frm.refresh();
//                                                     me.frm.selected_workflow_action = null;
//                                                     me.frm.script_manager.trigger("after_workflow_action");
//                                                 })
//                                                 .finally(() => {
//                                                     frappe.dom.unfreeze();
//                                                 });
//                                             });
//                                         } else {
//                                             frappe.dom.unfreeze();
//                                             frappe.msgprint(`Sorry! we could not proceed`);
//                                         }
//                                     })
//                             }, me.frm.doc.employee_name +'\'s ' + leave_title + ' Application');
//                         } else {
//                             me.frm.script_manager.trigger("before_workflow_action").then(() => {
//                                 frappe
//                                     .xcall("frappe.model.workflow.apply_workflow", {
//                                         doc: me.frm.doc,
//                                         action: d.action,
//                                     })
//                                     .then((doc) => {
//                                         frappe.model.sync(doc);
//                                         me.frm.refresh();
//                                         me.frm.selected_workflow_action = null;
//                                         me.frm.script_manager.trigger("after_workflow_action");
//                                     })
//                                     .finally(() => {
//                                         frappe.dom.unfreeze();
//                                     });
//                             });
//                         }
                        
// 					});
// 				}
// 			});

// 			this.setup_btn(added);
// 		});
// 	}

// };

// frappe.ui.form.States = WorkflowOverride;

class WorkflowOverride extends frappe.ui.form.States {

    show_actions() {
        var added = false;
        var me = this;

        if (this.frm.doc.__unsaved === 1) return;

        function has_approval_access(transition) {
            const user = frappe.session.user;
            return (
                user === "Administrator" ||
                transition.allow_self_approval ||
                user !== me.frm.doc.owner
            );
        }

        frappe.workflow.get_transitions(this.frm.doc).then((transitions) => {
            this.frm.page.clear_actions_menu();

            transitions.forEach((d) => {
                if (frappe.user_roles.includes(d.allowed) && has_approval_access(d)) {

                    added = true;
                    me.frm.page.add_action_item(__(d.action), function () {

                        // ---- CUSTOM HANDLER FOR REJECTION ----
                        if (
                            d.action === "Reject" &&
                            ["Leave Application", "Vehicle Maintenance Allowance"].includes(me.frm.doc.doctype)
                        ) {

                            const title =
                                me.frm.doc.doctype === "Vehicle Maintenance Allowance"
                                    ? `${me.frm.doc.employee_name}'s Vehicle Maintenance Allowance`
                                    : `${me.frm.doc.employee_name}'s ${
                                        (me.frm.doc.leave_type === "Annual Leave - JD" || me.frm.doc.leave_type === "Annual Leave - SD")
                                            ? "Annual Leave"
                                            : me.frm.doc.leave_type
                                    }`;

                            frappe.prompt([
                                {
                                    fieldname: "reject_reason",
                                    label: "Reason for Rejection",
                                    fieldtype: "Small Text",
                                    reqd: 1
                                }
                            ], (values) => {

                                // Save value to form field
                                me.frm.set_value("custom_rejection_reason", values.reject_reason);

                                frappe.dom.freeze();

                                // Save to database + allow transition
                                frappe.xcall("erpnext15_custom.my_scripts.workflow.before_transition", {
                                    doc: me.frm.doc,
                                    transition: d
                                }).then(res => {

                                    if (!res) {
                                        frappe.dom.unfreeze();
                                        frappe.msgprint("Could not proceed.");
                                        return;
                                    }

                                    me.frm.selected_workflow_action = d.action;

                                    me.frm.script_manager.trigger("before_workflow_action").then(() => {
                                        frappe
                                            .xcall("frappe.model.workflow.apply_workflow", {
                                                doc: me.frm.doc,
                                                action: d.action,
                                            })
                                            .then((doc) => {

                                                // Add comment to document
                                                frappe.xcall("frappe.desk.form.utils.add_comment", {
                                                    reference_doctype: me.frm.doc.doctype,
                                                    reference_name: me.frm.doc.name,
                                                    content: `Rejection Reason: ${values.reject_reason}`,
                                                    comment_email: frappe.session.user
                                                });

                                                frappe.model.sync(doc);
                                                me.frm.refresh();

                                                me.frm.selected_workflow_action = null;
                                                me.frm.script_manager.trigger("after_workflow_action");
                                            })
                                            .finally(() => {
                                                frappe.dom.unfreeze();
                                            });

                                    });

                                });

                            }, title);
                        }

                        // ---- DEFAULT HANDLER ----
                        else {
                            me.frm.script_manager.trigger("before_workflow_action").then(() => {
                                frappe
                                    .xcall("frappe.model.workflow.apply_workflow", {
                                        doc: me.frm.doc,
                                        action: d.action,
                                    })
                                    .then((doc) => {
                                        frappe.model.sync(doc);
                                        me.frm.refresh();
                                        me.frm.selected_workflow_action = null;
                                        me.frm.script_manager.trigger("after_workflow_action");
                                    })
                                    .finally(() => frappe.dom.unfreeze());
                            });
                        }

                    });
                }
            });

            this.setup_btn(added);
        });
    }
};

frappe.ui.form.States = WorkflowOverride;
