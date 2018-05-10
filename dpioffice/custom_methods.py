import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import throw, _
from frappe.model.naming import make_autoname
from datetime import datetime

@frappe.whitelist()
def set_task_autoname(doc, method):
	frappe.msgprint("testhello")
	project_abbr = frappe.db.get_value("Project",doc.project,"abbr")
	if project_abbr:
		now = datetime.now()
		doc.name =make_autoname("TASK-" + project_abbr +"-"+ str(now.month) +"-"+ str(now.year) + '-.#####')
	else:
		doc.name = make_autoname("TASK" + '.#####')
 

