
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from .forms import AddStudentForm, EditStudentForm
from .models import CustomUser, Faculty, Subject, Students, SessionYearModel, Attendance, Attendance_Report

def hod_home(request):
    all_student_count = Students.objects.all().count()
    subject_count = Subject.objects.all().count()
    faculty_count = Faculty.objects.all().count()
    
    faculty_attendance_present_list = []
    faculty_name_list = []

    faculties = Faculty.objects.all()
    for faculty in faculties:
        subject_ids = Subject.objects.filter(faculty_id=faculty.admin.id)
        attendance = Attendance.objects.filter(sub_id__in=subject_ids).count()
        faculty_attendance_present_list.append(attendance)
        faculty_name_list.append(faculty.admin.first_name)

    student_attendance_present_list = []
    student_name_list = []

    students = Students.objects.all()
    for student in students:
        attendance = Attendance_Report.objects.filter(student_id=student.admin.id, status=True).count()
        student_attendance_present_list.append(attendance)
        student_name_list.append(student.admin.first_name)

    context = {
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "faculty_count": faculty_count,
        "faculty_name_list": faculty_name_list,
        "faculty_attendance_present_list": faculty_attendance_present_list,
        "student_name_list": student_name_list,
        "student_attendance_present_list": student_attendance_present_list,
    }

    return render(request, "HOD_templates/hod_home.html", context)

def add_faculty(request) :

    return render(request,"HOD_templates/add_faculty.html")



def save_faculty(request) :
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_faculty')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
 
        try:
            user = CustomUser.objects.create_user(username=username,
                                                  password=password,
                                                  email=email,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  user_type=2)
            user.faculty.address = address
            user.save()
            messages.success(request, "Faculty Added Successfully!")
            return redirect('add_faculty')
        except:
            messages.error(request, "Failed to Add faculty!")
            return redirect('add_faculty')
   
def manage_faculty(request):
    faculty= Faculty.objects.all()
    context = {
        "faculty": faculty
    }
    return render(request, "HOD_templates/manage_faculty.html", context)

def edit_faculty(request, faculty_id):
    faculty = Faculty.objects.get(admin=faculty_id)

    context = {
        "faculty": faculty,
        "id": faculty_id
    }
    return render(request, "HOD_templates/edit_faculty_template.html", context)

def edit_faculty_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        faculty_id = request.POST.get('faculty_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # Updating CustomUser Model
            user = CustomUser.objects.get(id=faculty_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # Updating Faculty Model
            faculty_model = Faculty.objects.get(admin=faculty_id)
            faculty_model.address = address
            faculty_model.save()

            messages.success(request, "Faculty Updated Successfully.")
            return redirect('/edit_faculty/' + faculty_id)

        except:
            messages.error(request, "Failed to Update Faculty.")
            return redirect('/edit_faculty/' + faculty_id)

def delete_faculty(request, faculty_id):
    try:
        faculty = Faculty.objects.get(admin=faculty_id)
        faculty.delete()
        messages.success(request, "Faculty Deleted Successfully.")
    except Faculty.DoesNotExist:
        messages.error(request, "Faculty not found.")
    except Exception as e:
        messages.error(request, f"Failed to delete faculty: {e}")
    
    return redirect('manage_faculty')


def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "HOD_templates/manage_session_template.html", context)
 
 
def add_session(request):
    return render(request, "HOD_templates/add_session_template.html")

def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "HOD_templates/edit_session_template.html", context)
 
 
def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')
 
        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()
 
            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/'+session_id)
 
 
def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')