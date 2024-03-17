from django.contrib import admin
from django.urls import path,include

from .import views


from .import FacultyViews,HodViews,StudentViews

urlpatterns =[
    path('admin/',admin.site.urls,name ='admin'),
    path('',views.home,name = 'home'),
    path('login_user',views.login_user,name ='login_user'),
    path('logout_user',views.logout_user,name = 'logout_user'),
    path('sign_up', views.sign_up, name='sign_up'),
    
    path('dologin', views.dologin, name="dologin"),
    path('doSignup', views.doSignup, name="doSignup"),


    #student section
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
     path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),


    path('faculty_home/', FacultyViews.faculty_home, name="faculty_home"),
    path('faculty_profile/', FacultyViews.faculty_profile, name="faculty_profile"),
     path('faculty_profile_update/', FacultyViews.faculty_profile_update, name="faculty_profile_update"),


    #hod section
   
    path('hod_home/', HodViews.hod_home, name="hod_home"),
    path('add_faculty/', HodViews.add_faculty, name='add_faculty'),
    path('save_faculty/', HodViews.save_faculty, name="save_faculty"),
   
    path('manage_faculty/', HodViews.manage_faculty, name='manage_faculty'),
    path('edit_faculty', HodViews.edit_faculty, name="edit_faculty"),
    path('edit_faculty_save', HodViews.edit_faculty_save, name="edit_faculty_save"),
    path('delete_faculty', HodViews.delete_faculty, name="delete_faculty"),
    path(' manage_session', HodViews.manage_session, name="manage_session"),
    path('add_session', HodViews.add_session, name="add_session"),
    path('edit_session', HodViews.edit_session, name="edit_sessio"),
    path('delete_session', HodViews.delete_session, name="delete_session"),
 
      
]