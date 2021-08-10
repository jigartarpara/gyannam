import frappe
from frappe.utils.background_jobs import enqueue
import datetime


def send_email_before_day():
    scheduled_course = frappe.db.get_list('Course Schedule', filters= {'schedule_date': ['=', frappe.utils.nowdate()]}, fields=['name','student_group'])
    for course in scheduled_course:
        send_course_alert(course)

def schedule_alert():
    start_time = frappe.utils.now()
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
    scheduled_course = frappe.db.get_list('Course Schedule', filters= {'schedule_date': ['between', [start_time, end_time]], 'reminder_sent': ["!=", 1]}, fields=['name','student_group','from_time', 'to_time'])
    for course in scheduled_course:
        send_course_alert(course)
        frappe.db.set_value("Course Schedule", course.name, 'reminder_sent', 1)
        frappe.db.commit()
        
        

def send_course_alert(course):
    students_list = frappe.db.get_list("Student Group Student", filters = {'parent': course.student_group}, fields=['student'])
    receiver_list = []
    for student in students_list:
        students_email_id = frappe.db.get_value('Student', student.student, 'student_email_id')
        if students_email_id not in receiver_list:
            receiver_list.append(students_email_id)

    if receiver_list:
        doc = frappe.get_doc("Course Schedule", course.name)
        email_args = {
            "recipients": receiver_list,
            "sender": None,
            "message": """<html><body><h3>Live Class Alert</h3>
                    {5}
                    Class - {0}<br>
                    Teacher Name - {1}<br>
                    Date - {2}<br>
                    From - {3}<br>
                    To - {4}<br>
                    <br></body></html>""".format(doc.course, doc.instructor_name, doc.schedule_date, doc.from_time, doc.to_time, doc.message_body),
            "subject": 'Scheduled class on {0}'.format(doc.schedule_date),
            "reference_doctype": doc.doctype,
            "reference_name": doc.name
        }
        enqueue(method=frappe.sendmail, queue='short',timeout=300, is_async=True, **email_args)
    else:
        frappe.msgprint("No Recipients found")

def has_website_permission(doc, ptype, user, verbose=Fals):
    if doc.student_group == get_student():
		return True
	else:
		return False

def get_student():
    student = frappe.db.get_value("Student", {'student_email_id': frappe.session.user})
    if student:
        return frappe.db.get_value("Student Group Student", filters = {'student': student}, fields=['parent'])