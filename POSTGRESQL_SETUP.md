# PostgreSQL Setup Guide for StudyHub LMS

This guide will help you connect your StudyHub LMS application to PostgreSQL.

## 📋 Prerequisites

- PostgreSQL 12+ installed on your system
- Python 3.7+
- Virtual environment activated (from the project root)

## 🚀 Quick Setup (Windows)

### Step 1: Install PostgreSQL

1. Download from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer
3. Remember the password you set for the `postgres` user
4. Keep the default port: **5432**
5. During installation, pgAdmin 4 will be installed (useful for database management)

### Step 2: Create Database and User

Open **pgAdmin 4** or **SQL Shell** (psql):

```sql
-- Open SQL Shell (psql) from Start Menu

-- Create database
CREATE DATABASE study_materials;

-- Create user (better practice than using postgres directly)
CREATE USER studyhub WITH PASSWORD 'your_secure_password';

-- Grant privileges
ALTER ROLE studyhub SET client_encoding TO 'utf8';
ALTER ROLE studyhub SET default_transaction_isolation TO 'read committed';
ALTER ROLE studyhub SET default_transaction_deferrable TO on;
ALTER ROLE studyhub SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE study_materials TO studyhub;

-- Connect to the database and grant schema privileges
\c study_materials
GRANT ALL PRIVILEGES ON SCHEMA public TO studyhub;
```

### Step 3: Update Dependencies

In your project directory, the dependencies have already been updated:

```bash
# Verify psycopg2 is in requirements.txt
pip install -r requirements.txt
```

The key packages added:
- `psycopg2-binary==2.9.11` - PostgreSQL adapter for Python
- `python-dotenv==1.0.0` - For loading environment variables

### Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` with your PostgreSQL credentials:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=study_materials
   DB_USER=studyhub
   DB_PASSWORD=your_secure_password
   ```

### Step 5: Initialize Database

Run the Flask app to initialize the database:

```bash
python api/app.py
```

The app will:
1. Connect to PostgreSQL
2. Create all required tables automatically
3. Print: "✓ Database initialized successfully"

### Step 6: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 🔄 Switching from SQLite to PostgreSQL

The application has been updated to support PostgreSQL:

### Key Changes Made:

1. **Imports Updated**
   - Removed: `import sqlite3`
   - Added: `import psycopg2`
   - Added: `from psycopg2.extras import RealDictCursor`
   - Added: `from dotenv import load_dotenv`

2. **Database Connection**
   - Old: SQLite file-based connection
   - New: PostgreSQL with environment variable configuration
   - Supports both `DATABASE_URL` and individual parameters

3. **SQL Syntax Changes**
   - `?` placeholders → `%s` placeholders
   - `AUTOINCREMENT` → `SERIAL`
   - `TEXT` → `VARCHAR(255)` where appropriate
   - `BOOLEAN DEFAULT 1` → `BOOLEAN DEFAULT true`

4. **Cursor Management**
   - Uses `RealDictCursor` for dict-like access
   - Proper connection and cursor closing in try-finally blocks

## 🌐 Cloud Deployment (Heroku, Railway, Render)

For cloud deployments, use the `DATABASE_URL` environment variable:

### Heroku Example:
```bash
# The DATABASE_URL is automatically set by Heroku when you add PostgreSQL
# App will automatically detect and use it
heroku config | grep DATABASE_URL
```

### Railway or Render Example:
```bash
# Set the DATABASE_URL environment variable in your deployment settings
# Format: postgresql://username:password@host:port/database
```

The app will automatically detect and use `DATABASE_URL` if available.

## 📝 Database Schema

The application creates 14 tables automatically:

```
users                  - User accounts (students, teachers, admins)
departments            - Academic departments
courses                - Course offerings
course_enrollments     - Student enrollments in courses
modules                - Course modules/chapters
lessons                - Individual lessons within modules
subjects               - Study subjects
topics                 - Topics within subjects
resources              - Study materials and resources
assignments            - Course assignments
submissions            - Student assignment submissions
quizzes                - Quiz questions and configurations
announcements          - Course announcements
forum_posts            - Discussion forum posts
notifications          - User notifications
```

## 🔧 Troubleshooting

### Connection Error: "could not connect to server"
- **Solution**: Ensure PostgreSQL service is running
  ```powershell
  # Windows - Check if PostgreSQL service is running
  Get-Service | Where-Object {$_.Name -like "*postgres*"}
  
  # Start service if needed
  net start postgresql-x64-15  # Replace with your version
  ```

### "FATAL: Ident authentication failed for user"
- **Solution**: Check `.env` file has correct credentials
- Verify user was created with correct password in Step 2

### "Database does not exist"
- **Solution**: Ensure you created the `study_materials` database
- ```sql
  CREATE DATABASE study_materials;
  ```

### "Password authentication failed"
- **Solution**: Reset PostgreSQL password
  ```bash
  # For Windows PostgreSQL:
  # Use pgAdmin GUI to reset password
  
  # Or use command line:
  psql -U postgres -h localhost
  ALTER USER studyhub WITH PASSWORD 'new_password';
  ```

### Import Error: "psycopg2 module not found"
- **Solution**: Activate virtual environment and reinstall
  ```bash
  # Activate venv
  & "venv\Scripts\Activate.ps1"
  
  # Reinstall requirements
  pip install -r requirements.txt
  ```

## 📊 Useful PostgreSQL Commands

```sql
-- Connect to database
psql -U studyhub -d study_materials -h localhost

-- List all tables
\dt

-- View table structure
\d table_name

-- List databases
\l

-- Delete all data from tables (for testing)
TRUNCATE TABLE users CASCADE;

-- Exit
\q
```

## 🛡️ Security Best Practices

1. **Use strong passwords** for database users
2. **Never commit `.env`** to version control
3. **Use environment variables** for credentials
4. **Restrict database user permissions** to the specific database
5. **Enable SSL connections** for production (cloud providers handle this)
6. **Keep PostgreSQL updated** for security patches

## 📚 Useful Resources

- [PostgreSQL Official Docs](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [PgAdmin Tool](https://www.pgadmin.org/)
- [PostgreSQL Tutorials](https://www.postgresql.org/docs/current/tutorial.html)

## ✅ Verification Checklist

- [ ] PostgreSQL installed and running
- [ ] Database `study_materials` created
- [ ] User `studyhub` created with password
- [ ] `.env` file created with correct credentials
- [ ] Python packages installed (`pip install -r requirements.txt`)
- [ ] App started successfully (`python api/app.py`)
- [ ] Database initialized (check console for "✓ Database initialized successfully")
- [ ] Can access http://localhost:5000
- [ ] Can register a new account
- [ ] Can log in with registered account

---

**Congratulations!** Your StudyHub LMS is now using PostgreSQL! 🎉
