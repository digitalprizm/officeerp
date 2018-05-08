import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import throw, _
from frappe.model.naming import make_autoname


@frappe.whitelist()
def set_task_autoname(doc, method):
	project_abbr = frappe.db.get_value("Project",doc.project,"abbr")
	if project_abbr:
		doc.name =make_autoname("TASK-"+project_abbr + '-.#####')
	else:
		doc.name = make_autoname("TASK" + '.#####')


