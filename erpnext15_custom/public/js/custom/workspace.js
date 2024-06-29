frappe.ui.form.on("Workspace", {
    onload: frm => {
        $('div[item-parent="HR"]').parent().hide();
        $('a[title="HR"]').siblings('div').hide();
    }
});

