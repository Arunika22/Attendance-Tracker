from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from .models import CustomUser, Faculty, Students, SessionYearModel,Attendance_Report,Attendance,Subject

def faculty_home(request):
    username = request.user.first_name

    context = {
        'username': username,
    }
  
#     subjects = Subject.objects.filter(faculty_id=request.user.id)
    
#     subject_count = subjects.count()
#     print(subject_count)
    

#     # attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    
   
#     # faculty = Faculty.objects.get(admin=request.user.id)
    

#     # Fetch Attendance Data by Subjects
#     subject_list = []
#     attendance_list = []
#     for subject in subjects:
#         attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
#         subject_list.append(subject.subject_name)
#         attendance_list.append(attendance_count1)

#     # Fetch Students' Attendance Data
#     students_attendance = Students.objects.filter(subject_id__in=subjects)
#     student_list = []
#     student_list_attendance_present = []
#     student_list_attendance_absent = []
#     for student in students_attendance:
#         attendance_present_count = Attendance_Report.objects.filter(status=True,
#                                                                    student_id=student.id).count()
#         attendance_absent_count = Attendance_Report.objects.filter(status=False,
#                                                                   student_id=student.id).count()
#         student_list.append(student.admin.first_name + " " + student.admin.last_name)
#         student_list_attendance_present.append(attendance_present_count)
#         student_list_attendance_absent.append(attendance_absent_count)

#     context = {
#         "subject_count": subject_count,
#         "attendance_count": attendance_count,
       
#         "subject_list": subject_list,
#         "attendance_list": attendance_list,
#         "student_list": student_list,
#         "attendance_present_list": student_list_attendance_present,
#         "attendance_absent_list": student_list_attendance_absent
#     }
    return render(request, "Faculty_template/faculty_home.html",context)


 
def faculty_profile(request):
  

    return render(request, "Faculty_template/faculty_profile.html")


 
 
# def staff_take_attendance(request):
#     subjects = Subject.objects.filter(staff_id=request.user.id)
#     session_years = SessionYearModel.objects.all()
#     context = {
#         "subjects": subjects,
#         "session_years": session_years
#     }
    # return render(request, "Faculty_template/faculty_take_attendance", context)


# @csrf_exempt
# def get_attendance_dates(request):
     
 
#     # Getting Values from Ajax POST 'Fetch Student'
#     subject_id = request.POST.get("subject")
#     session_year = request.POST.get("session_year_id")
 
#     # Students enroll to Course, Course has Subjects
#     # Getting all data from subject model based on subject_id
#     subject_model = Subject.objects.get(id=subject_id)
 
#     session_model = SessionYearModel.objects.get(id=session_year)
#     attendance = Attendance.objects.filter(subject_id=subject_model,
#                                            session_year_id=session_model)
 
#     # Only Passing Student Id and Student Name Only
#     list_data = []
 
#     for attendance_single in attendance:
#         data_small={"id":attendance_single.id,
#                     "attendance_date":str(attendance_single.attendance_date),
#                     "session_year_id":attendance_single.session_year_id.id}
#         list_data.append(data_small)
 
#     return JsonResponse(json.dumps(list_data),
#                         content_type="application/json", safe=False)
 
 
# @csrf_exempt
# def get_attendance_student(request):
   
#     # Getting Values from Ajax POST 'Fetch Student'
#     attendance_date = request.POST.get('attendance_date')
#     attendance = Attendance.objects.get(id=attendance_date)
 
#     attendance_data = Attendance_Report.objects.filter(attendance_id=attendance)
#     # Only Passing Student Id and Student Name Only
#     list_data = []
 
#     for student in attendance_data:
#         data_small={"id":student.student_id.admin.id,
#                     "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
#         list_data.append(data_small)
 
#     return JsonResponse(json.dumps(list_data),
#                         content_type="application/json",
#                         safe=False)
 
 
# @csrf_exempt
# def update_attendance_data(request):
#     student_ids = request.POST.get("student_ids")
 
#     attendance_date = request.POST.get("attendance_date")
#     attendance = Attendance.objects.get(id=attendance_date)
 
#     json_student = json.loads(student_ids)
 
#     try:
         
#         for stud in json_student:
           
#             # Attendance of Individual Student saved on AttendanceReport Model
#             student = Students.objects.get(admin=stud['id'])
 
#             attendance_report = Attendance_Report.objects.get(student_id=student,
#                                                              attendance_id=attendance)
#             attendance_report.status=stud['status']
 
#             attendance_report.save()
#         return HttpResponse("OK")
#     except:
#         return HttpResponse("Error")
 
 
# def staff_profile(request):
#     user = CustomUser.objects.get(id=request.user.id)
#     faculty = Faculty.objects.get(admin=user)
 
#     context={
#         "user": user,
#         "faculty": faculty
#     }
#     return render(request, 'faculty_template/faculty_profile.html', context)
 
 
def faculty_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('faculty_profile')
    else:
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
 
            faculty = Faculty.objects.get(admin=customuser.id)
            faculty.address = address
            faculty.save()
 
            messages.success(request, "Profile Updated Successfully")
            return redirect('faculty_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('faculty_profile')
 