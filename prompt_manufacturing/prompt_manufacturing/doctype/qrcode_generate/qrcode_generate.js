// Copyright (c) 2024, Rutika Rathod and contributors
// For license information, please see license.txt

frappe.ui.form.on("Qrcode Generate", {
    grn_no: function(frm) {
        // Ensure grn_no is not empty
        

        // Call the server-side method
        frappe.call({
            method: "prompt_manufacturing.public.py.qrcode_img.serial_no_img",
            args: {
                grn_no: frm.doc.grn_no
            },
            callback: function(r) {
                var len = r.message.length
                var serial_items = r.message;

                for(var i = 0; i < len; i++) {
                    var row = frm.add_child("qrcode_item_details");
                    row.item_code = serial_items[i].item_code;
                    row.item_name = serial_items[i].item_name;
                    row.serial_no = serial_items[i].serial_no;
                   


                }
                frm.refresh_field("qrcode_item_details");
            }
        });
    },
    refresh: function(frm) {
        frm.set_query("grn_no", function() {
            return {
                filters: {
                    custom_qrcode_generate: 0
                }
            };
        });
    },
    after_save: function(frm) {
        if (frm.doc.grn_no) { // Ensure GRN No is available
            frappe.db.set_value("Purchase Receipt", frm.doc.grn_no, "custom_qrcode_generate", 1)
                .then(() => {
                    
                })
                
        } else {
            frappe.msgprint("GRN No is not specified.");
        }
    }
    
});
