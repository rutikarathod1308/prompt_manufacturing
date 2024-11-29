import frappe 

def serial_no_update(doc=None, serial_no=None):
    if doc.stock_entry_type == "Manufacture":
        item_dict = []
    
        # Collect non-finished items
        for item in doc.items:
            if item.is_finished_item == 0:
                item_dict.append({
                    "item_code": item.item_code,
                    "serial_no": item.serial_no,
                    "qty": item.qty,
                    "item_name": item.item_name
                })
        
        # Process finished items
        for item in doc.items:
            for d in item_dict:
                if item.is_finished_item:
                    # Ensure serial_no is not None or empty
                    if not item.serial_no:
                        frappe.msgprint(f"No serial number found for item {item.item_code}. Skipping.")
                        continue
                    
                    # Split serial numbers
                    serial_numbers = item.serial_no.split('\n')
                    for serial_no in serial_numbers:
                        # Fetch the Serial No document
                        try:
                            work = frappe.get_doc("Serial No", serial_no)
                        except frappe.DoesNotExistError:
                            frappe.msgprint(f"Serial No {serial_no} does not exist. Skipping.")
                            continue
                        
                        # Append to macustom_manufacturing_item_details table
                        work.append('custom_manufacturing_item_details', {
                            'item_code': d["item_code"],
                            'item_name': d["item_name"],
                            'qty': d["qty"],
                            'serial_no': d["serial_no"],
                            'manufacturing_used_date': doc.posting_date
                        })
                        work.save()

