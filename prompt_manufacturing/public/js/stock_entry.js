// frappe.ui.form.on("Stock Entry", {
//     after_save: function (frm) {
        
//         frm.doc.items.forEach((row) => {
//             frappe.call({
//                 method: "prompt_manufacturing.public.py.serial_no_update.serial_no_update",
//                 args: {
//                     stock_entry: frm.doc.name, // Pass the current Stock Entry name
//                     item_code: row.item_code, // Example: Pass the item code
//                     serial_no: row.serial_no, // Pass the serial numbers
//                 }
//             });
//             console.log("Hello")
//         });
//     },
// });
