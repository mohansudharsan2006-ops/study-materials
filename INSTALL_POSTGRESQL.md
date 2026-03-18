# PostgreSQL Setup Instructions for StudyHub LMS

## ✅ Step 1: Install PostgreSQL on Windows

### Option A: Using PostgreSQL Official Installer

1. **Download PostgreSQL**
   - Visit: https://www.postgresql.org/download/windows/
   - Download PostgreSQL 14+ (latest stable version)

2. **Run the Installer**
   ```
   postgres-14.10-1-windows-x64.exe  (example filename)
   ```

3. **Installation Settings**
   - Installation Directory: `C:\Program Files\PostgreSQL\14` (default is fine)
   - Password: Set a strong password for the `postgres` superuser
   - Port: Keep default `5432`
   - Locale: Use default
   - Click "Next" through remaining screens
   - Check "Stack Builder" (optional, for pgAdmin)

4. **Verify Installation**
   ```powershell
   psql --version
   # Output: psql (PostgreSQL) 14.10
   ```

### Option B: Using pgAdmin (GUI Recommended for Beginners)

pgAdmin 4 is installed with PostgreSQL and provides a user-friendly interface:
- Start Menu → Search "pgAdmin 4"
- Opens at: http://localhost:5050
- Login with email you provided during installation

---

## 📝 Step 2: Create Database and User

### Using pgAdmin 4 (GUI - Easiest)

1. **Open pgAdmin 4**
   - Start Menu → pgAdmin 4
   - Login with your email

2. **Create Database**
   - Right-click "Databases" → Create → Database
   - Name: `study_materials`
   - Click "Save"

3. **Create User**
   - Right-click "Login/Group Roles" → Create → Login/Group Role
   - Name: `studyhub`
   - Tab "Definition": Password: `your_secure_password`
   - Tab "Privileges": Enable all privileges
   - Click "Save"

4. **Grant Permissions**
   - Right-click `study_materials` → Properties
   - Tab "Security": Grant ALL to `studyhub`

### Using Command Line (SQL Shell)

1. **Open SQL Shell (psql)**
   ```
   Start Menu → Search "SQL Shell (psql)"
   ```

2. **Connect to PostgreSQL**
   ```sql
   -- Press Enter for default values, enter postgres password when asked
   Server [localhost]: 
   Database [postgres]: 
   Port [5432]: 
   Username [postgres]: 
   Password for user postgres: [enter password set during installation]
   ```

3. **Create Database**
   ```sql
   CREATE DATABASE study_materials;
   ```

4. **Create User**
   ```sql
   CREATE USER studyhub WITH PASSWORD 'your_secure_password';
   ```

5. **Grant Privileges**
   ```sql
   ALTER ROLE studyhub SET client_encoding TO 'utf8';
   ALTER ROLE studyhub SET default_transaction_isolation TO 'read committed';
   ALTER ROLE studyhub SET default_transaction_deferrable TO on;
   ALTER ROLE studyhub SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE study_materials TO studyhub;
   
   -- Connect to the database and grant schema privileges
   \c study_materials postgres
   GRANT ALL PRIVILEGES ON SCHEMA public TO studyhub;
   
   -- Exit
   \q
   ```

---

## ⚙️ Step 3: Configure StudyHub LMS

1. **Open `.env` file**
   - Location: `f:\study materials\.env`
   - Edit with Notepad or VS Code

2. **Update Database Credentials**
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=study_materials
   DB_USER=studyhub
   DB_PASSWORD=your_secure_password  # Change this!
   ```

3. **Save the file**

---

## 🚀 Step 4: Start the Application

### Option A: Run from VS Code

1. Open terminal in VS Code
   ```powershell
   & venv\Scripts\Activate.ps1
   python api/app.py
   ```

2. Expected output:
   ```
   ✓ Database initialized successfully
   WARNING: This is a development server...
   Running on http://127.0.0.1:5000
   ```

3. Open browser: http://localhost:5000

### Option B: Run from Command Prompt

```powershell
# Navigate to project
cd f:\study materials

# Activate virtual environment
venv\Scripts\activate

# Run app
python api/app.py
```

---

## 🧪 Step 5: Test the Application

1. **Register a New Account**
   - Go to http://localhost:5000/register
   - Role: Select "student"
   - Click "Register"

2. **Log In**
   - Email: Your registered email
   - Password: Your password
   - Click "Login"

3. **Explore**
   - View Dashboard: /dashboard/student
   - Browse Courses: /courses
   - View Profile: /profile

---

## 🐛 Troubleshooting

### Error: "could not connect to server: No such file or directory"

**Cause**: PostgreSQL service is not running

**Solution**:
```powershell
# Check if PostgreSQL service is running
Get-Service | Where-Object {$_.Name -like "*postgres*"}

