from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import datetime




from django.shortcuts import render,redirect,get_object_or_404

from .models import CustomUser, Students, Attendance_Report, Subject
from django.contrib.auth.decorators import login_required

def student_home(request):
    
    # stud_obj = Students.objects.get(admin=request.user.id)
    # print("Entering student_home view")
    # print("User Type:", request.user.user_type)
    # print("Student Object:", stud_obj)
    # total_attendance = Attendance_Report.objects.filter(student_id=stud_obj).count()
    # attendance_present = Attendance_Report.objects.filter(student_id=stud_obj, status=True).count()
    # attendance_absent = Attendance_Report.objects.filter(student_id=stud_obj, status=False).count()

    # total_subjects = Subject.objects.count()
    # subject_name = []
    # data_present = []
    # data_absent = []

    # subject_data = Subject.objects.all()
    # for subject in subject_data:
    #     attendance = Attendance_Report.objects.filter(subject_id=subject.id, student_id=stud_obj)
    #     attendance_present_count = attendance.filter(status=True).count()
    #     attendance_absent_count = attendance.filter(status=False).count()

    #     subject_name.append(subject.subject_name)
    #     data_present.append(attendance_present_count)
    #     data_absent.append(attendance_absent_count)
    username = request.user.first_name

    context = {
        'username': username,
    }
    # context = {
    #         "username" = username,
    # #     "total_attendance": total_attendance,
    #     "attendance_present": attendance_present,
    #     "attendance_absent": attendance_absent,
    #     "total_subjects": total_subjects,
    #     "subject_name": subject_name,
    #     "data_present": data_present,
    #     "data_absent": data_absent
    
    return render(request, "Student_templates/index_student.html", context)
def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
 
    context={
        "user": user,
        "student": student
    }
    return render(request, 'Student_templates/student_profile.html', context)

def student_profile_update(request) :
    if request.method != 'POST' :
        messages.error("Invalid operation")
    else :
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')
 
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
 
            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
             
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')