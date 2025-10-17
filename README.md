📝 Task Manager API
A robust RESTful API for task management with user authentication, built with Django and Django REST Framework. Features JWT authentication, role-based access control, advanced filtering, and comprehensive API documentation.
Image

🌟 Features
🔐 Authentication & Authorization

JWT-based authentication with access and refresh tokens
User registration and login
Password change functionality
Role-based access control (Admin & Regular User)
Token blacklisting for secure logout

📋 Task Management

Complete CRUD operations for tasks
Task priority levels (LOW, MEDIUM, HIGH)
Due date tracking with overdue detection
Mark tasks as complete/incomplete
Task statistics and analytics

🔍 Advanced Features

Search tasks by title and description
Filter by completion status, priority, and dates
Sort tasks by multiple fields
User-specific task isolation
Admin can view all users' tasks

🚀 Quick Start
Prerequisites

Python 3.8 or higher
pip (Python package manager)
Virtual environment (recommended)

Installation

Clone the repository

bash   git clone <your-repository-url>
   cd task_manager_project

Create and activate virtual environment

bash   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate

Install dependencies

bash   pip install -r requirements.txt

Environment setup
Create a .env file in the project root:

env   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_NAME=db.sqlite3

Run migrations

bash   python manage.py makemigrations
   python manage.py migrate

Create superuser (for admin access)

bash   python manage.py createsuperuser
Enter email, username, and password when prompted.

Start the development server

bash   python manage.py runserver

Access the application

API Documentation: http://127.0.0.1:8000/api/docs/
Admin Panel: http://127.0.0.1:8000/admin/
API Root: http://127.0.0.1:8000/api/

🧪 Testing the API
Using Swagger UI (Recommended)

Open http://127.0.0.1:8000/api/docs/
Click on POST /api/auth/register/ to create an account
Click the "Authorize" button (🔒) at the top
Enter: Bearer YOUR_ACCESS_TOKEN
Try out all endpoints interactively!
