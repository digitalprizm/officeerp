# -*- coding: utf-8 -*-
# Copyright (c) 2017, DPI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from dpioffice.dpioffice.report.dpi_task_report.dpi_task_report import execute  
from frappe.utils import flt, time_diff_in_hours, get_datetime, getdate, today, cint, add_days 
from frappe import _


class TaskEmail(Document):
	def validate(self):
		self.send_now()

	def send_now(self):
		frappe.msgprint(self.email_id)
		email_list = self.email_id.split(",")
		for i in email_list:
			custom_filter = aa = {'from_date': add_days(today(), -7),'to_date': today(),'assigned_to':i}
			report = frappe.get_doc('Report', "DPI Task Report") 
			columns, data = report.get_data(limit=100 or 100, user = "sam@digitalprizm.net", filters = custom_filter, as_dict=True)
			columns.insert(0, frappe._dict(fieldname='idx', label='', width='30px'))
			k = 0
			for k in range(len(data)):
				data[k]['idx'] = k+1
			html = frappe.render_template('frappe/templates/includes/print_table.html', {'columns': columns,'data':data})  
			# frappe.msgprint(html)
			single_email_id = i
			self.send_emails(html,single_email_id)
	def send_emails(self,html,single_email_id):
		message = '<p>{0}</p>'.format(_('{0} generated on {1}')\
				.format(frappe.bold(self.subject),
					frappe.utils.format_datetime(frappe.utils.now_datetime())))

		message += '<hr style="margin: 15px 0px;">' + self.description
		message += '<hr>' + html
		frappe.msgprint(single_email_id)
		frappe.msgprint(message)
		# report_doctype = frappe.db.get_value('Report', self.report, 'ref_doctype')
		# report_footer = frappe.render_template(self.get_report_footer(),dict(report_url = frappe.utils.get_url_to_report("DPI Task Report", "Script Report", "Task"),report_name = "DPI Task Report"))

		frappe.sendmail(
			recipients = single_email_id,
			subject = self.subject,
			message = message,
			attachments = None
		)