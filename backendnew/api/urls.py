from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('student/', views.StudentListCreateView.as_view(), name='student-list'),#student list
    
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),#student
    
    path('teacher/', views.TeacherListView.as_view(), name='teacher-list'),#teacher list
    
    path('teacher/<int:pk>/', views.TeacherDetailView2.as_view(), name='teacher-detail'),#teacher detail
    
    path('coursecategory/', views.CourseCategoryView.as_view(), name='coursecategory-list'),#course category list
    
    path('course/', views.CourseListAPIView.as_view(), name='course-list'),# course list
    
    path('course/<int:pk>/', views.CourseDetailAPIView.as_view(), name='course-detail'),# course detail
    
    path('coursecategory/<int:pk>/', views.CourseCategoryDetailView.as_view(), name='coursecategory-detail'),# course category detail
    
    path('login/',views.login_user, name='login'),# user login
    
    path('register/', views.register_user, name='register'),# user register
    
    path('commonuserregister', views.Common_user_registeer_view, name='commonuserregister'),# common user register
    
    path('commonuserlogin', views.common_user_login_view, name='commonuserlogin'),# common user login
    
    path('coursevideo/', views.CourseVideoListAPIView.as_view(), name='coursevideo-list'),# course video list
    
    path('coursevideo/<int:pk>/', views.CourseVideoDetailAPIView.as_view(), name='coursevideo-detail'),# course video detail
    
    path('chapters/', views.ChapterListCreateAPIView.as_view(), name='chapter-list'),# chapter list
    
    path('chapters/<int:pk>/', views.ChapterDetailAPIView.as_view(), name='chapter-detail'),# chapter detail
    
    path('courseenrollment/', views.student_courseenrollement_view, name='courseenrollment'),# courseenrollement function
    
    path('courseenrollmentlist/', views.CourseEnrollementListAPIView.as_view(), name='courseenrollment-list'),# courseenrollment list
    
    path('courseenrollment/<int:pk>/', views.CourseEnrollementDetailAPIView.as_view(), name='courseenrollment-detail'),# courseenrollment 
    path('studentprogress/', views.student_dashboard ,name='studentprogress'),#student progress

    path('quiz/', views.QuizListCreateView.as_view(), name='quiz-list'),# quiz list
    
    path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),# quiz detail
    
    path('superadminlogin/',views.superadmin_login,name='superadminlogin'),
    
    path('superadminlogout/',views.superadmin_logout,name='superadminlogout'),
    
    path('logout/', views.logout_user, name='logout'),#logout
    
    path('addcourse/',views.add_course,name='addcourse'), #add course
    
    path('displaycourse/',views.display_course,name="displaycourse"), #display course
    
    path('updatecourse/<str:name>',views.update_course,name='updatecourse'), #update course
    
    path('deletecourse/<str:name>',views.delete_course,name="deltecourse"),#delete course
    
    path('createcertificate/',views.create_certificate_api,name='createcertificate'),#create certificate
    
    path('certificateview/',views.Certificatelist.as_view(),name='certificateview'), #certificate view 
    
    path('certificate/',views.view_certificate_api,name='certificate'),
    
    path('success/', views.payment_success, name='success'),# success view
    # course video progress
    path('courseenrollmentprogress/', views.student_courseenrollement_progress_view, name='courseenrollmentprogress'),# course enrollment progress
    
    path('material/',views.coursematerial.as_view(),name = 'material'),
    
    path('courseenrollstatus/',views.check_enrollment_status,name='courseenrollstatus'),
    
    # path('courseenrollprogress/',views.course_enroll_progress,name="courseenrollprogress"), # course enroll progress
    
    path('coursecheck/',views.check_course_status,name='coursecheck'), # course status
    
    
    path('createcategory',views.Create_category,name='createcategory'
        
    ),
    path('updatecategory/<str:name>',views.Update_category,name='updatecategory'),
    
    path('deletecategory/<str:name>',views.Delete_category,name='deletecategory'),
    
    path(
        'createchapter/',views.create_chapter,name='createchapter'
    ),
    path('updatechapter/<str:name>',views.Update_chapter,name='updatechapter'),
    
    path('deletechapter/<str:name>',views.Delete_chapter,name='deletechapter'),
    
    path('createcategory',views.Create_category,name='createcategory'),
    
    path('updatecategory/<str:name>',views.Update_category,name='updatecategory'),
    
    path('deletecategory/<str:name>',views.Delete_category,name='deletecategory'),
    
    path('createcvideo',views.Create_video,name='createvideo'),
    
    path('updatevideo/<str:name>',views.Update_video,name='updatevideo'),
    
    path('deletevideo/<str:name>',views.Delete_video,name='deletevideo'),
    
    path('createdocument',views.Create_document,name='createdocument'),
    
    path('updatedocument/<str:name>',views.Update_document,name='updatedocument'),
    
    path('deletedocument/<str:name>',views.Delete_document,name='deletedocument'),
    
    path('createquiz',views.create_quiz,name='createquiz'),
    
    path('updatequiz/<str:name>',views.update_quiz,name='updatequiz'),
    
    path('deletequiz/<str:name>',views.Delete_quiz,name='deletequiz'),
    
    path('coursedocument/',views.CourseDocumentlist.as_view(),name='coursedocument'),
    
    path('createtext/',views.create_textconntent,name='createtext'),
    
    path('updatetext/<str:name>',views.update_textconntent,name='updatetext'),
    
    path('deletetext/<str:name>',views.Delete_textconntent,name='deletetext'),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    path('studentdashboard/',views.admin_dashboard,name='studentdashboard'),
    
    path('universitydashboard/',views.university_dashboard,name='universitydashboard'),
    
    path('assigncourse/',views.AssignCourseView.as_view() ,name='assigncourse'),
    
    
    
    
    
    
    
    
    
    
    
    








    path('api/token/',views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
