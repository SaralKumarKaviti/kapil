from django.db import models

# Create your models here.

class Manager(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=150, unique=True)
	employee_id = models.CharField(max_length=15,unique=True)

	def __str__(self):
		return self.name

class Counselor(models.Model):
	manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=150, unique=True)
	employee_id = models.CharField(max_length=15,unique=True)
	
	def __str__(self):
		return self.name

class Role(models.Model):
	manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=150, unique=True)
	employee_id = models.CharField(max_length=15,unique=True)
	role_type = models.CharField(max_length=50)
	added_on = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.name


# class EnrollStudents(models.Model):
#     COURSE_CHOICES = [
#         ('python_full_stack', 'Python Full Stack'),
#         ('java_full_stack', 'Java Full Stack'),
#         ('data_science', 'Data Science'),
#         ('aws', 'AWS Cloud'),
#         ('devops', 'Dev Ops'),
#         ('digital_marketing', 'Digital Marketing'),
#         ('ui_ux', 'UI / UX'),
#     ]
#     EDU_STATUS_CHOICES = [
#         ('passed_out', 'Passed Out'),
#         ('pursuing', 'Pursuing'),
#     ]
#     QUALIFICATIONS = [
#         ('inter', 'Intermediate'),
#         ('diploma', 'Diploma'),
#         ('degree', 'Degree'),
#         ('btech', 'Bachelor Technology'),
#         ('mtech', 'Master Technology'),
#     ]
    
#     counselor = models.ForeignKey('Counselor', on_delete=models.CASCADE)
#     manager = models.ForeignKey('Manager', on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=150, unique=True)
#     mobile = models.CharField(max_length=15, unique=True)
#     qualification = models.CharField(max_length=150, choices=QUALIFICATIONS)
#     course_name = models.CharField(max_length=50, choices=COURSE_CHOICES)
#     education_status = models.CharField(max_length=20, choices=EDU_STATUS_CHOICES)
#     branch = models.CharField(max_length=150)
#     course_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     created_on = models.DateTimeField(auto_now_add=True)
#     status = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} - {self.course_name}" 

