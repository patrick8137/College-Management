from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_three, name='login_three'),
    path('logout/', views.user_logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('mark-attendance/<int:dept_id>/', views.mark_attendance, name='mark_attendance'),
    path('download-admit/', views.download_admit_card, name='download_admit'),
    path('attendance/<int:dept_id>/', views.mark_attendance, name='mark_attendance'),
    path('timetable/<int:dept_id>/', views.view_timetable, name='view_timetable'),
    path('timetable/<int:dept_id>/add/', views.add_timetable, name='add_timetable'),
]
