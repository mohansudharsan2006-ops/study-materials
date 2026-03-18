# 🚀 Quick Start Guide - StudyHub

## Installation & Setup

### 1. **Prerequisites**
- Python 3.7+
- Virtual environment (already set up in your project)

### 2. **Install Dependencies**
```bash
cd f:\study materials
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. **Run the Application**
```bash
python api\app.py
```

The app will start on `http://localhost:5000`

---

## 🎯 First-Time User Guide

### For Students

1. **Sign Up**
   - Go to `/register`
   - Select "Student" as account type
   - Fill in your details and create account

2. **Browse Courses**
   - Visit `/courses`
   - Click on any course to view details
   - Click "Enroll" button to join

3. **Access Dashboard**
   - Click "My Dashboard" in navigation
   - View all your enrolled courses
   - See pending assignments
   - Read announcements

4. **Submit Assignments**
   - Go to your course
   - Click on "Assignments"
   - Click "Submit" on any assignment
   - Upload file or type your answer
   - Click "Submit" to complete

5. **View Profile**
   - Click your name in top right
   - Select "Profile"
   - Click "Edit Profile" to update your information

### For Teachers

1. **Sign Up**
   - Go to `/register`
   - Select "Teacher" as account type
   - Create your account

2. **Create a Course**
   - Click "Teach" in navigation (or "Create Course")
   - Fill in course details
   - Select department
   - Save course

3. **Manage Course**
   - Go to "Teacher Dashboard"
   - Click "View" on your course
   - Add announcements and materials

4. **Create Assignments**
   - Click "Assignments" for your course
   - Click "Create Assignment"
   - Set title, description, due date
   - Optionally upload assignment file
   - Save

5. **Grade Submissions**
   - Go to "Teacher Dashboard"
   - Look for "Submissions to Grade"
   - Click "Grade" button
   - Enter score and feedback
   - Submit

6. **Upload Resources**
   - Click "Resources" in navigation
   - Click "Upload Resource"
   - Select resource type
   - Choose subject/topic
   - Upload file
   - Save

---

## 🧪 Demo Accounts

When you first run the app, you can create accounts with these credentials:

### Student Account
```
Name: John Doe
Email: student@example.com
Password: password123
Role: Student
```

### Teacher Account
```
Name: Dr. Jane Smith
Email: teacher@example.com
Password: password123
Role: Teacher
```

---

## 📚 Features Overview

### Student Features
✅ Enroll in multiple courses
✅ View course materials and lessons
✅ Submit assignments online
✅ Receive grades and feedback
✅ Read course announcements
✅ Access downloadable resources
✅ Track your progress

### Teacher Features
✅ Create and manage courses
✅ Upload study materials
✅ Create multiple assignments
✅ View student submissions
✅ Grade assignments with feedback
✅ Post course announcements
✅ Track student enrollment
✅ Manage course resources

### Admin Features
✅ Access all teacher features
✅ View all courses and users
✅ System-wide statistics
✅ Manage departments

---

## 🗂️ Main Pages

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/` | Landing page with stats |
| Login | `/login` | Sign in |
| Register | `/register` | Create new account |
| Courses | `/courses` | Browse all courses |
| My Dashboard | `/dashboard/student` | Student overview |
| Teach | `/dashboard/teacher` | Teacher management |
| Resources | `/resources` | Study materials |
| Profile | `/profile` | User information |

---

## 📁 File Organization

```
Uploads/
├── student_123_assignment1.pdf   (Student submissions)
├── teacher_5_course_outline.docx (Course materials)
└── ...

study_materials.db               (SQLite database)
├── users table
├── courses table
├── assignments table
├── submissions table
└── ... (13 more tables)
```

---

## 🔧 Configuration Options

Edit `api/app.py` to customize:

**Database:**
```python
DATABASE = 'study_materials.db'
```

**Security:**
```python
app.secret_key = "advanced_secret_key_2024"
```

**File Upload:**
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', ...}
```

**Flask Settings:**
```python
app.run(debug=True, port=5000)
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Activate virtual environment and install dependencies
```bash
.\venv\Scripts\Activate.ps1
pip install flask
```

### "Address already in use"
**Solution:** Change port in app.py
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### "DatabaseError"
**Solution:** Delete `study_materials.db` to reset database
- Database will recreate automatically on next run

### "File upload not working"
**Solution:** Ensure `uploads/` folder exists
```bash
mkdir uploads
```

---

## 🚀 Deployment

### Deploy to Heroku
1. Install Heroku CLI
2. Create `Procfile`:
```
web: python api/app.py
```
3. Create `runtime.txt`:
```
python-3.9.13
```
4. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Deploy to PythonAnywhere
1. Upload files to PythonAnywhere
2. Create virtual environment
3. Configure WSGI file
4. Reload web app

---

## 📊 Database Management

### Access Database
```python
import sqlite3
conn = sqlite3.connect('study_materials.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
```

### Backup Database
```bash
copy study_materials.db study_materials_backup.db
```

### Reset Database
```bash
del study_materials.db
# On next run, it will be recreated
```

---

## 🎓 Usage Scenarios

### Scenario 1: Teacher Creates Course
1. Teacher registers and logs in
2. Goes to Dashboard → Create Course
3. Fills course details and saves
4. Students can now find and enroll
5. Teacher uploads materials and creates assignments

### Scenario 2: Student Submits Assignment
1. Student enrolls in course
2. Sees assignment on dashboard
3. Clicks "Submit"
4. Uploads file or types answer
5. Teacher grades and provides feedback

### Scenario 3: Multiple Classes
1. Teacher creates multiple courses (e.g., CS101, CS201)
2. Different students in different courses
3. Each course has separate materials and grades
4. Easy to manage multiple batches

---

## 💡 Tips & Best Practices

1. **Backup Regularly**
   - Copy `study_materials.db` weekly

2. **Use Meaningful Names**
   - Course codes like "CS101", "MATH201"
   - Clear assignment titles

3. **Set Realistic Deadlines**
   - Give students enough time
   - Set dates in proper format (YYYY-MM-DD)

4. **Organize Resources**
   - Use subjects and topics
   - Categorize materials properly

5. **Communicate**
   - Use announcements for important updates
   - Reply to student queries promptly

6. **Regular Maintenance**
   - Monitor upload folder size
   - Clean old submissions periodically
   - Update course descriptions

---

## 🔗 Useful Links

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [SQLite Reference](https://www.sqlite.org/docs.html)
- [Python Docs](https://docs.python.org/3/)

---

## 📞 Support Resources

1. **Check Logs**
   - Terminal shows error messages
   - Check browser console (F12)

2. **Common Issues**
   - See Troubleshooting section above

3. **Documentation**
   - Read ADVANCED_FEATURES.md for detailed info
   - Check app.py comments for code details

---

## 🎉 You're Ready!

Your advanced dynamic learning platform is ready to use. Start by:

1. ✅ Running the app
2. ✅ Creating test accounts
3. ✅ Creating a demo course
4. ✅ Testing student/teacher workflows
5. ✅ Customizing for your needs

**Happy Teaching and Learning! 🚀**

---

*StudyHub - Advanced Learning Management System*
Version 1.0 | Last Updated: March 2024
