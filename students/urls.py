from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_three, name='login_three'),
    path('logout/', views.user_logout, name='logout'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('attendance/<int:dept_id>/', views.mark_attendance, name='mark_attendance'),
    path('download-admit/', views.download_admit_card, name='download_admit'),
    path('timetable/<int:dept_id>/', views.view_timetable, name='view_timetable'),
    path('timetable/<int:dept_id>/add/', views.add_timetable, name='add_timetable'),
    path('timetable/<int:dept_id>/<int:tt_id>/edit/', views.edit_timetable, name='edit_timetable'),
    path('timetable/<int:dept_id>/<int:tt_id>/delete/', views.delete_timetable, name='delete_timetable'),
]
