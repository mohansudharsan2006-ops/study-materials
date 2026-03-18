# StudyHub - Advanced Dynamic Learning Platform

![StudyHub](https://img.shields.io/badge/StudyHub-v1.0-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![Flask](https://img.shields.io/badge/Flask-3.0+-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-informational)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205-purple)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Routes](#api-routes)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## 📖 Overview

StudyHub is a comprehensive, advanced learning management system (LMS) that transforms a static website into a dynamic, interactive platform for collaborative learning. It enables teachers to create courses, post materials, and manage assignments while allowing students to enroll, submit work, and track their progress.

### Evolution from Static to Dynamic
✅ **Before:** Basic static content pages (Discrete Math, Digital Electronics, etc.)
✅ **After:** Full-featured LMS with user authentication, course management, assignments, grading, and more

---

## ✨ Key Features

### 1. **User Authentication & Authorization**
- Secure registration with email verification support
- Role-based access control (Student, Teacher, Admin)
- Session management
- Password hashing with SHA256
- Profile management with bio and picture support

### 2. **Course Management System**
- Create and manage courses with codes, descriptions, and capacity
- Organize courses by departments
- Student enrollment tracking
- Course announcements
- Multiple module organization
- Lesson management with video support

### 3. **Assignment Management**
- Create assignments with due dates and point values
- File attachment support for assignment files
- Student assignment submission with file uploads or text
- Automatic submission tracking
- Teacher grading interface with score and feedback
- Late submission monitoring

### 4. **Resource Library**
- Upload study materials (PDF, DOC, PPT, images, videos)
- Organize by subjects and topics
- Public/private resource control
- Download tracking and statistics
- Resource categorization

### 5. **Comprehensive Dashboards**
- **Student Dashboard:** Enrolled courses, pending assignments, announcements
- **Teacher Dashboard:** Courses taught, student enrollment, pending submissions to grade
- **Statistics & Analytics:** Course stats, student progress, resource usage

### 6. **Discussion & Collaboration**
- Course announcements
- Discussion forum framework
- Comment and reply functionality

### 7. **Quiz System** (Framework Ready)
- Create quizzes with multiple question types
- Time-limited testing
- Automatic grading
- Student performance tracking

### 8. **Advanced Features**
- Notifications system
- Grade tracking and reporting
- Student progress analytics
- File upload with virus scanning support (extensible)
- Backup and recovery features

---

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask (Python 3.7+) |
| **Database** | SQLite 3 (upgradeable to PostgreSQL/MySQL) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **UI Framework** | Bootstrap 5 |
| **Icons** | Bootstrap Icons |
| **ORM** | SQLite3 native + Row Factory |
| **Authentication** | Session-based with hashing |
| **File Upload** | Werkzeug with validation |

---

## 📦 Installation

### Prerequisites
```
- Python 3.7 or higher
- pip (Python package manager)
- Git (optional)
```

### Step-by-Step Setup

1. **Clone or Download Project**
```bash
cd f:\study materials
```

2. **Create Virtual Environment** (if not already done)
```bash
python -m venv venv
```

3. **Activate Virtual Environment**
```bash
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

4. **Install Dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the Application**
```bash
python api/app.py
```

6. **Access the Platform**
```
Open browser and go to: http://localhost:5000
```

---

## 🚀 Usage

### First Login
1. Click "Register" in top navigation
2. Choose role: Student or Teacher
3. Fill in details and create account
4. Login with your credentials

### For Students
```
1. Enroll in courses from /courses
2. View Dashboard at /dashboard/student
3. Check assignments and deadlines
4. Submit assignments before due date
5. Track grades and feedback
```

### For Teachers
```
1. Create courses from /dashboard/teacher
2. Add course materials and resources
3. Create assignments with deadlines
4. Review student submissions
5. Grade and provide feedback
6. View course statistics
```

### For Admins
```
- Access all teacher functions
- View system-wide statistics
- Manage users and departments
- System administration
```

---

## 📁 Project Structure

```
f:\study materials\
│
├── api/
│   └── app.py                          # Main Flask application (850+ lines)
│       ├── Database setup & utilities
│       ├── Authentication routes
│       ├── Course management
│       ├── Assignment handling
│       ├── Resource management
│       ├── Profile management
│       └── Error handlers
│
├── templates/
│   ├── base.html                       # Base template with navigation
│   ├── base_*.html                     # Deprecated templates
│   ├── index_new.html                  # Home page
│   ├── login_new.html                  # Login page
│   ├── register_new.html               # Registration page
│   ├── courses_new.html                # Course listing
│   ├── course_detail.html              # Course details (template ready)
│   ├── dashboard_student_new.html      # Student dashboard
│   ├── dashboard_teacher_new.html      # Teacher dashboard
│   ├── assignments.html                # Assignment listing (template ready)
│   ├── create_assignment.html          # Create assignment (template ready)
│   ├── submit_assignment.html          # Submit assignment (template ready)
│   ├── submissions.html                # Grade submissions (template ready)
│   ├── grade_submission.html           # Grading interface (template ready)
│   ├── profile_new.html                # User profile
│   ├── edit_profile.html               # Edit profile (template ready)
│   ├── resources.html                  # Resources library (template ready)
│   ├── upload_resource.html            # Upload resources (template ready)
│   └── 404_new.html                    # Error page
│
├── database/
│   ├── database.sql                    # Original MySQL schema
│   └── advanced_schema.sql             # New PostgreSQL schema
│
├── static/
│   └── static.css                      # Stylesheet
│
├── uploads/                            # User file uploads
│   ├── assignment_*.pdf
│   ├── resource_*.doc
│   └── ...
│
├── ADVANCED_FEATURES.md                # Detailed feature documentation
├── QUICK_START.md                      # Quick start guide
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
└── study_materials.db                  # SQLite database (auto-created)
```

---

## 🗄️ Database Schema

### Core Tables (14 total)

| Table | Purpose | Records |
|-------|---------|---------|
| **users** | User accounts and authentication | Students, Teachers, Admins |
| **departments** | Academic departments | Computer Science, IT, etc. |
| **courses** | Course information | Multiple courses per teacher |
| **course_enrollments** | Student-course relationships | Enrollment tracking |
| **modules** | Course module organization | Grouped content |
| **lessons** | Individual lessons | Video, content, duration |
| **subjects** | Subject organization | Course subjects |
| **topics** | Topic organization | Subject topics |
| **resources** | Study materials | PDFs, videos, documents |
| **assignments** | Course assignments | Due dates, points |
| **submissions** | Student work submissions | Grade tracking |
| **quizzes** | Quiz definitions | Quiz questions |
| **announcements** | Course announcements | Course notifications |
| **forum_posts** | Discussion posts | Student-teacher discussion |
| **notifications** | User notifications | Real-time alerts |

### Key Relationships
```
User (1) --- (Many) Courses
Course (1) --- (Many) Enrollments --- (Many) Students
Course (1) --- (Many) Assignments --- (Many) Submissions
Course (1) --- (Many) Modules --- (Many) Lessons
```

---

## 🔌 API Routes

### Authentication Routes
```
POST   /register          - Create new account
POST   /login             - User login
GET    /logout            - End session
```

### Course Routes
```
GET    /courses                    - List all courses
GET    /course/<id>                - View course details
POST   /course/<id>/enroll         - Enroll in course
POST   /create-course              - Create new course [Teacher]
```

### Assignment Routes
```
GET    /course/<id>/assignments               - List assignments
POST   /create-assignment/<id>                - Create assignment [Teacher]
GET    /assignment/<id>/submit                - Submit assignment page
POST   /assignment/<id>/submit                - Submit assignment
GET    /assignment/<id>/submissions           - View submissions [Teacher]
GET    /submission/<id>/grade                 - Grade submission [Teacher]
POST   /submission/<id>/grade                 - Submit grade [Teacher]
```

### Resource Routes
```
GET    /resources             - Browse resources
POST   /upload-resource       - Upload resource [Teacher]
```

### User Routes
```
GET    /profile              - View profile
POST   /profile/edit         - Update profile
GET    /dashboard/student    - Student dashboard [Student]
GET    /dashboard/teacher    - Teacher dashboard [Teacher]
```

### Home Routes
```
GET    /                     - Homepage
```

---

## 🔐 Security Features

### Authentication
- ✅ Secure password hashing (SHA256)
- ✅ Session-based authentication
- ✅ CSRF protection via Flask sessions
- ✅ Role-based access control decorators

### Data Protection
- ✅ SQL injection prevention (parameterized queries)
- ✅ Input validation on forms
- ✅ File type validation for uploads
- ✅ File size limits (50MB max)

### Access Control
- ✅ Login required decorators
- ✅ Role verification for protected routes
- ✅ Teacher-only course management
- ✅ Student-only enrollment

---

## 📊 Statistics & Metrics

### Supported Metrics
- Active courses count
- Enrolled students count
- Assignment submission rates
- Resource download statistics
- User registration trends
- Course popularity

### Dashboard Displays
- Student pending assignments
- Recent announcements
- Course enrollment status
- Grade distribution
- Submission status

---

## 🚀 Deployment

### Local Development
```bash
python api/app.py
# Runs on http://localhost:5000
```

### Deploy to Heroku
```bash
# Create Procfile
echo "web: python api/app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Deploy to PythonAnywhere
1. Upload files to account
2. Set up virtual environment
3. Configure WSGI
4. Enable Web app

### Deploy to AWS
1. Use EC2 instance
2. Set up environment
3. Use Gunicorn + Nginx
4. Configure RDS (optional)

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "api/app.py"]
```

---

## 🧪 Testing

### Manual Testing Checklist
```
□ User Registration (Student & Teacher)
□ Login/Logout functionality
□ Create Course (Teacher)
□ Enroll in Course (Student)
□ Create Assignment (Teacher)
□ Submit Assignment (Student)
□ Grade Submission (Teacher)
□ Upload Resources
□ View Dashboard
□ View Profile & Edit
□ File Upload/Download
□ Error Handling (404, 500)
```

### Sample Test Data
```python
# Demo Credentials
Student: student@example.com / password123
Teacher: teacher@example.com / password123
Admin:   admin@example.com / password123

