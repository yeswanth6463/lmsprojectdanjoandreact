from django.db import models
from django.core import serializers
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Common_user(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=10)
    phone_number=models.BigIntegerField()
    university = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="1. common user"




class University(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="2.University"

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class teacher(models.Model):
    university = models.ForeignKey(University,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    qualification = models.CharField(max_length=100,null=True,blank=True)
    user_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')])
    dept_no = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

    def to_json(self):
        return serializers.serialize('json', [self])

class AcademicYear(models.Model):
    year = models.PositiveIntegerField()  # 1 = First Year, 2 = Second Year, etc.

    def __str__(self):
        return f"Year {self.year}"


class course_category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

    def to_json(self):
        return serializers.serialize('json', [self])

class course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(course_category, on_delete=models.CASCADE,null=True,blank=True)
    image = models.URLField(null=True,blank=True)
    total_chap = models.IntegerField()
    duration =models.IntegerField()
    price = models.IntegerField()
    background_image = models.URLField(null=True,blank=True)
    trending_course = models.BooleanField(default=False,null=True,blank=True)
    ratings= models.FloatField(default=4.0,blank=True,null=True)
    paid= models.BooleanField(default=False,null=True,blank=True)

    
    def __str__(self):
        return self.name
    
    def get_category_name(self):
        return self.category.name

    def to_json(self):
        return serializers.serialize('json', [self])

class Chapter(models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=100)
    chapter_type = models.CharField(max_length=50)  
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} ({self.chapter_type}) ({self.course.name})"

    

class course_video(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='videos')
    video_name = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.video_name
    
class course_material(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='materials')
    material_name = models.CharField(max_length=100)
    material = models.FileField(upload_to='materials/')
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return super().__str__()
    
class course_textcontent(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='textcontents')
    textcontent = models.TextField()
    status = models.BooleanField(default=False)


class student(models.Model):
  
    university = models.ForeignKey(University,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')])
    profile_img = models.ImageField(upload_to='images/',null=True)
    dept_no = models.CharField(max_length=100)
    # courses = models.ManyToManyField(course, related_name='students')
    academicYear = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True,blank=True)
    
    
    def __str__(self):
        return self.name

    def to_json(self):
        return serializers.serialize('json', [self])
    
class Semester(models.Model):
    SEM_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
    ]
    number = models.PositiveSmallIntegerField(choices=SEM_CHOICES, unique=True)

    def __str__(self):
        return f"Semester {self.number}"



class courseenrollement(models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE, related_name='enrolled_students')
    student = models.ForeignKey(student, on_delete=models.CASCADE, related_name='enrolled_courses')
    course_complete_modules=models.PositiveIntegerField(default=0)
    course_complete_videos=models.PositiveIntegerField(default=0)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    enrolled= models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course} status {self.percentage_complete:.2f}%"
    def get_student_name(self):
        return self.student.name
    def get_course_name(self):
        return self.course.name
    def to_json(self):
        return serializers.serialize('json', [self])

    @property
    def percentage_complete(self):
        total_videos = sum(chapter.videos.count() for chapter in self.course.chapters.all())
        if total_videos == 0:
            return 0
        return (self.course_complete_videos / total_videos) * 100

    @property
    def status(self):
        pct = self.percentage_complete
        if pct == 100:
            return "Completed"
        elif pct >= 76:
            return "Almost Done"
        elif pct >= 26:
            return "In Progress"
        else:
            return "Started"
    
    @property
    def is_completed(self):
        return self.percentage_complete == 100

    def update_completion(self, completed_videos_count, completed_modules_count):
        self.course_complete_videos = completed_videos_count
        self.course_complete_modules = completed_modules_count
        self.completed = (completed_videos_count == sum(chapter.videos.count() for chapter in self.course.chapters.all()))
        self.save()
    
    
class Quiz(models.Model):
    chapter= models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='quizzes')
    question_text = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])
    
    def __str__(self):
        return self.question_text
    def get_chapter_name(self):
        return self.chapter.title

class QuizResult(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.quiz} - {self.score}"   
    def get_student_name(self):
        return self.student.username
    def get_quiz_name(self):
        return self.quiz.name
    def get_quiz_id(self):
        return self.quiz.id
    def get_quiz_result(self):
        return self.score
    
    
class Certificate(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    certificate_image = models.ImageField(upload_to='certificates/')
    
    def __str__(self):
        return f"Certificate for {self.student} in {self.course}"
    
    def get_student_name(self):
        return self.student.name
    def get_course_name(self):
        return self.course.name

class Superadmin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Attendance(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    login_time=models.TimeField(auto_now=True)
    logout_time=models.TimeField(auto_now=True)

class LMSActivity(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    hours_spent = models.FloatField(default=0)
    login_time=models.TimeField(auto_now=True)
    logout_time=models.TimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student} - {self.date} - {self.hours_spent} - {self.login_time} -{self.logout_time}"
    
    
    def calculate_hours_spent(self):
        if self.login_time and self.logout_time:
            login_dt = datetime.combine(self.date, self.login_time)
            logout_dt = datetime.combine(self.date, self.logout_time)
            time_diff = logout_dt - login_dt
            self.hours_spent = round(time_diff.total_seconds() / 3600, 2)
        else:
            self.hours_spent = 0


class payment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.student} - {self.course} - {self.amount} - {self.payment_status}"
    
    def get_student_name(self):
        return self.student.name
    def get_course_name(self):
        return self.course.name
    
    
class Certificate_template(models.Model):
        template = models.ImageField(upload_to='templates/')
        course = models.ForeignKey(course, on_delete=models.CASCADE)
        
        
        def __str__(self):
            return self.course.name




############ University ##############



class CourseAssignment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('department', 'academic_year', 'semester', 'course')

    def __str__(self):
        return f"{self.department.name} - Year {self.academic_year.year} - Sem {self.semester.number} - {self.course.code}"