# Generated by Django 5.2.1 on 2025-06-04 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_academicyear_department_semester_remove_student_year_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course_category',
            name='description',
        ),
    ]
