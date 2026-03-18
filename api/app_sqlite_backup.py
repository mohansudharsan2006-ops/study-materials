from flask import Flask, render_template, request, redirect, session, flash, jsonify
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "advanced_secret_key_2024"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'png', 'ppt', 'pptx', 'mp4', 'avi'}

# ======================================
# DATABASE SETUP - PostgreSQL
# ======================================

# Database connection parameters from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'study_materials')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DATABASE_URL = os.getenv('DATABASE_URL', f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def get_db():
    """Get PostgreSQL database connection"""
    try:
        # Try to use DATABASE_URL (for cloud deployments like Heroku)
        if DATABASE_URL and DATABASE_URL.startswith('postgresql'):
            conn = psycopg2.connect(DATABASE_URL)
        else:
            # Use individual connection parameters
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
        conn.autocommit = False
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise

def init_db():
    """Initialize PostgreSQL database with schema"""
    conn = None
    cur = None
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Create tables
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) CHECK(role IN ('student', 'teacher', 'admin')) DEFAULT 'student',
                profile_picture VARCHAR(255),
                bio TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                code VARCHAR(50) UNIQUE NOT NULL,
                description TEXT,
                department_id INTEGER REFERENCES departments(id),
                teacher_id INTEGER REFERENCES users(id),
                capacity INTEGER DEFAULT 100,
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS course_enrollments (
                id SERIAL PRIMARY KEY,
                course_id INTEGER NOT NULL REFERENCES courses(id),
                student_id INTEGER NOT NULL REFERENCES users(id),
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                grade VARCHAR(10),
                UNIQUE(course_id, student_id)
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS modules (
                id SERIAL PRIMARY KEY,
                course_id INTEGER NOT NULL REFERENCES courses(id),
                title VARCHAR(255) NOT NULL,
                description TEXT,
                order_num INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                id SERIAL PRIMARY KEY,
                module_id INTEGER NOT NULL REFERENCES modules(id),
                title VARCHAR(255) NOT NULL,
                content TEXT,
                video_url VARCHAR(255),
                file_url VARCHAR(255),
                order_num INTEGER,
                duration_minutes INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                code VARCHAR(50),
                department_id INTEGER REFERENCES departments(id),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                subject_id INTEGER REFERENCES subjects(id),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                file_path VARCHAR(255),
                video_url VARCHAR(255),
                resource_type VARCHAR(50),
                subject_id INTEGER REFERENCES subjects(id),
                topic_id INTEGER REFERENCES topics(id),
                lesson_id INTEGER REFERENCES lessons(id),
                uploaded_by INTEGER REFERENCES users(id),
                downloads INTEGER DEFAULT 0,
                is_public BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS assignments (
                id SERIAL PRIMARY KEY,
                course_id INTEGER NOT NULL REFERENCES courses(id),
                title VARCHAR(255) NOT NULL,
                description TEXT,
                file_url VARCHAR(255),
                due_date TIMESTAMP NOT NULL,
                total_points INTEGER DEFAULT 100,
                created_by INTEGER NOT NULL REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id SERIAL PRIMARY KEY,
                assignment_id INTEGER NOT NULL REFERENCES assignments(id),
                student_id INTEGER NOT NULL REFERENCES users(id),
                file_url VARCHAR(255),
                submission_text TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                score INTEGER,
                feedback TEXT,
                graded_at TIMESTAMP,
                graded_by INTEGER REFERENCES users(id),
                UNIQUE(assignment_id, student_id)
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id SERIAL PRIMARY KEY,
                course_id INTEGER NOT NULL REFERENCES courses(id),
                title VARCHAR(255) NOT NULL,
                description TEXT,
                total_questions INTEGER,
                total_points INTEGER DEFAULT 100,
                time_limit_minutes INTEGER DEFAULT 60,
                passing_score INTEGER DEFAULT 60,
                created_by INTEGER NOT NULL REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS announcements (
                id SERIAL PRIMARY KEY,
                course_id INTEGER NOT NULL REFERENCES courses(id),
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                created_by INTEGER NOT NULL REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS forum_posts (
                id SERIAL PRIMARY KEY,
                course_id INTEGER NOT NULL REFERENCES courses(id),
                created_by INTEGER NOT NULL REFERENCES users(id),
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                is_pinned BOOLEAN DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                title VARCHAR(255) NOT NULL,
                message TEXT,
                is_read BOOLEAN DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        conn.commit()
        print("✓ Database initialized successfully")
        
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Database initialization error: {e}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# ======================================
# UTILITY FUNCTIONS
# ======================================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'warning')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def check_teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'warning')
            return redirect('/login')
        conn = None
        cur = None
        try:
            conn = get_db()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('SELECT role FROM users WHERE id = %s', (session['user_id'],))
            user = cur.fetchone()
            if user and user['role'] not in ('teacher', 'admin'):
                flash('You do not have permission to access this page', 'danger')
                return redirect('/')
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        return f(*args, **kwargs)
    return decorated_function

def get_user_info():
    if 'user_id' in session:
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        db.close()
        return user
    return None


# ======================================
# HOME PAGE
# ======================================
@app.route('/')
def index():
    user = get_user_info()
    db = get_db()
    
    if user:
        if user['role'] == 'student':
            # Student dashboard
            courses = db.execute('''
                SELECT c.* FROM courses c
                JOIN course_enrollments ce ON c.id = ce.course_id
                WHERE ce.student_id = ?
            ''', (user['id'],)).fetchall()
        elif user['role'] in ('teacher', 'admin'):
            # Teacher/Admin dashboard
            courses = db.execute('SELECT * FROM courses WHERE teacher_id = ? OR ?', 
                                (user['id'], user['role'] == 'admin')).fetchall()
        else:
            courses = []
    else:
        courses = []
        # Show statistics for non-logged in users
        total_courses = db.execute('SELECT COUNT(*) FROM courses').fetchone()[0]
        total_users = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        total_resources = db.execute('SELECT COUNT(*) FROM resources').fetchone()[0]
    
    db.close()
    return render_template('index.html', user=user, courses=courses)

# ======================================
# AUTHENTICATION ROUTES
# ======================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        role = request.form.get('role', 'student')

        if not all([name, email, password, password_confirm]):
            flash('All fields are required', 'danger')
            return redirect('/register')

        if password != password_confirm:
            flash('Passwords do not match', 'danger')
            return redirect('/register')

        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect('/register')

        db = get_db()
        try:
            hashed_pwd = hash_password(password)
            db.execute(
                'INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)',
                (name, email, hashed_pwd, role)
            )
            db.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            db.rollback()
            flash('Email already exists', 'danger')
            return redirect('/register')
        finally:
            db.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Email and password required', 'danger')
            return redirect('/login')

        db = get_db()
        hashed_pwd = hash_password(password)
        user = db.execute(
            'SELECT * FROM users WHERE email = ? AND password = ?',
            (email, hashed_pwd)
        ).fetchone()
        db.close()

        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']
            flash(f'Welcome {user["name"]}!', 'success')
            return redirect('/')
        else:
            flash('Invalid email or password', 'danger')
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect('/')

# ======================================
# STUDENT DASHBOARD
# ======================================

@app.route('/dashboard/student')
@check_login_required
def student_dashboard():
    if session.get('role') != 'student':
        return redirect('/')
    
    db = get_db()
    user_id = session['user_id']
    
    # Get enrolled courses
    courses = db.execute('''
        SELECT c.*, COUNT(DISTINCT a.id) as assignments_count
        FROM courses c
        LEFT JOIN course_enrollments ce ON c.id = ce.course_id
        LEFT JOIN assignments a ON c.id = a.course_id
        WHERE ce.student_id = ?
        GROUP BY c.id
    ''', (user_id,)).fetchall()
    
    # Get pending assignments
    pending_assignments = db.execute('''
        SELECT a.*, c.name as course_name
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        JOIN course_enrollments ce ON c.id = ce.course_id
        WHERE ce.student_id = ? AND a.due_date > datetime('now')
        ORDER BY a.due_date ASC
        LIMIT 5
    ''', (user_id,)).fetchall()
    
    # Get announcements
    announcements = db.execute('''
        SELECT a.*, c.name as course_name, u.name as created_by_name
        FROM announcements a
        JOIN courses c ON a.course_id = c.id
        JOIN course_enrollments ce ON c.id = ce.course_id
        JOIN users u ON a.created_by = u.id
        WHERE ce.student_id = ?
        ORDER BY a.created_at DESC
        LIMIT 10
    ''', (user_id,)).fetchall()
    
    db.close()
    return render_template('dashboard_student.html', courses=courses, 
                         pending_assignments=pending_assignments, 
                         announcements=announcements)

# ======================================
# TEACHER DASHBOARD
# ======================================

@app.route('/dashboard/teacher')
@check_teacher_required
def teacher_dashboard():
    db = get_db()
    user_id = session['user_id']
    
    # Get courses taught by this teacher
    courses = db.execute('''
        SELECT c.*, COUNT(DISTINCT ce.student_id) as enrolled_students
        FROM courses c
        LEFT JOIN course_enrollments ce ON c.id = ce.course_id
        WHERE c.teacher_id = ?
        GROUP BY c.id
    ''', (user_id,)).fetchall()
    
    # Get pending assignments to grade
    pending_submissions = db.execute('''
        SELECT s.*, a.title as assignment_title, c.name as course_name, u.name as student_name
        FROM submissions s
        JOIN assignments a ON s.assignment_id = a.id
        JOIN courses c ON a.course_id = c.id
        JOIN users u ON s.student_id = u.id
        WHERE a.created_by = ? AND s.score IS NULL
        ORDER BY s.submitted_at ASC
    ''', (user_id,)).fetchall()
    
    db.close()
    return render_template('dashboard_teacher.html', courses=courses, 
                         pending_submissions=pending_submissions)

# ======================================
# COURSES ROUTES
# ======================================

@app.route('/courses')
def view_courses():
    db = get_db()
    courses = db.execute('''
        SELECT c.*, d.name as department_name, u.name as teacher_name
        FROM courses c
        LEFT JOIN departments d ON c.department_id = d.id
        LEFT JOIN users u ON c.teacher_id = u.id
        WHERE c.status = 'active'
    ''').fetchall()
    db.close()
    return render_template('courses.html', courses=courses)

@app.route('/course/<int:course_id>')
def view_course(course_id):
    db = get_db()
    course = db.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
    
    if not course:
        flash('Course not found', 'danger')
        return redirect('/courses')
    
    # Get modules and lessons
    modules = db.execute('''
        SELECT m.*, COUNT(DISTINCT l.id) as lesson_count
        FROM modules m
        LEFT JOIN lessons l ON m.id = l.module_id
        WHERE m.course_id = ?
        GROUP BY m.id
        ORDER BY m.order_num
    ''', (course_id,)).fetchall()
    
    # Get announcements
    announcements = db.execute('''
        SELECT a.*, u.name as created_by_name
        FROM announcements a
        JOIN users u ON a.created_by = u.id
        WHERE a.course_id = ?
        ORDER BY a.created_at DESC
    ''', (course_id,)).fetchall()
    
    db.close()
    
    user = get_user_info()
    is_enrolled = False
    is_teacher = False
    
    if user:
        db = get_db()
        if user['role'] in ('teacher', 'admin'):
            is_teacher = (user['id'] == course['teacher_id'])
        else:
            enrollment = db.execute(
                'SELECT * FROM course_enrollments WHERE course_id = ? AND student_id = ?',
                (course_id, user['id'])
            ).fetchone()
            is_enrolled = enrollment is not None
        db.close()
    
    return render_template('course_detail.html', course=course, modules=modules, 
                         announcements=announcements, is_enrolled=is_enrolled, 
                         is_teacher=is_teacher)

@app.route('/course/<int:course_id>/enroll', methods=['POST'])
@check_login_required
def enroll_course(course_id):
    if session.get('role') != 'student':
        flash('Only students can enroll in courses', 'danger')
        return redirect(f'/course/{course_id}')
    
    db = get_db()
    try:
        db.execute(
            'INSERT INTO course_enrollments (course_id, student_id) VALUES (?, ?)',
            (course_id, session['user_id'])
        )
        db.commit()
        flash('Successfully enrolled in course!', 'success')
    except sqlite3.IntegrityError:
        flash('Already enrolled in this course', 'info')
    finally:
        db.close()
    
    return redirect(f'/course/{course_id}')

@app.route('/create-course', methods=['GET', 'POST'])
@check_teacher_required
def create_course():
    db = get_db()
    departments = db.execute('SELECT * FROM departments').fetchall()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        code = request.form.get('code', '').strip()
        description = request.form.get('description', '').strip()
        department_id = request.form.get('department_id')
        capacity = request.form.get('capacity', 100)
        
        try:
            db.execute('''
                INSERT INTO courses (name, code, description, department_id, teacher_id, capacity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, code, description, department_id, session['user_id'], capacity))
            db.commit()
            flash('Course created successfully!', 'success')
            return redirect('/dashboard/teacher')
        except sqlite3.IntegrityError:
            flash('Course code already exists', 'danger')
    
    db.close()
    return render_template('create_course.html', departments=departments)

# ======================================
# ASSIGNMENTS ROUTES
# ======================================

@app.route('/course/<int:course_id>/assignments')
def view_assignments(course_id):
    db = get_db()
    course = db.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
    
    if not course:
        return redirect('/courses')
    
    assignments = db.execute('''
        SELECT *, 
               (SELECT COUNT(*) FROM submissions WHERE assignment_id = assignments.id) as submission_count,
               (SELECT COUNT(*) FROM submissions WHERE assignment_id = assignments.id AND score IS NOT NULL) as graded_count
        FROM assignments
        WHERE course_id = ?
        ORDER BY due_date DESC
    ''', (course_id,)).fetchall()
    
    db.close()
    user = get_user_info()
    is_teacher = user and (user['id'] == course['teacher_id'] or user['role'] == 'admin')
    
    return render_template('assignments.html', course=course, assignments=assignments, is_teacher=is_teacher)

@app.route('/create-assignment/<int:course_id>', methods=['GET', 'POST'])
@check_teacher_required
def create_assignment(course_id):
    db = get_db()
    course = db.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
    
    if not course or (course['teacher_id'] != session['user_id'] and session.get('role') != 'admin'):
        return redirect('/courses')
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date = request.form.get('due_date')
        total_points = request.form.get('total_points', 100)
        
        file = request.files.get('file')
        file_url = None
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = filename
        
        db.execute('''
            INSERT INTO assignments (course_id, title, description, file_url, due_date, total_points, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (course_id, title, description, file_url, due_date, total_points, session['user_id']))
        db.commit()
        db.close()
        
        flash('Assignment created successfully!', 'success')
        return redirect(f'/course/{course_id}/assignments')
    
    db.close()
    return render_template('create_assignment.html', course=course)

@app.route('/assignment/<int:assignment_id>/submit', methods=['GET', 'POST'])
@check_login_required
def submit_assignment(assignment_id):
    if session.get('role') != 'student':
        return redirect('/')
    
    db = get_db()
    assignment = db.execute('''
        SELECT a.*, c.id as course_id FROM assignments a
        JOIN courses c ON a.course_id = c.id
        WHERE a.id = ?
    ''', (assignment_id,)).fetchone()
    
    if not assignment:
        flash('Assignment not found', 'danger')
        return redirect('/courses')
    
    # Check if student is enrolled
    enrolled = db.execute('''
        SELECT * FROM course_enrollments
        WHERE course_id = ? AND student_id = ?
    ''', (assignment['course_id'], session['user_id'])).fetchone()
    
    if not enrolled:
        flash('You are not enrolled in this course', 'danger')
        return redirect('/courses')
    
    # Check existing submission
    submission = db.execute('''
        SELECT * FROM submissions
        WHERE assignment_id = ? AND student_id = ?
    ''', (assignment_id, session['user_id'])).fetchone()
    
    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        file = request.files.get('file')
        file_url = None
        
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{session['user_id']}_{assignment_id}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = filename
        
        if submission:
            # Update existing submission
            db.execute('''
                UPDATE submissions
                SET submission_text = ?, file_url = ?, submitted_at = datetime('now')
                WHERE id = ?
            ''', (submission_text, file_url or submission['file_url'], submission['id']))
            flash('Submission updated!', 'success')
        else:
            # Create new submission
            db.execute('''
                INSERT INTO submissions (assignment_id, student_id, submission_text, file_url)
                VALUES (?, ?, ?, ?)
            ''', (assignment_id, session['user_id'], submission_text, file_url))
            flash('Assignment submitted successfully!', 'success')
        
        db.commit()
        return redirect(f'/course/{assignment["course_id"]}/assignments')
    
    db.close()
    return render_template('submit_assignment.html', assignment=assignment, submission=submission)

@app.route('/assignment/<int:assignment_id>/submissions')
@check_teacher_required
def view_submissions(assignment_id):
    db = get_db()
    assignment = db.execute('''
        SELECT a.*, c.id as course_id, u.name as teacher_name
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        JOIN users u ON a.created_by = u.id
        WHERE a.id = ?
    ''', (assignment_id,)).fetchone()
    
    if not assignment or (assignment['created_by'] != session['user_id'] and session.get('role') != 'admin'):
        return redirect('/courses')
    
    submissions = db.execute('''
        SELECT s.*, u.name as student_name
        FROM submissions s
        JOIN users u ON s.student_id = u.id
        WHERE s.assignment_id = ?
        ORDER BY s.submitted_at DESC
    ''', (assignment_id,)).fetchall()
    
    db.close()
    return render_template('submissions.html', assignment=assignment, submissions=submissions)

@app.route('/submission/<int:submission_id>/grade', methods=['GET', 'POST'])
@check_teacher_required
def grade_submission(submission_id):
    db = get_db()
    submission = db.execute('''
        SELECT s.*, a.total_points, u.name as student_name, a2.name as course_name, c.teacher_id
        FROM submissions s
        JOIN assignments a ON s.assignment_id = a.id
        JOIN courses c ON a.course_id = c.id
        JOIN users u ON s.student_id = u.id
        JOIN assignments a2 ON s.assignment_id = a2.id
        WHERE s.id = ?
    ''', (submission_id,)).fetchone()
    
    if not submission or (submission['teacher_id'] != session['user_id'] and session.get('role') != 'admin'):
        return redirect('/')
    
    if request.method == 'POST':
        score = request.form.get('score')
        feedback = request.form.get('feedback', '').strip()
        
        db.execute('''
            UPDATE submissions
            SET score = ?, feedback = ?, graded_at = datetime('now'), graded_by = ?
            WHERE id = ?
        ''', (score, feedback, session['user_id'], submission_id))
        db.commit()
        
        flash('Submission graded successfully!', 'success')
        return redirect(f'/assignment/{submission["assignment_id"]}/submissions')
    
    db.close()
    return render_template('grade_submission.html', submission=submission)

# ======================================
# RESOURCES/MATERIALS ROUTES
# ======================================

@app.route('/resources')
def view_resources():
    db = get_db()
    subjects = db.execute('SELECT * FROM subjects').fetchall()
    resources = db.execute('''
        SELECT r.*, s.name as subject_name, u.name as uploaded_by_name
        FROM resources r
        LEFT JOIN subjects s ON r.subject_id = s.id
        LEFT JOIN users u ON r.uploaded_by = u.id
        WHERE r.is_public = 1
        ORDER BY r.created_at DESC
    ''').fetchall()
    db.close()
    return render_template('resources.html', resources=resources, subjects=subjects)

@app.route('/upload-resource', methods=['GET', 'POST'])
@check_teacher_required
def upload_resource():
    db = get_db()
    subjects = db.execute('SELECT * FROM subjects').fetchall()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        resource_type = request.form.get('resource_type')
        subject_id = request.form.get('subject_id') or None
        video_url = request.form.get('video_url', '').strip() or None
        
        file = request.files.get('file')
        file_path = None
        
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{session['user_id']}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = filename
        
        db.execute('''
            INSERT INTO resources (title, description, file_path, video_url, resource_type, subject_id, uploaded_by, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        ''', (title, description, file_path, video_url, resource_type, subject_id, session['user_id']))
        db.commit()
        
        flash('Resource uploaded successfully!', 'success')
        return redirect('/resources')
    
    db.close()
    return render_template('upload_resource.html', subjects=subjects)

# ======================================
# PROFILE ROUTES
# ======================================

@app.route('/profile')
@check_login_required
def profile():
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    db.close()
    return render_template('profile.html', user=user)

@app.route('/profile/edit', methods=['GET', 'POST'])
@check_login_required
def edit_profile():
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        bio = request.form.get('bio', '').strip()
        
        db.execute(
            'UPDATE users SET name = ?, bio = ? WHERE id = ?',
            (name, bio, session['user_id'])
        )
        db.commit()
        session['name'] = name
        
        flash('Profile updated successfully!', 'success')
        return redirect('/profile')
    
    db.close()
    return render_template('edit_profile.html', user=user)

# ======================================
# ERROR HANDLERS
# ======================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ======================================
# BEFORE REQUEST
# ======================================

@app.before_request
def before_request():
    """Initialize database and make user available to templates"""
    init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)