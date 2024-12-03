import frappe

def qc_serial_no_update(doc=None,method=None):
    if doc.item_serial_no:
        frappe.db.set_value("Serial No",doc.item_serial_no,"custom_qc_check",1)
    
def qc_serial_no_cancel(doc=None,method=None):
    if doc.item_serial_no:
        frappe.db.set_value("Serial No",doc.item_serial_no,"custom_qc_check",0)