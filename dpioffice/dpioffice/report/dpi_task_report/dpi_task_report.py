from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    columns, data = [], []
    columns = get_colums()
    validate_filters(filters)
    data = get_data(filters)

    return columns, data

def validate_filters(filters):
	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date must be before To Date"))

def get_colums():
	columns = ["Task:Link/Task:81"]+["Subject:Data:250"]+["Project:Link/Project:120"]\
		+["Status:Data:60"]+["Priority:Data:60"]+["Assigned to:Data:105"]\
		+["Creadted by:Data:105"]+["Exp Start Date:Date:90"]\
		+["Exp End Date:Date:90"]+["Created On:Date:90"]\
		+["Last Modified On:Date:90"]+["Last Modified by:Data:105"]\
		+["Review Date:Date:100"]+["Closing Date:Date:100"]
	return columns



def get_data(filters):
	sql_query = """select 
						name ,
						subject,
						project,
						status,
						priority,
						case when assigned_to IS NOT NULL then (select full_name from tabUser u where u.name=t.assigned_to) end as "assigned_to",
						case when owner IS NOT NULL then (select full_name from tabUser u where u.name=t.owner) end as "created_by",
						exp_start_date,
						exp_end_date,
						creation,modified,
						case when modified_by IS NOT NULL then (select full_name from tabUser u where u.name=t.modified_by) end as "modified_by",
						review_date,
						closing_date
					FROM
						tabTask t """

	sql_query += """ where (modified between '{0}' and '{1}')""".format(filters.get("from_date"),filters.get("to_date"))
	if filters.get("owner") and filters.get("assigned_to"):
		sql_query += " and t.owner = '{0}' and assigned_to = '{1}' """.format(filters.get("owner"),filters.get("assigned_to"))
	
	elif filters.get("assigned_to"):
		sql_query += " and assigned_to = '{0}'""".format(filters.get("assigned_to"))
	elif filters.get("owner"):
		sql_query += " and t.owner = '{0}'""".format(filters.get("owner"))

	sql_query += " order by modified desc"
	dl = frappe.db.sql(sql_query,as_list=1,debug=1)
	return dl


# FROM
#   tabTask t order by modified desc;
    # if filters.get("exp_start_date"):
    #     dl = frappe.db.sql("""select subject,status,project,priority,exp_start_date,
    #         exp_end_date,owner from tabTask
    #         where exp_start_date >=0'
    #         """)
            # ORDER BY modified desc""".format(filters.get('date'),
            # filters.get("from_date"),filters.get("to_date"),as_list=1,debug=1))
    # else:
    #     dl = frappe.db.sql("""select subject,status,project,priority,exp_start_date,
    #         exp_end_date,owner from tabTask
    #         where (exp_end_date between '{0}' 
    #         and '{1}') """.format(filters.get("from_date"),filters.get("to_date"),as_list=1,debug=1))
    # dl = frappe.db.sql(query,as_list=1,debug=1)