# Sample Departments
- Computer Science
- Information Technology
- Electronics & Communication
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Flask module not found | Activate venv and install: `pip install flask` |
| Address already in use | Change port: `app.run(port=5001)` |
| Database errors | Delete `study_materials.db` to reset |
| File upload failing | Ensure `uploads/` folder exists |
| Templates not found | Check template file names match in app.py |

---

## 📈 Performance Optimization

### Database
- ✅ Indexed queries on frequently accessed columns
- ✅ Foreign keys for referential integrity
- ✅ Efficient table structure

### Frontend
- ✅ Bootstrap CDN for fast loading
- ✅ Minified CSS/JS
- ✅ Responsive design for all devices

### File Handling
- ✅ File size restrictions
- ✅ Secure filename generation
- ✅ Upload validation

---

## 🔄 Future Enhancements

### Planned Features
- [ ] Video streaming integration
- [ ] Real-time chat support
- [ ] Mobile app
- [ ] API documentation (Swagger)
- [ ] Advanced analytics dashboard
- [ ] Payment integration
- [ ] Email notifications
- [ ] Two-factor authentication
- [ ] OAuth integration (Google, GitHub)
- [ ] Machine learning recommendations

### Data Export
- [ ] Export grades to CSV
- [ ] Generate certificates
- [ ] Progress reports
- [ ] Analytics export

