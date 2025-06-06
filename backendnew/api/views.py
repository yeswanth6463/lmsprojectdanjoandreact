from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Certificate, student
from .serializers import CertificateSerializer
from rest_framework.decorators import action, api_view
from .models import student, teacher,  course_category, Common_user,  course_video, Chapter, course,courseenrollement, Quiz,QuizResult,Certificate,Superadmin,payment,course_material,University,course_textcontent
from .serializers import studentSerializer, teacherSerializer, course_categorySerializer, Common_user_serializers, course_videoSerializer, ChapterSerializer, courseSerializer,login_userserializer,course_enrollementDashboardSerializer, QuizSerializer,CertificateSerializer,course_materialSerializer,course_textcontentserializer
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from .certificate_generator import generate_certificate_image 
from urllib.parse import unquote
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import  Attendance, LMSActivity
from .models import payment
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse 
#how to import csrf_exempt in django rest framework
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import razorpay
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
import os
from django.conf import settings
from rest_framework import status
from .serializers import AttendanceSerializer, LMSActivitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import logout
from .models import student, Attendance  # Adjust your import based on your app
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# user = User.objects.get(username='yesh')
# token, created = Token.objects.get_or_create(user=user)
# print(token.key)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra user info in response
        data.update({
            'user': {
                'id': self.user.id,
                'name': self.user.name,
                'email': self.user.email,
                'user_type': self.user.user_type,
            }
        })
        return data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = student.objects.all()
    serializer_class = studentSerializer

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = student.objects.all()
    serializer_class = studentSerializer
    
class TeacherListCreateView(generics.ListCreateAPIView):
    queryset = teacher.objects.all()
    serializer_class = teacherSerializer
    
class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = teacher.objects.all()
    serializer_class = teacherSerializer

class TeacherListView(generics.ListCreateAPIView):
    queryset = teacher.objects.all()
    serializer_class = teacherSerializer

class TeacherDetailView2(generics.RetrieveUpdateDestroyAPIView):
    queryset = teacher.objects.all()
    serializer_class = teacherSerializer
    
class CourseCategoryView(generics.ListCreateAPIView):
    queryset = course_category.objects.all()
    serializer_class = course_categorySerializer

class CourseCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = course_category.objects.all()
    serializer_class = course_categorySerializer

class CourseVideoListAPIView(generics.ListCreateAPIView):
    queryset = course_video.objects.all()
    serializer_class = course_videoSerializer
class CourseVideoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = course_video.objects.all()
    serializer_class = course_videoSerializer

