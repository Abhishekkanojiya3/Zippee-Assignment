📝 Task Manager API

A RESTful API for task management built with Django and Django REST Framework, featuring JWT authentication, role-based access, and task filtering.

🚀 Features

🔐 JWT Authentication (register, login, logout, password change)

👥 Role-based access (Admin & User)

✅ CRUD operations for tasks

🔍 Filter, search, and sort tasks

📊 Task stats (completed, pending, overdue)

🧩 Swagger & ReDoc API documentation

⚙️ Setup
1. Clone & Setup
git clone <repo-url>
cd taskmanager
python -m venv venv
venv\Scripts\activate  # (Windows)
pip install -r requirements.txt

2. Configure Environment

Create a .env file:

SECRET_KEY=your-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=db.sqlite3

3. Run Migrations & Server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


Access:

API Docs → http://127.0.0.1:8000/api/docs/

Admin → http://127.0.0.1:8000/admin/

🔑 Main Endpoints
Action	Method	Endpoint
Register	POST	/auth/register/
Login	POST	/auth/login/
Logout	POST	/auth/logout/
List Tasks	GET	/tasks/
Create Task	POST	/tasks/
Task Details	GET	/tasks/{id}/
Update/Delete Task	PUT/PATCH/DELETE	/tasks/{id}/
Task Stats	GET	/tasks/stats/

All secured routes require:

Authorization: Bearer <access_token>

🗂️ Project Structure
taskmanager/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
├── apps/
│   ├── authentication/
│   └── tasks/
└── requirements.txt

🧰 Tech Stack

Django 4.2+

Django REST Framework

SimpleJWT

Django Filter

drf-yasg (Swagger)

Python Decouple
