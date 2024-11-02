from django.shortcuts import render,redirect,HttpResponse
from counselor_app.models import Manager, Counselor, Role
from django.db import connection
from django.conf import settings
from django.contrib import messages
import datetime

def generate_enrollment_id(course_name, date):
    courses_data = {
        'Python Full Stack': 'KIHPY',
        'Java Full Stack': 'KIHJA',
        'Data Science': 'KIHDS',
        'Digital Marketing': 'KIHDM',
        'UI / UX': 'KIHUI'
    }

    data = courses_data.get(course_name, 'UNKNOWN')
    date_str = date.strftime("%d%m%Y")

    with connection.cursor() as cur:
        # Use DATE() function in MySQL to get the date part
        sequence_query = "SELECT COUNT(*) FROM counselor_app_studentenrollment WHERE course_name = %s AND DATE(enrolled_on) = %s"
        cur.execute(sequence_query, [course_name, date.date()])
        count = cur.fetchone()[0]

    sequential_number = count + 1
    enrollment_id = f"{data}{date_str}{sequential_number:04d}"
    return enrollment_id



# Create your views here.

def employee_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id').upper()
        print(email, employee_id)  # For debugging; consider removing in production
        
        with connection.cursor() as cur:
            query = "SELECT id FROM counselor_app_role WHERE email = %s AND employee_id = %s"
            cur.execute(query, [email, employee_id])
            employee_data = cur.fetchone()
            
        if employee_data:
            request.session['emp_role_id'] = employee_data[0]  # Store the actual ID
            return redirect('employee_dashboard_page')
        else:
            error = "Invalid Email or Employee ID!"
            return render(request, 'employee/employee_login.html', {'error': error})

    return render(request, 'employee/employee_login.html')

def employee_dashboard_page(request):
    emp_id = request.session.get('emp_role_id')
    if not emp_id:
        return render(request,'employee/employee_login.html')
    with connection.cursor() as cur:
        query = "SELECT name,email FROM counselor_app_role WHERE id = %s"
        cur.execute(query,[emp_id])
        employee_data = cur.fetchone()
    if employee_data:
        employee_details={
            "employee_name":employee_data[0],
            "employee_email":employee_data[1],
            
        }
        with connection.cursor() as cur:
            student_query = """
                    SELECT id,first_name, last_name, email, mobile, course_name, enrolled_on 
                    FROM counselor_app_studentenrollment 
                    WHERE counselor_id = %s
                """
            cur.execute(student_query, [emp_id])
            enrolled_students = cur.fetchall()
            

            student_enrollment_details = []
            for student in enrolled_students:
                student_enrollment_details.append({
                    "id": student[0],
                    "first_name": student[1],
                    "last_name": student[2],
                    "email": student[3],
                    "mobile": student[4],
                    "course_name": student[5],
                    "enrolled_on": student[6],
                })

        enrolled_student_count = len(student_enrollment_details)
                
        final_data = {
                'employee_details': employee_details,
                'student_enrollment_details': student_enrollment_details,
                'enrolled_student_count': enrolled_student_count
            }
        
    
    return render(request,'employee/employee_dashboard.html',final_data) 



def employee_logout(request):
    emp_id = request.session.get('emp_role_id')
    if emp_id:
        request.session.pop(emp_id,None)
        messages.success(request,"Successfully loggout!")
        return redirect('employee_login')



def manager_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id').upper()
        print(email, employee_id)  # For debugging; consider removing in production
        
        with connection.cursor() as cur:
            query = "SELECT id FROM counselor_app_manager WHERE email = %s AND employee_id = %s"
            cur.execute(query, [email, employee_id])
            manager_data = cur.fetchone()
            print(manager_data)  # For debugging; consider removing in production
            
        if manager_data:
            request.session['manager_id'] = manager_data[0]  # Store the actual ID
            return redirect('manager_dashboard_page')
        else:
            error = "Invalid Email or Employee ID!"
            return render(request, 'manager/manager_login.html', {'error': error})

    return render(request, 'manager/manager_login.html')

