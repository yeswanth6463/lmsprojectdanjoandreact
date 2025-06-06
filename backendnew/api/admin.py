from django.contrib import admin
from .models import University,student,teacher,course,course_category,Common_user,course_video,Chapter,courseenrollement,Quiz,QuizResult,Certificate,Superadmin,Attendance,LMSActivity,payment,course_material,Certificate_template,CourseAssignment,Semester,AcademicYear,Department,course_textcontent
# Register your models here.
admin.site.register(University)
admin.site.register(student)
admin.site.register(teacher)
admin.site.register(course_category)
admin.site.register(course)
admin.site.register(Chapter)
admin.site.register(course_video)
admin.site.register(Common_user)
admin.site.register(courseenrollement)
admin.site.register(Quiz)
admin.site.register(QuizResult)
admin.site.register(Certificate)
admin.site.register(Superadmin)
admin.site.register(Attendance)
admin.site.register(LMSActivity)
admin.site.register(payment)
admin.site.register(course_material)
admin.site.register(Certificate_template)
admin.site.register(AcademicYear)
admin.site.register(Semester)
admin.site.register(CourseAssignment)
admin.site.register(Department)
admin.site.register(course_textcontent)










#how to change site icon'








# how to deeign the admin panel
# admin.site.index_template = "admin/index.html"
# admin.site.index_template = "admin/index.html"
admin.site.index_template = "admin/index.html"








