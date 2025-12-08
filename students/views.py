from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from .models import Student, Teacher, Department, Attendance, TimeTable
from .forms import StudentCreateForm, TeacherCreateForm, TimeTableForm, DepartmentForm
from datetime import date
from io import BytesIO
from reportlab.pdfgen import canvas

# Role helpers
def is_admin(user):
    return user.is_superuser or user.is_staff

def is_teacher(user):
    return hasattr(user, 'teacher')

def is_student(user):
    return hasattr(user, 'student')

# Single-page login
def login_three(request):
    msg = ''
    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if role == 'admin' and is_admin(user):
                login(request, user)
                return redirect('admin_dashboard')
            if role == 'teacher' and is_teacher(user):
                login(request, user)
                return redirect('teacher_dashboard')
            if role == 'student' and is_student(user):
                login(request, user)
                return redirect('student_dashboard')
            msg = 'Invalid credentials for selected role.'
        else:
            msg = 'Invalid username or password.'
    return render(request, 'login_three.html', {'message': msg})

def user_logout(request):
    logout(request)
    return redirect('login_three')

# Admin dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    teachers = Teacher.objects.select_related('user').all()
    students = Student.objects.select_related('user').all()
    departments = Department.objects.all()
    today = date.today()
    attendance_today = {}
    for dept in departments:
        dept_students = Student.objects.filter(department=dept)
        total = dept_students.count()
        present = Attendance.objects.filter(student__in=dept_students, date=today, present=True).count()
        attendance_today[dept.name] = {'total': total, 'present': present}
    return render(request, 'admin_dashboard.html', {
        'teachers': teachers,
        'students': students,
        'attendance_today': attendance_today,
        'departments': departments,
        'today': today
    })

# Add student (with image upload)
@login_required
@user_passes_test(is_admin)
def add_student(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            first = form.cleaned_data['first_name']
            last = form.cleaned_data.get('last_name', '')
            phone = form.cleaned_data['phone']
            email = form.cleaned_data.get('email', '')
            username = (first + ((' ' + last) if last else '')).strip().replace(' ', '').lower()
            password = phone  # insecure; for demo only
            user = User.objects.create_user(username=username, password=password, first_name=first, last_name=last, email=email)
            student = form.save(commit=False)
            student.user = user
            student.save()
            return redirect('admin_dashboard')
    else:
        form = StudentCreateForm()
    return render(request, 'student_form.html', {'form': form})

# Add teacher
@login_required
@user_passes_test(is_admin)
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['first_name']
            last = form.cleaned_data.get('last_name', '')
            phone = form.cleaned_data['phone']
            email = form.cleaned_data.get('email', '')
            username = (first + last).strip().replace(' ', '').lower()
            password = phone
            user = User.objects.create_user(username=username, password=password, first_name=first, last_name=last, email=email)
            teacher = Teacher(user=user, department=form.cleaned_data.get('department'))
            teacher.save()
            return redirect('admin_dashboard')
    else:
        form = TeacherCreateForm()
    return render(request, 'teacher_form.html', {'form': form})

# Teacher dashboard
@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = request.user.teacher
    departments = Department.objects.all()
    return render(request, 'teacher_dashboard.html', {'teacher': teacher, 'departments': departments})

# Mark attendance (AJAX-friendly)
@login_required
@user_passes_test(is_teacher)
def mark_attendance(request, dept_id=None):
    teacher = request.user.teacher
    dept = get_object_or_404(Department, id=dept_id) if dept_id else None
    students = Student.objects.filter(department=dept) if dept else Student.objects.none()
    if request.method == 'POST':
        date_str = request.POST.get('date')
        if not date_str:
            return JsonResponse({'status':'error','message':'date required'}, status=400)
        dt = date.fromisoformat(date_str)
        for s in students:
            present = request.POST.get(f'present_{s.id}') == 'on'
            att, created = Attendance.objects.get_or_create(student=s, date=dt, defaults={'present': present, 'marked_by': teacher})
            if not created:
                att.present = present
                att.marked_by = teacher
                att.save()
        return JsonResponse({'status':'ok'})
    return render(request, 'mark_attendance.html', {'students': students, 'department': dept, 'today': date.today().isoformat()})

# Student dashboard
from django.utils import timezone
# other imports...

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student = request.user.student
    attends = Attendance.objects.filter(student=student).order_by('-date')

    # Timetable for student's department (order by day then start_time)
    timetable = TimeTable.objects.filter(department=student.department).order_by('day', 'start_time')

    # Optional: compute next upcoming class (simple approach)
    next_class = None
    now = timezone.localtime()
    today_name = now.strftime('%A')  # e.g., 'Monday'
    # find today's classes after current time
    todays = timetable.filter(day=today_name, start_time__gte=now.time()).order_by('start_time')
    if todays.exists():
        next_class = todays.first()

    return render(request, 'student_dashboard.html', {
        'student': student,
        'attendances': attends,
        'timetable': timetable,
        'next_class': next_class,
    })


# Admit card with student image
@login_required
@user_passes_test(is_student)
def download_admit_card(request):
    student = request.user.student
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont('Helvetica-Bold', 20)
    p.drawString(200, 800, 'ADMIT CARD')

    p.setFont('Helvetica', 12)
    p.drawString(40, 750, f"Name: {request.user.get_full_name()}")
    p.drawString(40, 730, f"Username: {request.user.username}")
    p.drawString(40, 710, f"Department: {student.department.name if student.department else '-'}")
    p.drawString(40, 690, f"Roll No: {student.roll_no or '-'}")

    # Draw image if exists
    if student.image:
        try:
            image_path = student.image.path
            # position x=400, y=650 — adjust as needed
            p.drawImage(image_path, 400, 660, width=120, height=120, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            p.drawString(400, 700, "Image not available")

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={'Content-Disposition': 'attachment; filename="admit_card.pdf"'})

@login_required
def view_timetable(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)
    timetable = TimeTable.objects.filter(department=department).order_by('day', 'start_time')

    return render(request, 'view_timetable.html', {
        'department': department,
        'timetable': timetable
    })

@login_required
@user_passes_test(lambda u: is_teacher(u) or is_admin(u))
def add_timetable(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)

    if request.method == 'POST':
        form = TimeTableForm(request.POST)
        if form.is_valid():
            tt = form.save(commit=False)
            tt.department = department   # override department from URL
            tt.save()
            return redirect('view_timetable', dept_id=department.id)
    else:
        form = TimeTableForm(initial={'department': department})

    return render(request, 'add_timetable.html', {
        'form': form,
        'department': department
    })