class ChapterListCreateAPIView(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class ChapterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class CourseListAPIView(generics.ListAPIView):
    queryset = course.objects.all()
    serializer_class = courseSerializer

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = course.objects.all()
    serializer_class = courseSerializer
    
class CourseDocumentlist(generics.ListAPIView):
    queryset = course_material.objects.all()
    serializer_class = course_materialSerializer
    
class coursetextview(generics.ListAPIView):
    queryset = course_textcontent.objects.all()
    serializer_class = course_textcontentserializer

class coursetextdetailview(generics.RetrieveDestroyAPIView):
    queryset = course_textcontent.objects.all()
    serializer_class = course_textcontentserializer

    

class CourseEnrollementListAPIView(generics.ListCreateAPIView):
    queryset = courseenrollement.objects.all()
    serializer_class = course_enrollementDashboardSerializer
class CourseEnrollementDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = courseenrollement.objects.all()
    serializer_class = course_enrollementDashboardSerializer
    
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class Certificatelist(generics.ListCreateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    
class coursematerial(generics.ListCreateAPIView):
    queryset = course_material.objects.all()
    serializer_class = course_materialSerializer

@api_view(['GET'])
def Certficateviewuser(request):
    email = request.GET.get('email')
    print(email)
    students_instance = student.objects.filter(email=email).first()
    print(students_instance)
    
    if students_instance:
        certificate_instance = Certificate.objects.filter(student=students_instance).first()
        data = {
            'certificate': certificate_instance.certificate_image.url if certificate_instance else None
        }
    else:
        data = {
            'error': 'Student not found.'
        }

    return Response(data)

@api_view(['POST', 'GET'])
def logout_user(request):
    from datetime import datetime
    from django.utils.timezone import make_aware, is_aware

    login_str = request.data.get('storedLoginTime')
    logout_str = request.data.get('logout_time')
    user_email = request.data.get('student_email')

    if not logout_str or not user_email or not login_str:
        return Response({"error": "Missing logout_time, login_time, or email."}, status=400)

    time_format = "%d/%m/%Y, %I:%M:%S %p"

    try:
        login_time = datetime.strptime(login_str, time_format)
        logout_time = datetime.strptime(logout_str, time_format)

        # Ensure both times are timezone-aware
        if not is_aware(login_time):
            login_time = make_aware(login_time)
        if not is_aware(logout_time):
            logout_time = make_aware(logout_time)

    except ValueError:
        return Response({"error": "Invalid date format."}, status=400)

    delta = logout_time - login_time
    new_hours_spent = min(delta.total_seconds() / 3600, 24)

    # --- Try student first
    student_instance = student.objects.filter(email=user_email).first()
    if student_instance:
        try:
            attendance_record = Attendance.objects.filter(student=student_instance).last()
            if attendance_record:
                attendance_record.logout_time = logout_time
                attendance_record.save()

            lms_record = LMSActivity.objects.filter(student=student_instance).last()
            if lms_record:
                previous_hours = lms_record.hours_spent or 0
                lms_record.logout_time = logout_time
                lms_record.hours_spent = round(previous_hours + new_hours_spent, 2)
                lms_record.save()
        except Exception as e:
            return Response({"error": f"Failed to update student records: {str(e)}"}, status=500)

    else:
        # --- Try teacher
        teacher_instance = teacher.objects.filter(email=user_email).first()
        if teacher_instance:
            print("logout successfull ")
        else:
            return Response({"error": "No user (student or teacher) found with this email."}, status=404)

    # Log out from session
    try:
        logout(request._request)
        return Response({"message": "Logout successful.", "hours_spent": round(new_hours_spent, 2)}, status=200)
    except Exception as e:
        return Response({"error": f"Logout failed: {str(e)}"}, status=500)

@api_view(['POST'])
def login_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        user_type = request.data.get('user_type')
        print(email)
        users=0
        if user_type == 'student':
            try:
                users = student.objects.get(email=email, password=password, user_type=user_type)
            except student.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        elif user_type == 'teacher':
            try:
                users = teacher.objects.get(email=email, password=password, user_type=user_type)
            except teacher.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(users)

        if user_type == 'student':
            from datetime import date
            today = date.today()
            login_time = request.data.get('login_time')
            
            try:
                attendance = Attendance.objects.get(student=users, date=today)
            except Attendance.DoesNotExist:
                attendance = None
            try:
                lms_activity = LMSActivity.objects.get(student=users, date=today)
            except LMSActivity.DoesNotExist:
                lms_activity = None

            if attendance is None:
                Attendance.objects.create(student=users, date=today,present=True, login_time=login_time)
            else:
                attendance.login_time = login_time
                attendance.save()

            if lms_activity is None:
                LMSActivity.objects.create(student=users, date=today)
            else:
                lms_activity.save()
                
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": users.id,
                "name": users.name,
                "email": users.email,
                "user_type": users.user_type
            },
            "login_time":login_time
        }, status=status.HTTP_200_OK)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def common_user_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user= Common_user.objects.get(email=email, password=password)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        except Common_user.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    name = request.data.get('name')
    phone_number = request.data.get('phone')
    email = request.data.get('email')
    password = request.data.get('password')
    user_type = request.data.get('user_type')
    # print(user_type)
    if user_type == 'student':
        try:
            user = student.objects.get(email=email)
            if user:
                print("User already exists")
                return Response({"error": "user already exists "}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            user = student(name=name, phone_number=phone_number, email=email, password=password, user_type=user_type)
            user.save()
            print(" registration successful ")
            return Response('User registered successfully')
    elif user_type == 'teacher':
        try:
            user = teacher.objects.get(email=email)
            if user:
                print("User already exists")
                return Response({"error": "user already exists "}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            user = teacher(name=name, phone_number=phone_number, email=email, password=password, user_type=user_type)
            user.save()
            print(" registration successful ")
            return Response('User registered successfully')
    else:
        return Response('Invalid user type')

@api_view(['POST'])
def Common_user_registeer_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        university = request.POST.get('university')
        qualification = request.POST.get('qualification')
        try:
            user = Common_user.objects.get(email=email)
            return Response('User already exists')
        except Common_user.DoesNotExist:
            user = Common_user(name=name, phone_number=phone_number, email=email, password=password, university=university, qualification=qualification)
            user.save()
            return Response('User registered successfully')

@api_view(['POST'])
def student_courseenrollement_view(request):
    # import logging
    # logger = logging.getLogger(_name_)
    # logger.info(f"Received enrollment request data: {request.data}")
    if request.method == 'POST':
        course_id = request.data.get('id')
        student_email = request.data.get('email')
        student_name = request.data.get('name')
        number = request.data.get('number')
        amount = request.data.get('amount')

        
    print(student_email, course_id,student_name,number,amount)
    if not student_email:
        print("Email parameter is missing")
        return Response({"error": "Email parameter is required"}, status=400)
    try:
        students = student.objects.get(email=student_email)
        print(number)
        if not students:
            return Response({"error": "Student not found or unauthorized"}, status=404)
        course_details = course.objects.get(id=course_id)
        if not course_details:
            return Response({"error": "Course not found"}, status=404)
    except student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)
    except course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    student_obj = student.objects.get(email=student_email)
    course_obj = course.objects.get(id=course_id)
    print(student_obj)
    print(course_obj)



    if courseenrollement.objects.filter(course=course_obj, student=student_obj).exists():
    
        return Response({'error': 'Student already enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        enrollement = courseenrollement(course=course_obj, student=student_obj)
        # enrollement.save()

        client = razorpay.Client(auth=("rzp_test_6b8dLoMFlQOROE", "cWTmuq2mTfiSTzsZW0uWv56f"))
        amount = int((amount) * 100)

        payment_order = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'
        })
        

        payment.objects.create(
            name=student_name,
            email=student_email,
            phone_number=number,
            student=student_obj,
            course=course_obj,
            amount=amount,
            payment_id=payment_order['id'],
            payment_status=True,
        )

       
        return Response({
            'message': 'Enrollment successful',
            'order_id': payment_order['id'],
            'razorpay_key_id': 'rzp_test_6b8dLoMFlQOROE',
            'amount': amount,
            'currency': 'INR',
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        return Response({'error': f'Error occurred during enrollment: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def payment_success(request):
    if request.method == "POST":
        data = json.loads(request.body)

        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")

        if not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
            return JsonResponse({"error": "Missing payment details"}, status=400)

        client = razorpay.Client(auth=("rzp_test_6b8dLoMFlQOROE", "cWTmuq2mTfiSTzsZW0uWv56f"))

        try:
            # Verify signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            return JsonResponse({"status": "Payment verified successfully"})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"error": "Signature verification failed"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
    
@api_view(['POST'])
def superadmin_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            admin = Superadmin.objects.get(username=username, password=password)
            return Response('Admin logged in successfully', status=status.HTTP_200_OK)
        except Exception as e:
            return Response('Invalid username or password', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def superadmin_logout(request):
     if request.method == 'POST':
        try:
            logout(request._request)
            return Response('Logout successful')
        except Exception as e:
            print(e)
            return Response('Logout failed')
        else:
            return Response('Invalid request method')


@api_view(['GET'])
def student_dashboard(request):
    student_email = request.query_params.get('email')
    print(f"Requested email: {student_email}")

    if not student_email:
        return Response({"error": "Email parameter is required"}, status=400)

    try:
        student_instance = student.objects.get(email=student_email)
    except student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)

    # Now you trust the email. Optionally, validate token here.

    courses = courseenrollement.objects.filter(student=student_instance)
    certificateissue = Certificate.objects.filter(student=student_instance)
    total_courses = courses.count()
    completed_courses = courses.filter(completed=True).count()
    not_completed = total_courses - completed_courses
    certificate_gained=0
    if certificateissue:
        certificate_gained=certificateissue.count()
    
    course_details = [
        {
            'course_id': ce.course.id,
            'course_name': ce.course.name,
            'course_description': ce.course.description,
            'course_image': ce.course.image.url if ce.course.image else None,
        } for ce in courses
    ]

    attendance_records = Attendance.objects.filter(student=student_instance, present=True)
    attendance_dates = [att.date.isoformat() for att in attendance_records]
    activities = LMSActivity.objects.filter(student=student_instance)
    hours_by_date = {}
    for activity in activities:
        date_str = activity.date.strftime('%Y-%m-%d')
        hours_by_date[date_str] = hours_by_date.get(date_str, 0) + activity.hours_spent

    return Response({
        "student": {
            "name": student_instance.name,
            "email": student_instance.email,
            "id": student_instance.id
        },
        "courses": {
            "total": total_courses,
            "completed": completed_courses,
            "not_completed": not_completed,
            "course_details": course_details,
            'certificate_gained':certificate_gained,
        },
        "attendance": attendance_dates,
        "hours_spent": hours_by_date,
    })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_attendance(request):
    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print("attendence saved")
        return Response({'message': 'Attendance saved successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_lms_activity(request):
    serializer = LMSActivitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'LMS activity saved successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def student_courseenrollement_progress_view(request):
   student_email = request.GET.get('email')
   course_id = request.GET.get('course_id')
   print(student_email, course_id)
   if not student_email:
        print("Email parameter is missing")
        return Response({"error": "Email parameter is required"}, status=400)
   try:
        students = student.objects.get(email=student_email)
        if not students:
            return Response({"error": "Student not found or unauthorized"}, status=404)
        course_details = course.objects.get(id=course_id)
        if not course_details:
            return Response({"error": "Course not found"}, status=404)
   except student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)
   except course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)
   except Exception as e:
        return Response({"error": str(e)}, status=500)
   try:
        course_enrollment = courseenrollement.objects.create(student=students, course=course_details,enrolled=True)
        course_enrollment.save()
        return Response({"message": "Course enrollment created successfully"}, status=201)
   except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def check_enrollment_status(request):
    student_email = request.query_params.get('email')
    course_id = request.query_params.get('course_id')

    if not student_email or not course_id:
        return Response({"error": "Both email and course_id are required"}, status=400)
    try:
        student_obj = student.objects.get(email=student_email)
        course_obj = course.objects.get(id=course_id)
    except student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)
    except course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    try:
        enrollment = courseenrollement.objects.filter(student=student_obj, course=course_obj).first()
        enrolled_status = enrollment.enrolled if enrollment else False
        return Response({"enrolled": enrolled_status}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def university_dashboard(request):
    try:
        university = university.objects.get(id=1)
        return Response({"university": university.name}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@csrf_exempt
@api_view(['POST'])
def create_certificate_api(request):
    email = request.data.get('email')
    course_name = request.data.get('course')
    print(email)
    print(course_name)

    if not email or not course_name:
        return HttpResponse("Missing email or course name", status=400)

    try:
        student_instance = student.objects.get(email=email)
    except student.DoesNotExist:
        raise Http404("Student not found")

    try:
        course_instance = course.objects.get(name=course_name)
    except course.DoesNotExist:
        raise Http404("Course not found")

    # Generate certificate image as ContentFile
    student_name = student_instance.name
    print(student_name)
    certificate_file = generate_certificate_image(student_name, course_name)

    # Create and save certificate model instance
    certificate = Certificate.objects.create(
        student=student_instance,
        course=course_instance,
        certificate_image=certificate_file,
    )
    certificate.certificate_image.save(certificate_file.name, certificate_file)
    certificate.save()

    # Return the saved image as response
    response = HttpResponse(certificate_file, content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="{certificate_file.name}"'
    return response


@api_view(['GET'])
def view_certificate_api(request):
    email = request.GET.get('email')
    course_name = request.GET.get('course')

    print(f"Email: {email}")
    print(f"Course: {course_name}")

    try:
        student_instance = student.objects.get(email=email)
        course_instance = course.objects.get(name=course_name)

        certificate = Certificate.objects.filter(student=student_instance, course=course_instance).first()

        if certificate:
            return HttpResponse(certificate.certificate_image, content_type='image/jpeg')
        else:
            return Response({"error": "Certificate not found"}, status=404)

    except student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)
    except course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def check_course_status(request):
    student_email = request.query_params.get('email')
    course_id = request.query_params.get('course_id')

    if not student_email or not course_id:
        return Response({"error": "Both email and course_id are required"}, status=400)
    try:
        student_obj = student.objects.get(email=student_email)
        course_obj = course.objects.get(id=course_id)
    except student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)
    except course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    try:
        enrollment = courseenrollement.objects.filter(student=student_obj, course=course_obj).first()
        enrolled_status = enrollment.completed if enrollment else False
        return Response({"completed": enrolled_status}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def add_course(request):
    if request.method == 'POST':
        try:
            course_name = request.data.get('name')
            course_description = request.data.get('Description')
            course_image = request.data.get('Image')  
            print(course_image)
            total_chapter = request.data.get('total_chap')
            duration = request.data.get('duration')
            price = request.data.get('Price')
            background_image = request.data.get('BackgroundImage')
            print(background_image)
            # trending_course = request.data.get('trending_data')
            category = request.data.get('category')
            print(category)
            course_categor_instance = course_category.objects.get(name=category)
            print(course_categor_instance)
            course.objects.create(
                name=course_name,
                description=course_description,
                image=course_image,
                total_chap=total_chapter,
                duration=duration,
                price=price,
                background_image=background_image,
                category=course_categor_instance,
            )

            return Response({'message': 'Course added successfully'}, status=201)

        except Exception as e:
            print("Error:", str(e))
            return Response({'error': 'Error occurred while adding course'}, status=400)

@api_view(['PUT'])
def update_course(request, name):
    try:
        decoded_name = unquote(name)
        course_obj = course.objects.get(name=decoded_name)
        course_obj.name = request.data.get('name', course_obj.name)
        course_obj.description = request.data.get('description', course_obj.description)
        course_obj.total_chap = int(request.data.get('total_chap', course_obj.total_chap))
        course_obj.duration = int(request.data.get('duration', course_obj.duration))
        course_obj.price = int(request.data.get('price', course_obj.price))

        if 'Image' in request.FILES:
            course_obj.image = request.FILES['Image']
        if 'BackgroundImage' in request.FILES:
            course_obj.background_image = request.FILES['BackgroundImage']

        category_id = request.data.get('category')
        if category_id:
            from .models import course_category
            try:
                category_obj = course_category.objects.get(id=int(category_id))
                course_obj.category = category_obj
            except course_category.DoesNotExist:
                pass

        trending_course = request.data.get('trending_course')
        if trending_course is not None:
            course_obj.trending_course = trending_course.lower() in ['true', '1', 'yes']

        ratings = request.data.get('ratings')
        if ratings:
            course_obj.ratings = float(ratings)

        paid = request.data.get('paid')
        if paid is not None:
            course_obj.paid = paid.lower() in ['true', '1', 'yes']

        course_obj.save()
        return Response({'message': 'Course updated successfully'}, status=status.HTTP_200_OK)
    except course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def display_course(request):
    if request.method == 'GET':
        try:
            courses = course.objects.all()
            serializer = courseSerializer(courses, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            print("Error:", str(e))
            return Response({'error': 'Error occurred while displaying courses'}, status=400)

@api_view(['DELETE'])
def delete_course(request, name):
    try:
        courses = course.objects.get(name=name)
        courses.delete()
        return Response({'message': 'Course deleted'}, status=status.HTTP_204_NO_CONTENT)
    except course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def Create_category(request):
    category_name = request.data.get('category_name')
    print(category_name)
    if not category_name:
        return Response({"error": "Both category_name and category_description are required"}, status=400)
    try:
        course_category.objects.get(name=category_name)
        return Response({"error": "Category already exists"}, status=400)
    
    except course_category.DoesNotExist:
        category = course_category.objects.create(name=category_name)
        category.save()
        
        return Response({"message": "Category created"}, status=200)
    except Exception as e:
        print(e)
        return Response({"error": "Category already exists"}, status=400)

@api_view(['PUT'])
def Update_category(request, pk):
    try:
        category = course_category.objects.get(id=pk)
    except course_category.DoesNotExist:
        return Response({"error": "Category not found"}, status=404)
    category_name = request.data.get('category_name')
    category_description = request.data.get('category_description')
    if not category_name or not category_description:
        return Response({"error": "Both category_name and category_description are required"}, status=400)
    category.category_name = category_name
    category.category_description = category_description
    
    category.save()
    return Response({"message": "Category updated successfully"}, status=200)

@api_view(['DELETE'])
def Delete_category(request, pk):
    try:
        category = course_category.objects.get(id=pk)
    except course_category.DoesNotExist:
        return Response({"error": "Category not found"}, status=404)
    category.delete()
    return Response({"message": "Category deleted successfully"}, status=200)

@api_view(['POST'])
def create_chapter(request):
    chapter_name = request.data.get('title')
    # chapter_type = request.data.get('chapter_type')
    course_name = request.data.get('course')
    print(chapter_name,course_name)
    if not chapter_name or not course_name:
        return Response({"error": "Both chapter_name, chapter_description and course_id are required"}, status=400)
    try:
        # Get course instance by name
        course_instance = course.objects.get(id=course_name)
        chapters = Chapter.objects.create(title=chapter_name,course=course_instance)
        chapters.save()
        return Response({"message": "Chapter created successfully"}, status=201)
    except course.DoesNotExist:
        print(e)
        return Response({"error": "Course not found"}, status=404)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=500)

@api_view(['PUT'])
def Update_chapter(request, str):
    
        try:
            chapter = Chapter.objects.get(title=str)
        except Chapter.DoesNotExist:
            return Response({"error": "Chapter not found"}, status=404)
        chapter_name = request.data.get('chapter_name')
        chapter_description = request.data.get('chapter_description')
        course_name = request.data.get('course_name')
        if not chapter_name or not chapter_description or not course_name:
            return Response({"error": "Both chapter_name, chapter_description and course_id are required"}, status=400)
        try:
            course_instance = course.objects.get(name=course_name)
        except course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)
        chapter.title = chapter_name
        chapter.chapter_description = chapter_description
        chapter.course = course_instance
        
        chapter.save()
        return Response({"message": "Chapter updated successfully"}, status=200)

@api_view(['DELETE'])
def Delete_chapter(request, str):
    try:
        chapter = Chapter.objects.get(title=str)
    except chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=404)
    chapter.delete()
    return Response({"message": "Chapter deleted successfully"}, status=200)


@api_view(['POST'])
def Create_video(request):
    
    video_name = request.data.get('video_name')
    video = request.FILES.get('video')
    chapter_name = request.data.get('chapter_name')
    
    try:
        chapter = Chapter.objects.get(title=chapter_name)
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=404)
    if not video_name or not video or not chapter_name:
        return Response({"error": "Both video_name, video and chapter_name are required"}, status=400)
    chapter_instance = Chapter.objects.filter(title=chapter_name)
    video_instance = course_video(video=video, title=video_name, chapter=chapter_instance)
    video_instance.save()
    return Response({"message": "Video created successfully"}, status=200)


@api_view(['PUT'])
def Update_video(request, pk):
    try:
        video = course_video.objects.get(id=pk)
    except course_video.DoesNotExist:
        return Response({"error": "Video not found"}, status=404)
    video_name = request.data.get('video_name')
    video = request.FILES.get('video')
    chapter_name = request.data.get('chapter_name')
    try:
        chapter = Chapter.objects.get(title=chapter_name)
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=404)
    if not video_name or not video or not chapter_name:
        return Response({"error": "Both video_name, video and chapter_name are required"}, status=
                        400)
        video_instance = course_video.objects.filter(id=pk)
        video_instance.video = video
        video_instance.title = video_name
        video_instance.chapter = chapter
        video_instance.save()
        return Response({"message": "Video updated successfully"}, status=200)

@api_view(['DELETE'])
def Delete_video(request, pk):
    try:
        video_instance = course_video.objects.get(id=pk)
    except course_video.DoesNotExist:
        return Response({"error": "Video not found"}, status=404)
    video_instance.delete()
    return Response({"message": "Video deleted successfully"}, status=200)


@api_view(['POST'])
def Create_document (request):
    document_name = request.data.get('document_name')
    document = request.FILES.get('document')
    chapter_name = request.data.get('chapter_name')
    try:
        chapter_instance = Chapter.objects.get(title=chapter_name)
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=404)
    if not document_name or not document or not chapter_name:
        return Response({"error": "Both document_name, document and chapter_name are required"}, status=400)
    document_instance = course_material.objects.create(document=document, title=document_name, chapter=chapter_instance)
    document_instance.save()
    return Response({"message": "Document created successfully"}, status=200)


@api_view(['PUT'])
def Update_document(request, pk):
    try:
        document = course_material.objects.get(id=pk)
    except course_material.DoesNotExist:
        return Response({"error": "Document not found"}, status=404)
    document_name = request.data.get('document_name')
    document = request.FILES.get('document')
    chapter_name = request.data.get('chapter_name')
    try:
        chapter_instance = Chapter.objects.get(title=chapter_name)
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=404)
    if not document_name or not document or not chapter_name:
        return Response({"error": "Both document_name, document and chapter_name are required"}, status=
                        400)
    document.title = document_name
    document.document = document
    document.chapter = chapter_instance
    document.save()
    return Response({"message": "Document updated successfully"}, status=200)
    

