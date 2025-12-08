# College Management System (Django)

A Django-based College Management System with **Principal, Teacher, and Student login**, including CRUD operations, attendance management, timetable handling, student image upload, and PDF admit card generation.

---

## 🚀 Features

### 🔐 Authentication
- Single login page with **3 roles**
  - Principal
  - Teacher
  - Student

### Principal
- Add departments
- Add teachers
- Add students (with image upload)
- Automatically generate student login credentials
- View total attendance
- View teacher & student lists

### Teacher
- Login using assigned credentials
- View students by department
- Mark attendance (AJAX-based)
- View timetable (extendable)

### Student
- Login using admin-generated credentials
- View personal profile
- View attendance history
- Download **Admit Card (PDF)** with uploaded photo


## Future Enhancements

The following features can be added in future versions of this project to improve functionality, scalability, and security:

### Authentication & Security
- Role-based permissions using Django Permissions & Groups
- Change password option for teachers and students
- Forgot password / password reset via email

### 🎓 Academic Management
- Subject-wise attendance tracking
- Marks and internal assessment module
- Course & subject allocation to teachers

### 📆 Timetable & Scheduling
- Advanced timetable generator
- Clash detection for teacher schedules
- Student-specific timetable view

### 📊 Reports & Analytics
- Attendance reports by department/subject
- Monthly & yearly attendance analysis
- Graphical dashboards using charts

### 🖼 UI & User Experience
- Mobile-responsive design
- Profile edit pages for all roles


### 📄 Documents & Exports
- Advanced PDF admit cards with QR code
- ID card generation
- Attendance & report export to Excel/PDF