from django.shortcuts import render,redirect
from counselor_app.models import Manager, Counselor, Role
from django.db import connection
from django.conf import settings
from django.contrib import messages
import datetime


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
    else:
        if employee_data is None:
            msg = "No Employee Data!!"
            return render(request,'employee/employee_dashboard.html',{'msg':msg})
    return render(request,'employee/employee_dashboard.html',{'employee_details':employee_details}) 
def employee_logout(request):
    emp_id = request.session.get('emp_role_id')
    if emp_id:
        request.session.pop(emp_id,None)
        messages.success(request,"Successfully loggout!")
        return redirect('employee_login')

# def enroll_students(request):
#     if 

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

        employee_query = "SELECT name, email,role_type FROM counselor_app_role WHERE manager_id = %s"
        cur.execute(employee_query,[manager_id])
        
        employee_data = cur.fetchall()
        
    if manager_data:
        manager_details={
            "manager_name":manager_data[0],
            "manager_email":manager_data[1],
            "manager_empid":manager_data[2]
        }
    employee_list = [{"name": employee[0], "email": employee[1]} for employee in employee_data]
    return render(request,'manager/manager_dashboard.html',
        {'manager_details':manager_details,
        'employee_list': employee_list}
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
        employee_list = [{"name": employee[0], "email": employee[1], "employee_id":employee[2],"role_type":employee[3]} for employee in employee_data]
        print(employee_list)
        return render(request,'manager/view_team.html',
        {'manager_details':manager_details,
        'employee_list': employee_list}
        )

    # return render(request,'manager/view_team.html')

def manager_logout(request):
    manager_id = request.session.get('manager_id')
    if manager_id:
        request.session.pop(manager_id,None)
        messages.success(request,"Successfully loggout!")
        return redirect('manager_login')