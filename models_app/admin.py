from django.contrib import admin
from models_app.models import User,Subjects,Attendance


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','user_type']
    list_filter = ['user_type']
    search_fields = ['email']
    
admin.site.register(User,UserAdmin)

class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['id','name','section']
    list_filter = ['code','name']
    search_fields = ['name']

admin.site.register(Subjects,SubjectsAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id','student_id','faculty_id','subject_id','date']
    list_filter = ['subject_id',]
    search_fields = ['student_id']

admin.site.register(Attendance,AttendanceAdmin)


# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ['id','name']

# admin.site.register(Department,DepartmentAdmin)

# class BranchAdmin(admin.ModelAdmin):
#     list_display = ['id','name','department']

# admin.site.register(Branch,BranchAdmin)

# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ['id','name','branch','subject_code']

# admin.site.register(Subject,SubjectAdmin)

# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ['id','student','faculty','subject','status','date']

# admin.site.register(Attendance,AttendanceAdmin)