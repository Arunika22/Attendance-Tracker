from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()

class CustomUser(AbstractUser):
    HOD = '1'
    FACULTY = '2'
    STUDENT = '3'

    EMAIL_TO_USER_TYPE_MAP = {
        'hod': HOD,
        'faculty': FACULTY,
        'student': STUDENT
    }

    user_type_data = ((HOD, "HOD"), (FACULTY, "Faculty"), (STUDENT, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

    # groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    # user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')



class AdminHOD(models.Model):
    
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='admin_hod')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Faculty(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True,related_name='faculty_profile')
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    # def __str__(self) :
    #     return self.admin.username
    

class Students(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='student_profile')
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    session_year_id = models.ForeignKey(SessionYearModel, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Subject(models.Model) :
    id = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=50)
    faculty_id =models.ForeignKey(CustomUser,on_delete =models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Attendance(models.Model) :

    id = models.AutoField(primary_key=True)
    sub_id = models.ForeignKey(Subject,on_delete = models.DO_NOTHING)
    attendance_date =models.DateField()
    session_id = models.ForeignKey(SessionYearModel,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Attendance_Report(models.Model) :
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
 



def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
       
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Faculty.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance,
                                    
                                    session_year_id=SessionYearModel.objects.get(id=1),
                                    address="",
                                    profile_pic="",
                                    gender="")
            
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin_hod.save()
    elif instance.user_type == 2:
        instance.faculty_profile.save()
    elif instance.user_type == 3:
        instance.student_profile.save()

