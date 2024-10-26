from django.shortcuts import render,redirect
from counselor_app.models import Manager, Counselor
from django.db import connection
from django.conf import settings
from django.contrib import messages


# Create your views here.

def counselor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id')
        print(email, employee_id)  # For debugging; consider removing in production
        
        with connection.cursor() as cur:
            query = "SELECT id FROM counselor_app_counselor WHERE email = %s AND employee_id = %s"
            cur.execute(query, [email, employee_id])
            counselor_data = cur.fetchone()
            
        if counselor_data:
            request.session['counselor_id'] = counselor_data[0]  # Store the actual ID
            return redirect('counselor_dashboard_page')
        else:
            error = "Invalid Email or Employee ID!"
            return render(request, 'counselor/counselor_login.html', {'error': error})

    return render(request, 'counselor/counselor_login.html')

def counselor_dashboard_page(request):
    counselor_id = request.session.get('counselor_id')
    if not counselor_id:
        return render(request,'counselor_login.html')
    with connection.cursor() as cur:
        query = "SELECT name,email FROM counselor_app_counselor WHERE id = %s"
        cur.execute(query,[counselor_id])
        counselor_data = cur.fetchone()
    if counselor_data:
        counselor_details={
            "counselor_name":counselor_data[0],
            "counselor_email":counselor_data[1],
            
        }
    return render(request,'counselor/counselor_dashboard.html',{'counselor_details':counselor_details}) 
def counselor_logout(request):
    counselor_id = request.session.get('counselor_id')
    if counselor_id:
        request.session.pop(counselor_id,None)
        messages.success(request,"Successfully loggout!")
        return redirect('counselor_login')

# def enroll_students(request):
#     if 

def manager_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id')
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

        counselor_query = "SELECT name, email FROM counselor_app_counselor WHERE manager_id = %s"
        cur.execute(counselor_query,[manager_id])
        
        counselor_data = cur.fetchall()
        
    if manager_data:
        manager_details={
            "manager_name":manager_data[0],
            "manager_email":manager_data[1],
            "manager_empid":manager_data[2]
        }
    counselor_list = [{"name": counselor[0], "email": counselor[1]} for counselor in counselor_data]
    return render(request,'manager/manager_dashboard.html',
        {'manager_details':manager_details,
        'counselor_list': counselor_list}
        )

def add_role(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return render(request,'manager/manager_login.html')

    if request.method == 'POST':
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id')
        role_type = request.POST.get('role_type')

        with connection.cursor() as cur:
            if role_type == "counselor":
                #insert query
                pass

            elif role_type == "python_analyst":
                pass

            elif role_type == "java_analyst":
                pass

            elif role_type == "analyst":
                pass
            elif role_type == "developer":
                pass
            elif role_type == "trainer":
                pass


    return render(request,'manager/add_role.html')

def manager_logout(request):
    manager_id = request.session.get('manager_id')
    if manager_id:
        request.session.pop(manager_id,None)
        messages.success(request,"Successfully loggout!")
        return redirect('manager_login')