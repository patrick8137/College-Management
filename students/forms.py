from django import forms
from .models import Student, Teacher, Department, TimeTable

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class TeacherCreateForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=True)

    class Meta:
        model = Teacher
        fields = ['department']

class StudentCreateForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=True)

    class Meta:
        model = Student
        fields = ['department', 'image', 'roll_no']

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['department', 'day', 'start_time', 'end_time', 'subject', 'teacher']
