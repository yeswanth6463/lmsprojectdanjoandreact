# Generated by Django 5.2.1 on 2025-05-30 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course_video',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
