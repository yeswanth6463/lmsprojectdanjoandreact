# Generated by Django 5.2.1 on 2025-06-03 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_student_dept_no_teacher_dept_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='dept_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