@api_view(['DELETE'])
def Delete_document(request, pk):
    try:
        document = course_material.objects.get(id=pk)
    except course_material.DoesNotExist:
        return Response({"error": "Document not found"}, status=404)
    document.delete()
    return Response({"message": "Document deleted successfully"}, status=200)


@api_view(['POST'])
def create_textconntent(request):
    text_content = request.data.get('text_content')
    chapter_name = request.data.get('chapter_name')
    try:
        chapter_instance = Chapter.objects.get(title=chapter_name)
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=404)
    if not text_content or not chapter_name:
        return Response({"error": "Both text_content and chapter_name are required"}, status=400)
    text_content_instance = course_textcontent.objects.create(text=text_content, chapter=chapter_instance)
    text_content_instance.save()
    return Response({"message": "Text content created successfully"}, status=200)

@api_view(['PUT'])
def update_textconntent(request,pk):
    try:
        text_content_instance = course_textcontent.objects.get(id=pk)
    except course_textcontent.DoesNotExist:
        return Response({"error": "Text content not found"}, status=404)
    text_content = request.data.get('text_content')
    chapter_name = request.data.get('chapter_name')
    try:
        chapter_instance = Chapter.objects.get(title=chapter_name)
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=404)
    if not text_content or not chapter_name:
        return Response({"error": "Both text_content and chapter_name are required"}, status=400)
    text_content_instance.text = text_content
    text_content_instance.chapter = chapter_instance
    text_content_instance.save()
    return Response({"message": "Text content updated successfully"}, status=200)

