# 🍬 Sweet Shop Management System

A full-stack Sweet Shop Management System built using Django REST Framework, PostgreSQL, and a modern React frontend.
The system supports user authentication, role-based access (Admin/User), inventory management, and follows Test-Driven Development (TDD) principles.

## ✨ Features
🔐 Authentication

User Registration

User Login

JWT-based authentication

Role-based access (Admin / User)

🍭 Sweet Management

View all available sweets (authenticated users)

Search & filter sweets

Purchase sweets (quantity auto-decreases)

Disable purchase if out of stock

## 🛠 Admin Panel Features

Add new sweets

Update sweet details

Delete sweets

Restock sweets

🧪 Testing

Backend fully developed using TDD

High coverage using pytest & pytest-django

Authentication, authorization, inventory, and edge cases covered

## 🏗 Tech Stack
Backend

Django

Django REST Framework

PostgreSQL

JWT Authentication

pytest (TDD)

Frontend

React

React Router

Axios

CSS / Tailwind (UI)

Responsive Design (Mobile, Tablet, Desktop)

## 📂 Project Structure
Sweet_Shop_Management/
│
├── backend/
│   ├── apps/
│   │   ├── accounts/        # Auth, JWT, permissions
│   │   └── sweets/          # Sweets & inventory
│   ├── tests/               # pytest test cases
│   ├── sweetshop/           # Project config
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md

🧪 Test-Driven Development (TDD)

This project strictly follows Red → Green → Refactor:

Write failing test

Implement minimal logic

Refactor safely

Commit each step

Run backend tests:

cd backend
pytest

## 🔑 Admin System (IMPORTANT)
Where are users stored?

Users are stored in PostgreSQL

Django default auth_user table

How admin works

Admin = is_staff = True

Checked via custom permission IsAdminUser

Create Admin User (Recommended)
cd backend
python manage.py createsuperuser

## Django Admin Panel URL
http://localhost:8000/admin/


You can:

View users

Promote users to admin

Inspect database records

▶️ Running the Project Locally
Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt


Configure PostgreSQL in settings.py:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sweetshop_db",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


Run migrations & server:

python manage.py migrate
python manage.py runserver


## Backend runs at:

http://localhost:8000

## Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs at:

http://localhost:5173


⚠️ Always use trailing slashes in API calls:

/api/auth/login/
/api/auth/register/

🚀 API Overview
Auth
POST /api/auth/register/
POST /api/auth/login/

Sweets
GET    /api/sweets/
POST   /api/sweets/            (Admin)
POST   /api/sweets/{id}/purchase/
POST   /api/sweets/{id}/restock/ (Admin)

🤖 My AI Usage
Tools Used

ChatGPT,Gemini 

How AI Was Used

Structuring frontend UI flow

Improving documentation clarity

Reflection

AI significantly improved productivity by:

Helping reason about edge cases

Maintaining clean and consistent structure

All code was reviewed, modified, and validated manually.
AI was used as an assistant, not a replacement for understanding.




Add Environment Variables:


🚀 Frontend Deployment (Vercel / Netlify)
Vercel (Recommended)
cd frontend
npm run build


✅ Final Notes

Backend is interview-ready

TDD is clearly demonstrated

Admin system is secure & role-based

Frontend is responsive & user-friendly

Documentation is complete
