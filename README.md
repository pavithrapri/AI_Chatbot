# AI_Chatbot

# COMPLETE DJANGO CHATBOT SETUP GUIDE

* 1. CREATE PROJECT STRUCTURE
```bash
mkdir django_chatbot
cd django_chatbot
```

# 2. CREATE VIRTUAL ENVIRONMENT
```bash
python -m venv chatbot_env
```

# Activate virtual environment
- On Windows:
```bash
chatbot_env\Scripts\activate
```
- On Mac/Linux:
```bash
source chatbot_env/bin/activate
```

# 3. INSTALL REQUIRED PACKAGES
```bash
pip install Django==4.2.7
pip install mysqlclient==2.2.0
pip install groq==0.4.1
pip install python-dotenv==1.0.0
```

# 4. CREATE DJANGO PROJECT
```bash
django-admin startproject chatbot_project
cd chatbot_project
```

# 5. CREATE DJANGO APP
```bash
python manage.py startapp chat
```

# =====================================
# FILE STRUCTURE SHOULD LOOK LIKE:
# =====================================

```
chatbot_project/
├── chatbot_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── chat/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   └── templates/
│       └── chat/
│           └── index.html
|
├── .env
├── requirements.txt
└── manage.py
```

# =====================================
# ADDITIONAL CONFIGURATION FILES
# =====================================

## requirements.txt
```bash
echo "Django==4.2.7
mysqlclient==2.2.0
groq==0.4.1
python-dotenv==1.0.0" > requirements.txt
```

## .env file (IMPORTANT: Replace with your actual values)
```bash
echo "GROQ_API_KEY=your_groq_api_key_here
DB_NAME=chatbot_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=django-insecure-your-secret-key-here-replace-this
DEBUG=True" > .env
```

# =====================================
# MYSQL DATABASE SETUP
# =====================================

## 1. Install MySQL (if not already installed)
- For Ubuntu/Debian:
```bash
sudo apt update && sudo apt install mysql-server mysql-client
```

- For macOS with Homebrew:
```bash
brew install mysql
```

- For Windows: Download MySQL installer from mysql.com

## 2. Start MySQL service
```bash
# Linux
sudo systemctl start mysql

# macOS
brew services start mysql
```

## 3. Secure MySQL installation
```bash
sudo mysql_secure_installation
```

## 4. Create database and user
```sql
mysql -u root -p << EOF
CREATE DATABASE chatbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'chatbot_user'@'localhost' IDENTIFIED BY 'secure_password_123';
GRANT ALL PRIVILEGES ON chatbot_db.* TO 'chatbot_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF
```

# =====================================
# GROQ API KEY SETUP
# =====================================

1. Go to https://console.groq.com/  
2. Sign up/Login  
3. Navigate to API Keys section  
4. Create a new API key  
5. Copy the API key and paste it in your `.env` file  

# =====================================
# DJANGO SETUP COMMANDS
# =====================================

1. Create migrations  
```bash
python manage.py makemigrations chat
```

2. Apply migrations  
```bash
python manage.py migrate
```

3. Create superuser (optional)  
```bash
python manage.py createsuperuser
```

4. Run development server  
```bash
python manage.py runserver
```

# =====================================
# TESTING THE APPLICATION
# =====================================

1. Start the server  
```bash
python manage.py runserver
```

2. Open browser and go to:  
http://127.0.0.1:8000/

3. Test the chat functionality:
- Type a message and send  
- Verify AI response appears  
- Check database for stored messages  
- Test clear chat functionality

4. Access admin panel:  
http://127.0.0.1:8000/admin/  
- Login with superuser credentials  
- View chat messages in the admin  

# =====================================
# TROUBLESHOOTING COMMON ISSUES
# =====================================

## Issue 1: MySQL connection error  
**Solution:**  
- Check MySQL service is running  
- Verify database credentials in .env  
- Ensure database exists  

## Issue 2: Groq API error  
**Solution:**  
- Verify API key is correct  
- Check internet connection  
- Ensure API quota is not exceeded  

## Issue 3: CSRF token error  
**Solution:**  
- Ensure `{% csrf_token %}` is in template  
- Check CSRF middleware is enabled  

## Issue 4: Static files not loading  
**Solution:**  
- Run: `python manage.py collectstatic`  
- Check `STATIC_URL` and `STATICFILES_DIRS` in settings  

## Issue 5: Migration errors  
**Solution:**  
- Delete migration files (keep `__init__.py`)  
- Run: `python manage.py makemigrations`  
- Run: `python manage.py migrate`

---

Your chatbot application is now ready to use!

```bash
echo "Setup completed successfully! "
echo "Run 'python manage.py runserver' and visit http://127.0.0.1:8000/"
```
