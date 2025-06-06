from rest_framework import serializers
from .models import Attendance, LMSActivity,student,teacher,course,course_category,courseenrollement,course_video,Chapter,Certificate,Common_user,Quiz,QuizResult,payment,course_material,course_textcontent
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _




class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'date', 'present']
        
class LMSActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LMSActivity
        fields = ['id','student','date','hours_spent']
        

class studentSerializer(serializers.ModelSerializer):
    class Meta:
        model = student
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def validate_email(self, value):
        if student.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Email already exists."))
        return value

    def validate_phone_number(self, value):
        if student.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(_("Phone number already exists."))
        return value

class teacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = teacher
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def validate_email(self, value):
        if teacher.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Email already exists."))
        return value

    def validate_phone_number(self, value):
        if teacher.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(_("Phone number already exists."))
        return value

class course_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = course_category
        fields = '__all__'
class course_videoSerializer(serializers.ModelSerializer):
    class Meta:
        model = course_video
        fields = ['id', 'video_name', 'video', 'chapter']
        
class course_materialSerializer(serializers.ModelSerializer):
    class Meta:
        model = course_material
        fields = '__all__'
        
class course_textcontentserializer(serializers.ModelSerializer):
    class Meta:
        model = course_textcontent
        fields = '__all__'
        
        
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields=['question_text','option1','option2','option3','option4','answer']


class ChapterSerializer(serializers.ModelSerializer):
    videos = course_videoSerializer(many=True, read_only=True)
    materials = course_materialSerializer(many=True, read_only=True)
    textcontents = course_textcontentserializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'chapter_type', 'videos', 'materials', 'quizzes','textcontents','course']

       

class Common_user_serializers(serializers.ModelSerializer):
    class Meta:
        model = Common_user
        fields = ['id', 'name', 'email', 'password', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class login_userserializer(serializers.ModelSerializer):
    class Meta:
        model = Common_user
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = ['id', 'quiz', 'student', 'score']
    

class courseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)
    class Meta:
        model = course
        fields = ['id', 'name', 'description', 'category', 'image', 'total_chap', 'duration', 'price', 'chapters', 'background_image', 'trending_course', 'ratings', 'paid']


class course_enrollementDashboardSerializer(serializers.ModelSerializer):
    percentage_complete = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = courseenrollement
        fields = ['id', 'course', 'student', 'course_complete_videos', 'percentage_complete','course_complete_modules' 'completed','enrolled','enrollment_date']

    def get_percentage_complete(self, obj):
        return obj.percentage_complete

    def get_status(self, obj):
        return obj.status

class paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = payment
        fields = '__all__'
        extra_kwargs = {
            'amount': {'required': True},
            'payment_method': {'required': True}
        }
        
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'course', 'student', 'certificate_image', 'issue_date']