def manager_dashboard_page(request):
    manager_id = request.session.get('manager_id')
    print(manager_id)
    if not manager_id:
        return render(request,'manager/manager_login.html')

    with connection.cursor() as cur:
        manager_query = "SELECT name,email,employee_id FROM counselor_app_manager WHERE id = %s"
        cur.execute(manager_query,[manager_id])
        manager_data = cur.fetchone()

        # employee_query = "SELECT name, email,role_type FROM counselor_app_role WHERE manager_id = %s"
        # cur.execute(employee_query,[manager_id])
        
        # employee_data = cur.fetchall()
        
    if manager_data:
        manager_details={
            "manager_name":manager_data[0],
            "manager_email":manager_data[1],
            "manager_empid":manager_data[2]
        }if manager_data else {}

    with connection.cursor() as cur:
        employee_query = "SELECT name, email, role_type FROM counselor_app_role WHERE manager_id = %s"
        cur.execute(employee_query, [manager_id])
        employee_data = cur.fetchall()
    employee_list = [{"name": employee[0], "email": employee[1]} for employee in employee_data]

    with connection.cursor() as cur:
        student_query = """
        SELECT s.first_name, s.last_name, s.enrollment_id, s.email, s.mobile, s.enrolled_on, c.name
        FROM counselor_app_studentenrollment AS s
        JOIN counselor_app_role AS c ON s.counselor_id = c.id
        WHERE c.manager_id = %s AND c.role_type = 'counselor'
        """
        cur.execute(student_query, [manager_id])
        student_data = cur.fetchall()

    student_list = [{
        "s_no": sno + 1,
        "first_name": student[0],
        "last_name": student[1],
        "enrollment_id": student[2],
        "email": student[3],
        "mobile": student[4],
        "enrolled_on":student[5],
        "counselor_name": student[6]
    } for sno, student in enumerate(student_data)]
    student_enrolled_count = len(student_list)

    with connection.cursor() as cur:
        course_count_query = """
        SELECT c.name AS course_name, COUNT(s.enrollment_id) AS enrollment_count
    FROM counselor_app_studentenrollment AS s
    JOIN counselor_app_role AS c ON s.counselor_id = c.id
    WHERE c.manager_id = %s AND c.role_type = 'counselor'
    GROUP BY c.name
        """
        cur.execute(course_count_query, [manager_id])
        course_data = cur.fetchall()

    course_countss = {course[0]: course[1] for course in course_data}
    print(course_countss)
    # print(course_counts)

    course_counts = {
        "Python": 30,
        "JavaScript": 20,
        "Data Science": 15,
        "Digital Marketing": 10,
        "UI/UX": 5
    }

    course_labels = list(course_counts.keys())
    course_data = list(course_counts.values())

    

    return render(request,'manager/manager_dashboard.html',
        {'manager_details':manager_details,
        'employee_list': employee_list,
        'student_list': student_list,
        'student_enrolled_count': student_enrolled_count,
        'course_labels': course_labels,
        'course_data': course_data}
        )

