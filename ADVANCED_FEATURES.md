# 🎓 StudyHub - Advanced Dynamic Learning Platform

## ✨ Features Implemented

### 1. **Role-Based Access Control**
   - **Students**: Can enroll in courses, submit assignments, take quizzes, and access resources
   - **Teachers**: Can create and manage courses, upload materials, create assignments, and grade submissions
   - **Admin**: Full platform management capabilities

### 2. **Course Management System**
   - Create and manage multiple courses
   - Organize courses by departments
   - Course descriptions, codes, and capacity limits
   - Track enrolled students per course
   - Course announcements and discussion forums

### 3. **Advanced Learning Features**

   #### Courses & Modules
   - Hierarchical course structure with modules and lessons
   - Organize content logically
   - Embedded video support
   - Duration tracking for lessons

   #### Assignments System
   - Teachers create assignments with due dates
   - Students submit assignments with file uploads and text
   - Grading system for teachers
   - Score tracking and feedback
   - Automatic submission tracking

   #### Quizzes (Framework Ready)
   - Create quizzes for courses
   - Multiple question types support
   - Time-limited testing
   - Automatic grading capabilities
   - Student performance tracking

   #### Resources Library
   - Upload study materials (PDFs, documents, videos)
   - Organize by subjects and topics
   - Public/private resource control
   - Download tracking
   - Resource metadata (title, description, type)

### 4. **Student Dashboard**
   - Overview of enrolled courses
   - Pending assignments with due dates
   - Recent announcements
   - Quick course access
   - Progress tracking

### 5. **Teacher Dashboard**
   - Course management overview
   - Student enrollment stats
   - Pending submissions to grade
   - Course statistics
   - Bulk assignment creation

### 6. **User Management**
   - Secure registration with password confirmation
   - Email-based login system
   - User profiles with:
     - Name and email
     - Bio/description
     - Profile picture support (framework)
     - Account type (Student/Teacher)
   - Profile editing capabilities
   - Session management

### 7. **Database Features**
   - SQLite database with comprehensive schema
   - 14+ interconnected tables
   - Foreign key relationships
   - Indexed queries for performance
   - Includes:
     - Users (with roles)
     - Departments & Subjects
     - Courses & Enrollments
     - Modules & Lessons
     - Assignments & Submissions
     - Quizzes & Questions
     - Announcements & Forum
     - Resources & Downloads
     - Notifications

## 📁 Project Structure

```
study materials/
├── api/
│   └── app.py                 # Flask application with all routes
├── templates/
│   ├── base.html             # Base template with navigation
│   ├── index_new.html        # Home page with statistics
│   ├── login_new.html        # Student/Teacher login
│   ├── register_new.html     # Registration with role selection
│   ├── courses_new.html      # Browse all courses
│   ├── dashboard_student_new.html  # Student dashboard
│   ├── dashboard_teacher_new.html  # Teacher dashboard
│   ├── profile_new.html      # User profile page
│   └── 404_new.html          # Error page
├── database/
│   ├── database.sql          # Original schema
│   └── advanced_schema.sql   # New PostgreSQL schema
├── static/
│   └── static.css            # Styling
├── uploads/                  # File upload directory
└── requirements.txt          # Python dependencies

```

## 🚀 Key Routes

### Public Routes
- `/` - Home page
- `/login` - Student/Teacher login
- `/register` - New account registration
- `/courses` - Browse available courses
- `/resources` - Study materials library

### Student Routes (Protected)
- `/dashboard/student` - Student dashboard
- `/course/<id>` - View course details
- `/course/<id>/enroll` - Enroll in course
- `/course/<id>/assignments` - View assignments
- `/assignment/<id>/submit` - Submit assignment
- `/profile` - View profile
- `/profile/edit` - Edit profile

### Teacher Routes (Protected)
- `/dashboard/teacher` - Teacher dashboard
- `/create-course` - Create new course
- `/upload-resource` - Upload study material
- `/course/<id>/assignments` - Manage assignments
- `/create-assignment/<id>` - Create assignment
- `/assignment/<id>/submissions` - View student submissions
- `/submission/<id>/grade` - Grade a submission

### Authentication
- `/logout` - End session

## 🔐 Security Features

- **Password Hashing**: SHA256 encryption for passwords
- **Session Management**: Secure session handling
- **Role-Based Access**: Protected routes with decorators
- **File Upload Validation**: Allowed file types validation
- **CSRF Protection**: Flask session security
- **File Size Limits**: 50MB maximum file size

## 📊 Database Schema Highlights

### Users Table
- ID, Name, Email (unique), Hashed Password
- Role (student/teacher/admin)
- Bio, Creation timestamp

### Courses Table
- Course code (unique)
- Department association
- Teacher assignment
- Student capacity
- Status tracking (active/inactive)

### Assignments Table
- Title and description
- Due dates
- Total points
- File attachments
- Creation tracking

### Submissions Table
- Assignment reference
- Student reference
- File/text submission
- Score and feedback
- Grading information

## 🔧 Configuration

Edit constraints in `app.py`:
```python
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'png', 'ppt', 'pptx', 'mp4', 'avi'}
```

## 🎯 Advanced Features Ready for Expansion

1. **Discussion Forums**: Framework built - replies structure ready
2. **Notifications System**: Table created for real-time alerts
3. **Quiz System**: Complete structure for automated testing
4. **Lesson Analytics**: Track student engagement and progress
5. **Attendance Tracking**: Basic framework for classroom management

## 💾 Database Initialization

The database is automatically created on first run with:
- All required tables
- Foreign key relationships
- Proper indexing
- Default departments and subjects

## 🎨 UI/UX Features

- **Responsive Design**: Bootstrap 5 framework
- **Modern UI**: Clean, professional interface
- **Flash Messages**: User-friendly notifications
- **Navigation**: Intuitive menu structure
- **Card-Based Layouts**: Organized content presentation
- **Icons**: Bootstrap Icons integration

## 📈 Scalability Features

- SQLite database (easily upgradable to PostgreSQL/MySQL)
- Indexed database queries
- Organized file structure
- Modular route definitions
- Reusable templates

## 🛠 Deployment Ready

The platform can be deployed to:
- Heroku (with Procfile)
- PythonAnywhere
- AWS
- DigitalOcean
- Vercel (already in project)

## 📝 Next Steps

1. **Test the application** - Run the app and test all features
2. **Customize branding** - Update logos and colors
3. **Add more resources** - Create initial courses and materials
4. **Enable email notifications** - Add email integration
5. **Implement payment system** - For paid courses (optional)

## 🚀 Running the Application

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies (if needed)
pip install -r requirements.txt

# Run the Flask app
python api\app.py
```

The app will run at `http://localhost:5000`

## 📞 Support

For issues or questions:
1. Check the error logs in terminal
2. Verify database file exists: `study_materials.db`
3. Ensure all dependencies are installed
4. Check file upload permissions

---

**StudyHub** - Advanced Learning Management System v1.0
Created with Flask, SQLite, and Bootstrap 5
