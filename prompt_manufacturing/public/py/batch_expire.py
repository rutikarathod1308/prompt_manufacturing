import frappe
from frappe.utils import add_months, nowdate, getdate

@frappe.whitelist()
def get_expiry_date():
    # Fetch the current date
    current_date = getdate(nowdate())
    
    # Calculate the date one month from today
    one_month_later = getdate(add_months(current_date, 1))
    
    # Fetch all batches with their expiry dates
    batch_value = frappe.db.get_all("Batch", fields=["name", "expiry_date"])
    
    # Initialize a list for batches expiring soon
    expiring_batches = []

    for batch in batch_value:
        if batch.get("expiry_date"):
            expiry_date = getdate(batch["expiry_date"])
            # Check if the expiry date is between current date and one month later
            if current_date <= expiry_date <= one_month_later:
                expiring_batches.append(batch["name"])
    
    # Count of expiring batches
    count = len(expiring_batches)
    
    # Prepare the response for the Number Card
    return {
        "value": count,
        "fieldtype": "Number",
        "route": "List/Batch",
        "route_options": {
            "expiry_date": ["between", [str(current_date), str(one_month_later)]]
        }
    }
