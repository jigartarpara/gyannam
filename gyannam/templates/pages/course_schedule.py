from __future__ import unicode_literals
import frappe

def get_context(context):
    context.no_cache = True
    context.show_sidebar = True
    if frappe.session.user == 'Administrator':
        course_schedule = frappe.get_list('Course Schedule', fields=['name', 'student_group', 'from_time', 'to_time', 'message_body'])
        context.course_schedule = course_schedule
    else:
        student = frappe.db.get_value("Student", {'student_email_id': frappe.session.user}, 'name')
        students_group_list = frappe.db.get_all("Student Group", filters = [["Student Group Student", "student", "=", student]])
        for schedule in students_group_list:
            course_schedule = frappe.get_list('Course Schedule', filters={'student_group': schedule.name}, fields=['name', 'student_group', 'from_time', 'to_time', 'message_body'])
        context.course_schedule = course_schedule


