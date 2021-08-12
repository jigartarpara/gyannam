import frappe

@frappe.whitelist()
def has_website_permission(user, name):
    if user != 'Guest':
        student_group = frappe.db.get_value("Course Schedule", {'web_page': name}, 'student_group')
        if student_group:
            check_if_user_registerd(student_group,user)

def check_if_user_registerd(student_group, user):
    students = frappe.get_all("Student Group Student", filters={'parent': student_group}, fields=['student'])
    instructors = frappe.get_all("Student Group Instructor", filters={'parent': student_group}, fields=['instructor'])
    registered_user = []
    if students or instructors:
        for student in students:
            stu_email = frappe.db.get_value("Student", {'name':student.student}, 'student_email_id')
            if stu_email not in registered_user:
                registered_user.append(stu_email)
        for instructor in instructors:
            emp = frappe.db.get_value("Instructor", {'name': instructor}, 'employee')
            if emp:
                emp_email = frappe.db.get_value("Employee", {'name': emp}, 'prefered_email')
                if emp_email not in registered_user:
                    registered_user.append(emp_email)
    print(registered_user)
    if user in registered_user:
        return True
    else:
        frappe.throw("You are not permitted to access this class")
       