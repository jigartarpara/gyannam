from __future__ import unicode_literals
import frappe

def get_context(context):
    context.no_cache = True
    context.show_sidebar = True
    context.login_required = True
    if frappe.session.user == 'Administrator':
        course_schedule = frappe.get_list('Course Schedule', fields=['name', 'student_group', 'from_time', 'to_time', 'message_body'])
        context.course_schedule = course_schedule
    else:
        student = frappe.db.get_value("Student", {'student_email_id': frappe.session.user}, 'name')
        emp = frappe.db.get_value("Employee", {'prefered_email': frappe.session.user}, 'name')
        instructor = frappe.db.get_value("Instructor", {'employee': emp}, 'name')
        if student:
            students_group_list = frappe.db.get_all("Student Group", filters = [["Student Group Student", "student", "=", student]])
            group_list = []
            for group in students_group_list:
                group_list.append(group.name)
            course_schedule = frappe.get_list('Course Schedule', filters= [["Course Schedule",'student_group','in', group_list]], fields=['name', 'student_group', 'from_time', 'to_time', 'message_body'])
            context.course_schedule = course_schedule
        if instructor:
            instructor_group_list = frappe.db.get_all("Student Group", filters = [["Student Group Instructor", "instructor", "=", instructor]])
            group_list = []
            for group in instructor_group_list:
                group_list.append(group.name)
            course_schedule = frappe.get_list('Course Schedule', filters= [["Course Schedule",'student_group','in', group_list]], fields=['name', 'student_group', 'from_time', 'to_time', 'message_body'])
            context.course_schedule = course_schedule
