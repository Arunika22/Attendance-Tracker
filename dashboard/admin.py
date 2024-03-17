from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser,AdminHOD,Faculty,Students,Subject,Attendance,Attendance_Report,SessionYearModel

class UserModel(UserAdmin) :
    pass

admin.site.register(CustomUser, UserModel)
 
admin.site.register(AdminHOD)
admin.site.register(Faculty)

admin.site.register(Students)
admin.site.register(SessionYearModel)

admin.site.register(Subject)

admin.site.register(Attendance)
admin.site.register(Attendance_Report)