def add_role(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('manager_login')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id').upper()
        role_type = request.POST.get('role_type')
        added_on = datetime.datetime.now()

        if not name or not email or not employee_id or not role_type:
            error = "All fields are required!"
            return render(request, 'manager/add_role.html', {'error': error})

        with connection.cursor() as cur:
            query = """
                INSERT INTO counselor_app_role 
                (manager_id, name, email, employee_id, role_type, added_on)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, [manager_id, name, email, employee_id, role_type, added_on])

        messages.success(request, "Successfully added role!")
        return redirect('manager_dashboard_page')

    return render(request, 'manager/add_role.html')

def view_team(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('manager_login')
    with connection.cursor() as cur:
        manager_query = "SELECT name,email,employee_id FROM counselor_app_manager WHERE id = %s"
        cur.execute(manager_query,[manager_id])
        manager_data = cur.fetchone()

        employee_query = "SELECT name, email,employee_id,role_type FROM counselor_app_role WHERE manager_id = %s"
        cur.execute(employee_query,[manager_id])
        
        employee_data = cur.fetchall()
    if manager_data:
        manager_details={
            "manager_name":manager_data[0],
            "manager_email":manager_data[1],
            "manager_empid":manager_data[2]
        }
        employee_list = [
        {
            "name": employee[0], 
            "email": employee[1], 
            "employee_id":employee[2],
            "role_type":employee[3]
        } 
        for employee in employee_data
        ]
        no_employee_data = not employee_list

        return render(request,'manager/view_team.html',
        {'manager_details':manager_details,
        'employee_list': employee_list,
        'no_employee_data': no_employee_data}
        )

    # return render(request,'manager/view_team.html')

def manager_logout(request):
    manager_id = request.session.get('manager_id')
    if manager_id:
        request.session.pop(manager_id,None)
        messages.success(request,"Successfully loggout!")
        return redirect('manager_login')


def add_enroll_students(request):
    emp_id = request.session.get('emp_role_id')
    if not emp_id:
        return render(request, 'employee/employee_login.html')

    if request.method == 'POST':
        # Extracting the POST data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        location = request.POST.get('location')
        mode_of_attending = request.POST.get('mode_of_attending')
        qualification = request.POST.get('qualification')
        branch = request.POST.get('branch')
        course_name = request.POST.get('course_name')
        course_amount = request.POST.get('course_amount')
        discount_amount = request.POST.get('discount_amount')
        total_amount = request.POST.get('total_amount')
        gender = request.POST.get('gender')
        education_status = request.POST.get('education_status')
        passed_year = request.POST.get('passed_year')
        marks = request.POST.get('marks')
        current_year = request.POST.get('current_year')
        enrolled_on = datetime.datetime.now()
        enrollment_id = generate_enrollment_id(course_name, enrolled_on)

        with connection.cursor() as cur:
            # Fetch manager ID
            manager_query = "SELECT manager_id FROM counselor_app_role WHERE id = %s"
            cur.execute(manager_query, [emp_id])
            manager_data = cur.fetchone()

        if manager_data:
            manager_id = manager_data[0]

            # Check if manager_id exists in counselor_app_manager
            with connection.cursor() as cur:
                check_manager_query = "SELECT id FROM counselor_app_manager WHERE id = %s"
                cur.execute(check_manager_query, [manager_id])
                if not cur.fetchone():
                    messages.error(request, "Manager ID does not exist in the manager table.")
                    return render(request, 'student/add_enroll_student.html')

            # Check for existing enrollment
            with connection.cursor() as cur:
                check_enrollment_query = """
                    SELECT c.name FROM counselor_app_studentenrollment se
                    JOIN counselor_app_role c ON se.counselor_id = c.id
                    WHERE se.email = %s AND se.mobile = %s AND se.course_name = %s
                """
                cur.execute(check_enrollment_query, [email, mobile, course_name])
                existing_enrollment = cur.fetchone()

                if existing_enrollment:
                    counselor_name = existing_enrollment[0]
                    messages.error(request, f"Student already enrolled by counselor: {counselor_name}.")
                    return render(request, 'student/add_enroll_student.html')

            # Check if the mobile number already exists in the student enrollment table
            with connection.cursor() as cur:
                check_mobile_query = "SELECT * FROM counselor_app_studentenrollment WHERE mobile = %s"
                cur.execute(check_mobile_query, [mobile])
                if cur.fetchone():
                    messages.error(request, "Mobile number already exists in the enrollment records.")
                    return render(request, 'student/add_enroll_student.html')

            # Insert student enrollment record
            with connection.cursor() as cur:
                student_query = """
                    INSERT INTO counselor_app_studentenrollment 
                    (first_name, last_name, email, mobile, location, mode_of_attending, qualification,
                        branch, course_name, course_amount, discount_amount, total_amount, gender,
                        education_status, passed_year, marks, current_year, enrolled_on, enrollment_id,
                        manager_id, counselor_id) VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(student_query, [
                    first_name, last_name, email, mobile, location, mode_of_attending,
                    qualification, branch, course_name, course_amount, discount_amount,
                    total_amount, gender, education_status, passed_year, marks,
                    current_year, enrolled_on, enrollment_id, manager_id, emp_id
                ])

            messages.success(request, "Student enrolled successfully!")
            return redirect('employee_dashboard_page')

        else:
            messages.error(request, "Manager ID not found.")
            return render(request, 'student/add_enroll_student.html')

    return render(request, 'student/add_enroll_student.html')

def edit_enrolled_student(request, student_id):
    emp_id = request.session.get('emp_role_id')
    if not emp_id:
        return redirect('employee_login')
    with connection.cursor() as cur:
        student_query = """
            SELECT id, first_name, last_name, email, mobile, location, mode_of_attending,
                   qualification, branch, course_name, course_amount, discount_amount,
                   total_amount, gender, education_status, passed_year, marks,
                   current_year, enrolled_on, enrollment_id, manager_id, counselor_id
            FROM counselor_app_studentenrollment
            WHERE id = %s
        """
        cur.execute(student_query, [student_id])
        student = cur.fetchone()

    if student:
        student_id, first_name, last_name, email, mobile, location, mode_of_attending, \
        qualification, branch, course_name, course_amount, discount_amount, total_amount, \
        gender, education_status, passed_year, marks, current_year, enrolled_on, \
        enrollment_id, manager_id, counselor_id = student

        if request.method == 'POST':
            updated_first_name = request.POST.get('first_name')
            updated_last_name = request.POST.get('last_name')
            updated_email = request.POST.get('email')
            updated_mobile = request.POST.get('mobile')
            updated_location = request.POST.get('location')
            updated_mode_of_attending = request.POST.get('mode_of_attending')
            updated_qualification = request.POST.get('qualification')
            updated_branch = request.POST.get('branch')
            updated_course_name = request.POST.get('course_name')
            updated_course_amount = request.POST.get('course_amount')
            updated_discount_amount = request.POST.get('discount_amount')
            updated_total_amount = request.POST.get('total_amount')
            updated_gender = request.POST.get('gender')
            updated_education_status = request.POST.get('education_status')
            updated_passed_year = request.POST.get('passed_year')
            updated_marks = request.POST.get('marks')
            updated_current_year = request.POST.get('current_year')

            # Update the student enrollment record
            update_query = """
                UPDATE counselor_app_studentenrollment
                SET first_name = %s, last_name = %s, email = %s, mobile = %s,
                    location = %s, mode_of_attending = %s, qualification = %s,
                    branch = %s, course_name = %s, course_amount = %s,
                    discount_amount = %s, total_amount = %s, gender = %s,
                    education_status = %s, passed_year = %s, marks = %s,
                    current_year = %s
                WHERE id = %s
            """
            with connection.cursor() as cur:
                cur.execute(update_query, [
                    updated_first_name, updated_last_name, updated_email, updated_mobile,
                    updated_location, updated_mode_of_attending, updated_qualification,
                    updated_branch, updated_course_name, updated_course_amount,
                    updated_discount_amount, updated_total_amount, updated_gender,
                    updated_education_status, updated_passed_year, updated_marks,
                    updated_current_year, student_id
                ])

            messages.success(request, "Student enrollment updated successfully!")
            return redirect('employee_dashboard_page')
        context = {
            'student': {
                'id': student_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'mobile': mobile,
                'location': location,
                'mode_of_attending': mode_of_attending,
                'qualification': qualification,
                'branch': branch,
                'course_name': course_name,
                'course_amount': course_amount,
                'discount_amount': discount_amount,
                'total_amount': total_amount,
                'gender': gender,
                'education_status': education_status,
                'passed_year': passed_year,
                'marks': marks,
                'current_year': current_year,
            },
            'employee_details': request.session.get('employee_details'),
        }
        print(context)
        return render(request, 'student/edit_enroll_student.html', context)

    messages.error(request, "Student not found.")
    return redirect('employee_dashboard_page')


def delete_enrolled_student(request, student_id):
    emp_id = request.session.get('emp_role_id')
    if not emp_id:
        return redirect('employee_login')
    with connection.cursor() as cur:
        delete_query="DELETE FROM counselor_app_studentenrollment WHERE id = %s"
        cur.execute(delete_query, [student_id])
    messages.success(request, "Student data deleted successfully!")
    return redirect('employee_dashboard_page')
    

def view_enrolled_student(request, student_id):
    emp_id = request.session.get('emp_role_id')
    if not emp_id:
        return redirect('employee_login')
    student_details = {}

    with connection.cursor() as cur:
        query ="""SELECT 
                first_name, last_name, email, course_name, branch,
                enrollment_id, location, mode_of_attending, qualification,
                course_amount, discount_amount, total_amount,
                gender, education_status, passed_year, marks, current_year,
                enrolled_on FROM counselor_app_studentenrollment WHERE id = %s"""
        cur.execute(query, [student_id])
        student_data=cur.fetchone()
        if student_data:
            student_details = {
                'first_name': student_data[0],
                'last_name': student_data[1],
                'email': student_data[2],
                'course_name': student_data[3],
                'branch': student_data[4],
                'enrollment_id': student_data[5],
                'location': student_data[6],
                'mode_of_attending': student_data[7],
                'qualification': student_data[8],
                'course_amount': student_data[9],
                'discount_amount': student_data[10],
                'total_amount': student_data[11],
                'gender': student_data[12],
                'education_status': student_data[13],
                'passed_year': student_data[14],
                'marks': student_data[15],
                'current_year': student_data[16],
                'enrolled_on': student_data[17],
            }
        return render(request, 'student/view_enrolled_student.html', {'student': student_details})
def payment_enrolled_student(request, student_id):
    return HttpResponse(request,student_id)