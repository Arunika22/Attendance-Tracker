from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser,  AdminHOD, Faculty, Students

from django.contrib.auth.hashers import check_password

from django.contrib import messages

# Create your views here.

def home(request) :
    return render(request,'home.html')

def login_user(request) :
    return render(request,'login_user.html')



def dologin(request) :
    print("here")
    email_id  = request.POST.get('email')
    password = request.POST.get('password')
    user_type = request.POST.get('usertype')
    print(email_id)
    print(password)
    print(user_type)
    print(request.user)
    if not ( email_id and password and user_type) :
        messages.error(request,"Please provide complete details") 
        return render(request,"login_user.html")
    


    user = CustomUser.objects.filter(email=email_id, password=password,user_type = user_type).last()

    
    
    print(request.user)

    if not user :
        messages.error(request,"Invalid credintials,User does not exist !!")
        return render(request,"login_user.html")
    
    login(request,user)
    print(request.user)

    if user.user_type == CustomUser.STUDENT or user_type.lower() == 'student': 
        return redirect('student_home/')
    elif user.user_type == CustomUser.FACULTY or user_type.lower() == 'faculty'  :
        return redirect('faculty_home/')    
    elif user.user_type == CustomUser.HOD or user_type.lower() == 'hod' :
        return redirect('hod_home/')

    return render(request,'home.html')

def sign_up(request) :
    return render(request,'sign_up.html')


def doSignup(request) :
    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email_id = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")
        confirm_password = request.POST.get("confirmPassword")
        print(email_id)
        print(password)
        print(user_type)
        print(confirm_password)
        print(first_name)
        print(last_name)
        if not ( email_id and password and confirm_password) :
            messages.error(request,"Please provide complete details") 
            return render(request,"sign_up.html")
            
        if password != confirm_password :
            messages.error(request,"Password mismatch")
            return render(request,'sign_up.html')
            

        user_exists = CustomUser.objects.filter(email = email_id).exists()

        if user_exists :
            messages.error(request, "Please use valid format for the email id")
            return render(request, 'sign_up.html')
        # user_type = get_user_type_from_email(email_id)
        
        # if user_type is None:
        #     messages.error(request, "Please use valid format for the email id: '<username>.<staff|student|hod>@<college_domain>'")
        #     return render(request, 'sign_up.html')
        username = email_id.split('@')[0]

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'User with this username already exists. Please use different username')
            return render(request, 'sign_up.html')
            
        user = CustomUser()
        user.username = username
        user.email = email_id
        user.password = password
        user.user_type = user_type
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        if user_type == CustomUser.FACULTY:
            Faculty.objects.create(admin=user)
        elif user_type == CustomUser.STUDENT:
            Students.objects.create(admin=user)
        elif user_type == CustomUser.HOD:
            AdminHOD.objects.create(admin=user)
        return render(request, 'login_user.html')
        
     
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
 

        
    
    
