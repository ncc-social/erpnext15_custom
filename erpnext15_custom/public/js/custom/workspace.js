$(document).ready(function () {
    function hideHRElementsIfNoRelevantRoles() {
        // Ensure frappe.user_roles is defined
        if (!frappe.user_roles) {
            console.error("frappe.user_roles is not defined");
            return;
        }

        // Array of roles that should be checked
        const relevantRoles = ["System Manager", "HR User", "HR Manager"];

        // Check if none of the relevant roles are present in frappe.user_roles
        const noRelevantRolesPresent = !relevantRoles.some(role => frappe.user_roles.includes(role));

        // Log the result for debugging
        console.log(noRelevantRolesPresent); // true if none of the relevant roles are present, false otherwise

        // Perform actions based on the check
        if (noRelevantRolesPresent) {
            // Hide elements if none of the relevant roles are present
            frappe.pages['Workspaces'].page.sidebar.find('div[item-parent="HR"]').parent().hide();
            frappe.pages['Workspaces'].page.sidebar.find('a[title="HR"]').siblings('div').hide();
        }
    }

    // Use a timeout to ensure elements are loaded
    setTimeout(hideHRElementsIfNoRelevantRoles, 1000); // Adjust the delay as needed
});