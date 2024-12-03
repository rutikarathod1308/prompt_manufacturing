import frappe

@frappe.whitelist()
def serial_no_img(doc=None, grn_no=None):
    grn_no = frappe.form_dict["grn_no"]
    serial_list = []
    item_details = frappe.db.get_all(
    "Purchase Receipt Item",
    filters={"parent": grn_no},
    fields=["item_code", "item_name", "qty", "serial_no"]
)
    for item in item_details:
        if item.serial_no:
            serial_numbers = item.serial_no.split('\n')
            for serial in serial_numbers:
                serial_list.append({
                    "item_code":item.item_code,
                    "qty":item.qty,
                    "serial_no":serial,
                    "item_name":item.item_name
                })
        
                
            
        
    frappe.response["message"] = serial_list