@api_view(['DELETE'])
def Delete_textconntent(request, pk):
    try:
        text_content_instance = course_textcontent.objects.get(id=pk)
    except course_textcontent.DoesNotExist:
        return Response({"error": "Text content not found"}, status=404)
    text_content_instance.delete()
    return Response({"message": "Text content deleted successfully"}, status=200)

@api_view(['POST'])
def create_quiz(request):
    question_texts = request.data.get('text')
    option1 = request.data.get('option1')
    option2 = request.data.get('option2')
    option3 = request.data.get('option3')
    option4 = request.data.get('option4')
    correct_answer = request.data.get('correct_option')
    chapter_name = request.data.get('chapter')
    try:
        chapter_instance = Chapter.objects.get(title=chapter_name)
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=404)
    if not question_texts or not option1 or not option2 or not option3 or not option4 or not correct_answer or not chapter_name:
        return Response({"error": "All fields are required"}, status=400)
    quiz = Quiz.objects.create(text=question_texts, option1=option1, option2=
                               option2, option3=option3, option4=option4, correct_answer=correct_answer
                               , chapter=chapter_instance)
    quiz.save()
    return Response({"message": "Quiz created successfully"}, status=200)

@api_view(['PUT'])
def update_quiz(request,pk):
    try:
        quiz = Quiz.objects.get(id=pk)
    except Quiz.DoesNotExist:
        return Response({"error": "Quiz not found"}, status=404)
    quiz.chapter = request.data.get('chapter') 
    quiz.text = request.data.get('text')
    quiz.option1 = request.data.get('option1')
    quiz.option2 = request.data.get('option2')
    quiz.option3 = request.data.get('option3')
    quiz.option4 = request.data.get('option4')
    quiz.correct_answer = request.data.get('correct_option')
    quiz.save()
    return Response({"message": "Quiz updated successfully"}, status=200)

