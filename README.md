# Shine Solar Energy - Django Website

## Setup Instructions

1. Create virtual environment:
   python -m venv venv
   venv\Scripts\activate  (Windows)  OR  source venv/bin/activate  (Linux/Mac)

2. Install requirements:
   pip install -r requirements.txt

3. Run migrations:
   python manage.py migrate

4. Create superuser (admin login):
   python manage.py createsuperuser

5. Collect static files:
   python manage.py collectstatic

6. Run the server:
   python manage.py runserver

## Admin Dashboard
- URL: http://localhost:8000/admin-panel/
- Login with the superuser credentials you created

## Features
- Beautiful solar energy website
- Products & Brands management (admin)
- Contact enquiry management
- Solar savings calculator
- Responsive mobile design
- Colors: Navy (#0B2341) + Gold (#F4B400)
