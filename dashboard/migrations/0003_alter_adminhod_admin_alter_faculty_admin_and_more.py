# Generated by Django 4.2.10 on 2024-03-02 04:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0002_remove_adminhod_id_remove_faculty_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adminhod",
            name="admin",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="admin_hod",
                serialize=False,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="admin",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="faculty_profile",
                serialize=False,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="students",
            name="admin",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="student_profile",
                serialize=False,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
