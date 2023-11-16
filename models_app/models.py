from django.db import models
from django.contrib.auth.models import AbstractUser
from models_app.manager import UserManager



class User(AbstractUser):
    section_choices = [
        ('IT-1','IT-1'),
        ('IT-2','IT-2'),
        ('IOT','IOT'),
        ('DS','DS'),
    ]
    
    year_choices = [
        ('I','I'),
        ('II','II'),
        ('III','III'),
        ('IV','IV'),
    ]
    
    user_type_choices = [
        ('Student','Student'),
        ('Faculty','Faculty'),
        ('HOD','HOD'),
    ]
    username = None
    enrollment_number = models.CharField(max_length=15,blank=True,null=True,unique=True)
    first_name = models.CharField(max_length=20, blank=False,null=False)
    last_name = models.CharField( max_length=20, blank=False,null=False)
    section = models.CharField(max_length=20,choices=section_choices,blank=True,null=True)
    year = models.CharField(max_length=20,choices=year_choices,blank=True,null=True)
    email = models.EmailField(blank=False,null=False,unique=True)
    user_type = models.CharField(max_length=20,default='Student',null=False, blank=False)
    login_otp = models.CharField(max_length=6,null=True,blank=True)
    is_deleted = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
    

    def __str__(self) -> str:
        return f'{self.id},{self.email}'


class Subjects(models.Model):
    section_choices = [
        ('IT-1','IT-1'),
        ('IT-2','IT-2'),
        ('IOT','IOT'),
        ('DS','DS'),
    ]
    name = models.CharField(max_length=50,null=False,blank=False)
    code = models.CharField(max_length=10,null=False,blank=False)
    section = models.CharField(max_length=20,choices=section_choices,blank=False,null=False)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.id},{self.name},{self.section}'


class Attendance(models.Model):
    student_id = models.ForeignKey(User,related_name='student',on_delete = models.SET_NULL,null=True,blank=True)
    faculty_id = models.ForeignKey(User,related_name='faculty',on_delete = models.SET_NULL,null=True,blank=True)
    subject_id = models.ForeignKey(Subjects,on_delete = models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(null=False,blank=False)
    time = models.TimeField(null=False,blank=False)
    section_choices = [
        ('IT-1','IT-1'),
        ('IT-2','IT-2'),
        ('IOT','IOT'),
        ('DS','DS'),
    ]
    year_choices = [
        ('I','I'),
        ('II','II'),
        ('III','III'),
        ('IV','IV'),
    ]
    section = models.CharField(max_length=20,choices=section_choices,blank=True,null=True)
    year = models.CharField(max_length=20,choices=year_choices,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.id}'


# class User(AbstractUser):
#     ROLES = [
#         ('student', 'Student'),
#         ('teacher', 'Teacher'),
#         ('hod', 'Head of Department'),
#         ('admin', 'Administrator'),
#     ]
#     USER_TYPE_CHOICES = [
#         ('A','A'),
#         ('B','B'),
#         ('C','C'),
#         ('D','D'),
#         ('E','E')
#     ]
#     YEARS = [
#         ('1','1'),
#         ('2','2'),
#         ('3','3'),
#         ('4','4'),
#     ]
#     SEMESTERS = [
#         ('1','1'),
#         ('2','2'),
#         ('3','3'),
#         ('4','4'),
#         ('5','5'),
#         ('6','6'),
#         ('7','7'),
#         ('8','8')
#     ]
#     role = models.CharField(max_length=20, choices=ROLES,null=False,blank=False)
#     user_type = models.CharField(max_length=5,choices=USER_TYPE_CHOICES,default="A")
#     name = models.CharField(max_length=255,null=False,blank=False)
#     contact_number = models.CharField(max_length=13,null=False,blank=False)
#     enrollment_number = models.CharField(max_length=20,null=True,blank=True)
#     department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE,null=True,blank=True)
#     year = models.CharField(max_length=10,choices=YEARS,null=True,blank=True)
#     semester = models.CharField(max_length=10,choices=SEMESTERS,null=True,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     USERNAME_FIELD = 'username'
#     EMAIL_FIELD = "email"
#     REQUIRED_FIELDS = ["email"]
#     objects = UserManager()


#     def __str__(self) -> str:
#         return f'{self.id},{self.username}'


# class Attendance(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False,related_name='attendance_records_as_student')
#     faculty = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,related_name='attendance_records_as_faculty')
#     subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=False,blank=False)
#     branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False,blank=False)
#     date = models.DateField()
#     status_choice = (
#         ('Present','Present'),
#         ('Absent','Absent'),
#         ('Leave','Leave')
#     )
#     status = models.CharField(max_length=10,choices=status_choice,null=False,blank=False)
    