@api_view(['DELETE'])
def Delete_quiz(request, pk):
    try:
        quiz = Quiz.objects.get(id=pk)
    except Quiz.DoesNotExist:
        return Response({"error": "Quiz not found"}, status=404)
    quiz.delete()
    return Response({"message": "Quiz deleted successfully"}, status=200)

@api_view(['GET'])
def admin_dashboard(request):
    
    
    
    total_student = student.objects.count()
    total_faculity = teacher.objects.count()
    total_university = University.objects.count()
    
    data={
        'total_student':total_student,
        'total_faculity':total_faculity,
        'total_university':total_university
    }
    
    return Response(data)

@api_view(['POST'])
def  University_dashboard(request):
    try:
        university = University.data.get('email')
    except University.DoesNotExist:
        return Response({"error": "University not found"}, status=404)
    university_instance = University.objects.filter(email=university)
    total_student = student.objects.filter(university=university_instance).count()
    total_faculity = teacher.objects.filter(university=university_instance).count()
    
    data={
        'total_student':total_student,
        'total_faculity':total_faculity
        
    }
    return Response(data)

class AssignCourseView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        student_id = request.data.get('student_id')
        course_id = request.data.get('course_id')
        try:
            student = student.objects.get(id=student_id)
            course = course.objects.get(id=course_id)
            course_enrollment = courseenrollement.objects.create(student=student_id, course=course_id,enrolled=True)
            course_enrollment.save()
            
            return Response({'message': 'Course assigned successfully'})
        except student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        except course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=404)



