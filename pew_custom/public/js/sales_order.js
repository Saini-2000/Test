frappe.ui.form.on('Sales Order', {
  
    refresh: function(frm) {

        sync_users_with_table(frm);
    },
    custom_users: function(frm) {
        sync_users_with_table(frm);
    }
});

function sync_users_with_table(frm) {
    let selected_users = frm.doc.custom_users || [];
    let userdemo_table = frm.doc.custom_data || [];

    let current_users_in_table = userdemo_table.map(row => row.custom_helo);

    selected_users.filter(user_obj => !current_users_in_table.includes(user_obj['userss']))
        .forEach(user_obj => {
            let new_row = frm.add_child('custom_userdemo');
            new_row.custom_helo = user_obj['userss'];
        });

    frm.doc.custom_userdemo = userdemo_table.filter(row =>
        selected_users.some(user_obj => user_obj['userss'] === row.custom_helo)
    );

    frm.refresh_field('custom_userdemo');
    frm.dirty();
}

// Multiselect Field Name : custom_tms
// Child Table Name : custom_userdemo
// Child Table field name : custom_helo
// ( userss ) is the link field from child table which is connected with multiselect field 









