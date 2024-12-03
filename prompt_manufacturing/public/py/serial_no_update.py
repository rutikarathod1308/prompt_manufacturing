import frappe 
import time
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


def qc_generate_submit(doc=None,method=None):
    time.sleep(2)
    for item in doc.items:
        
        serial_no = frappe.db.get_all(
            "Serial and Batch Entry",
            filters={"parent": item.serial_and_batch_bundle,},
            fields=["*"]
        )

        for serial in serial_no:
            # Check if Quality Inspection already exists
            existing_qi = frappe.db.exists(
                "Quality Inspection",
                {"reference_name": doc.name, "docstatus": ["!=", 2]}
            )
            
            if not existing_qi:
                # Create a new Quality Inspection draft
                qi_doc = frappe.get_doc({
                    "doctype": "Quality Inspection",
                    "inspection_type" : "Incoming",
                    "reference_type" :"Purchase Receipt",
                    "reference_name": doc.name,
                    "sample_size" : 0 ,
                    "item_code": item.item_code,
                    
                    "item_serial_no": serial.get("serial_no"),
                    "status": "Accepted",
                    "inspected_by":"Administrator"
                    # Add any additional fields required for Quality Inspection
                })
                qi_doc.insert(ignore_permissions=True)  # Insert as draft
                