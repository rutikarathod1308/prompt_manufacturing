import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, get_number_format_info


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def item_query(doctype, txt, searchfield, start, page_len, filters):
	from frappe.desk.reportview import get_match_cond # type: ignore

	from_doctype = cstr(filters.get("from"))
	if not from_doctype or not frappe.db.exists("DocType", from_doctype):
		return []

	mcond = get_match_cond(from_doctype)
	cond, qi_condition = "", "and (quality_inspection is null or quality_inspection = '')"

	if filters.get("parent"):
		if (
			from_doctype in ["Purchase Invoice Item", "Purchase Receipt Item"]
			and filters.get("inspection_type") != "In Process"
		):
			cond = """and item_code in (select name from `tabItem` where
				inspection_required_before_purchase = 1)"""
		elif (
			from_doctype in ["Sales Invoice Item", "Delivery Note Item"]
			and filters.get("inspection_type") != "In Process"
		):
			cond = """and item_code in (select name from `tabItem` where
				inspection_required_before_delivery = 1)"""
		elif from_doctype == "Stock Entry Detail":
			cond = """and s_warehouse is null"""

		if from_doctype in ["Supplier Quotation Item"]:
			qi_condition = ""

		return frappe.db.sql(
			f"""
				SELECT item_code
				FROM `tab{from_doctype}`
				WHERE parent=%(parent)s and docstatus < 2 and item_code like %(txt)s
				{qi_condition} 
			""",
			{"parent": filters.get("parent"), "txt": "%%%s%%" % txt},
		)

	elif filters.get("reference_name"):
		return frappe.db.sql(
			f"""
				SELECT production_item
				FROM `tab{from_doctype}`
				WHERE name = %(reference_name)s and docstatus < 2 and production_item like %(txt)s
				{qi_condition} 
			""",
			{"reference_name": filters.get("reference_name"), "txt": "%%%s%%" % txt},
		)