# Start PostgreSQL service
net start postgresql-x64-14  # Replace 14 with your version
```

### Error: "FATAL: Ident authentication failed"

**Cause**: Incorrect username or authentication method

**Solution**:
- Verify `.env` has correct `DB_USER` and `DB_PASSWORD`
- Check that user `studyhub` was created correctly
- Try using `psql -U studyhub -h localhost -d study_materials` to test

### Error: "database 'study_materials' does not exist"

**Cause**: Database not created

**Solution**:
```sql
-- In SQL Shell:
CREATE DATABASE study_materials;
```

### Error: "Password authentication failed"

**Cause**: Wrong password in `.env` or password not set correctly

**Solution**:
```powershell
# In pgAdmin 4:
# Right-click 'studyhub' user → Properties → Change password
# OR use SQL:

# In SQL Shell:
\c postgres postgres  -- Connect as postgres superuser
ALTER USER studyhub WITH PASSWORD 'new_password';
```

### Error: "Module psycopg2 not found"

**Cause**: Virtual environment not activated or packages not installed

**Solution**:
```powershell
# Activate venv
& venv\Scripts\Activate.ps1

# Reinstall requirements
pip install -r requirements.txt
```

### Error: "port 5000 is already in use"

**Cause**: Another Flask instance is running

**Solution**:
```powershell
# Kill the process
Get-Process | Where-Object {$_.Name -eq "python"} | Stop-Process -Force

# Or use different port in app.py
# Change: app.run(debug=True, port=5000)
# To    : app.run(debug=True, port=5001)
```

---

## 📊 Useful PostgreSQL Commands

```sql
-- Connect to database
psql -U studyhub -h localhost -d study_materials

-- List databases
\l

-- List tables
\dt

-- View table structure
\d users

-- Show all records in a table
SELECT * FROM users;

-- Count total users
SELECT COUNT(*) FROM users;

-- View specific user
SELECT * FROM users WHERE email = 'your-email@example.com';

-- Backup database
pg_dump -U studyhub study_materials > backup.sql

-- Restore database
psql -U studyhub study_materials < backup.sql

-- Delete all data from tables (for testing)
TRUNCATE TABLE users CASCADE;

-- Exit psql
\q
```

---

## 📋 Verification Checklist

Before deploying, verify:

- [ ] PostgreSQL installed and running (`Get-Service | Where-Object {$_.Name -like "*postgres*"}`)
- [ ] Database `study_materials` created (`psql -U postgres -l | grep study_materials`)
- [ ] User `studyhub` created with password
- [ ] `.env` file has correct credentials
- [ ] Python packages installed (`pip list | grep psycopg2`)
- [ ] App starts without errors (`python api/app.py`)
- [ ] Can access http://localhost:5000
- [ ] Can register a new account
- [ ] Can log in with credentials
- [ ] Dashboard loads correctly
- [ ] Can view courses and assignments

---

## 🌐 Cloud Deployment

For deploying to cloud services (Heroku, Railway, Render), use `DATABASE_URL`:

### Example DATABASE_URL Format:
```
postgresql://studyhub:password@localhost:5432/study_materials
```

### Set in Cloud Provider:
```
DATABASE_URL=postgresql://username:password@host:5432/dbname
```

The app will automatically detect and use the `DATABASE_URL` environment variable.

---

## 🔒 Security Best Practices

1. **Never commit `.env`** to version control
   - Add `.env` to `.gitignore`
   - Use `git rm --cached .env`

2. **Use strong passwords** for database users
   - At least 12 characters
   - Mix uppercase, lowercase, numbers, special chars

3. **Restrict database user permissions**
   - Create separate users for different applications
   - Limit permissions to necessary tables only

4. **Enable SSL** for production (cloud providers handle this)
   - Heroku, Railway, Render all use SSL by default

5. **Regular backups**
   ```powershell
   pg_dump -U studyhub study_materials > backup_$(Get-Date -Format "yyyy-MM-dd").sql
   ```

---

## 📚 Additional Resources

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/)
- [pgAdmin4 GUI Tool](https://www.pgadmin.org/)
- [Flask + SQLAlchemy (ORM Alternative)](https://flask-sqlalchemy.palletsprojects.com/)

---

**Congratulations!** Your StudyHub LMS is now running on PostgreSQL! 🎉

For questions or issues, refer to the troubleshooting section or check the console output for detailed error messages.