---

## 📚 Documentation

### Available Docs
- **ADVANCED_FEATURES.md** - Detailed feature list and architecture
- **QUICK_START.md** - User guide and troubleshooting
- **README.md** - This file (project overview)
- **Code Comments** - Inline documentation in app.py

---

## 📧 Support

### Getting Help
1. Check QUICK_START.md for common issues
2. Review app.py comments for code details
3. Check error messages in terminal
4. Verify file permissions and paths

### Reporting Issues
1. Note the specific error message
2. Include steps to reproduce
3. Check error logs
4. Provide environment details

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👥 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 🎓 Learning Resources

### Related Topics
- Flask Web Development: https://flask.palletsprojects.com/
- SQLite Tutorial: https://www.sqlite.org/lang.html
- Bootstrap Documentation: https://getbootstrap.com/docs/
- Python Best Practices: https://peps.python.org/

---

## 🏆 Achievements

✅ Converted static website to dynamic LMS
✅ Implemented user authentication
✅ Built course management system
✅ Created assignment tracking
✅ Developed teacher grading interface
✅ Resource library with categorization
✅ Responsive modern UI with Bootstrap
✅ Scalable database architecture
✅ Deployment-ready application

---

## 📞 Contact & Support

**Project:** StudyHub - Advanced Learning Management System
**Version:** 1.0
**Last Updated:** March 2024
**Maintainer:** Your Name

For questions or support, please reach out through:
- Email: support@studyhub.com
- GitHub Issues: [Link to repo issues]
- Documentation: See ADVANCED_FEATURES.md

---

## 🙏 Acknowledgments

- Flask community for excellent framework
- Bootstrap team for beautiful UI framework
- Contributors and testers

---

**Happy Learning! 🚀**

*StudyHub - Making Education Accessible and Interactive*
