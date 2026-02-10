<!-- @format -->

# Crowdfunding Platform - Django Application

A comprehensive, production-ready crowdfunding platform built with Django 5.2, featuring advanced project management, user authentication, donations, ratings, and community engagement.

## Features

**User Management:**
- User registration with email verification
- Social login (Google, Facebook OAuth)
- Profile management with picture upload
- Password reset functionality
- Account deletion with confirmation

**Project Management:**
- Create, edit, and delete projects
- Upload multiple project images
- Project categorization and tagging
- Project search and filtering
- Detailed project timeline

**Community Features:**
- Donate to projects with progress tracking
- Rate projects (1-5 stars)
- Leave comments and replies
- Project reporting system
- Follow projects

**Additional Features:**
- Responsive mobile-friendly design
- Advanced filtering and search
- Email notifications
- Admin dashboard
- Sample data seeding command

## Technology Stack

- **Backend**: Django 5.2 with PostgreSQL/SQLite
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Django allauth with OAuth 2.0
- **Image Processing**: Pillow
- **Server**: Gunicorn + WhiteNoise
- **Deployment**: Render.com
- **Admin**: Django admin interface

## Quick Start

### Local Development

1. **Clone and Setup**:
   ```bash
   git clone <repo-url>
   cd Crowd-FundingProject
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Database Setup**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py seed_data  # Optional: load sample data
   ```

4. **Run Server**:
   ```bash
   python manage.py runserver
   # Visit http://localhost:8000
   ```

### Deployment to Render

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions.

Quick checklist:
- [ ] Generate secure SECRET_KEY
- [ ] Set up PostgreSQL database
- [ ] Configure OAuth credentials
- [ ] Set environment variables in Render
- [ ] Deploy and create superuser

## Project Structure

```
├── crowdfunding/          # Main settings & config
│   ├── settings.py       # Django settings (uses .env)
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI entry point
├── projects/              # Projects app
│   ├── models.py         # Project, Donation, Rating models
│   ├── views.py          # Project views
│   ├── forms.py          # Project forms
│   └── management/
│       └── seed_data.py  # Sample data generator
├── users/                 # Authentication app
│   ├── models.py         # CustomUser, Profile models
│   ├── views.py          # Auth views
│   └── forms.py          # User forms
├── static/                # CSS, JS, images
├── media/                 # User uploads
├── templates/             # HTML templates
├── .env                   # Environment variables
├── .env.example           # Environment template
├── requirements.txt       # Python dependencies
├── Procfile               # Render deployment
├── DEPLOYMENT.md          # Deployment guide
└── README.md              # This file
```

## Environment Variables

All settings use environment variables for security. Create `.env` file:

```bash
# Django
DEBUG=True
SECRET_KEY=your-secure-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL in production)
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# OAuth
GOOGLE_CLIENT_ID=your-google-id
GOOGLE_CLIENT_SECRET=your-google-secret
FACEBOOK_CLIENT_ID=your-facebook-id
FACEBOOK_CLIENT_SECRET=your-facebook-secret

# Security (production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

See `.env.example` for all available variables.
- Comment and reply system
- Show related projects 
- Top contributors, featured projects, latest 5 added and top rated projects at home page
- Static Testimonials

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Git

## Setup Guide

1. Clone the repository:

```powershell
git clone https://github.com/AymanCE-SE/Django-CrowdFunding
cd Crowd-FundingProject
```

2. Create and activate virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

3. Install requirements:

```powershell
pip install -r requirements.txt
```

4. Configure PostgreSQL:

```sql
CREATE DATABASE crowdfunding_db;
CREATE USER crowdfunding WITH PASSWORD '123456';
ALTER USER crowdfunding CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE crowdfunding_db TO crowdfunding;
```

5. Update database settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crowdfunding_db',
        'USER': 'crowdfunding',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

6. Create fresh migrations:

```powershell
# Remove existing migrations (if any)
Remove-Item ".\projects\migrations\*.py"
Remove-Item ".\users\migrations\*.py"

# Create __init__.py files
New-Item -Path ".\projects\migrations\__init__.py" -ItemType File -Force
New-Item -Path ".\users\migrations\__init__.py" -ItemType File -Force

# Create migrations
python manage.py makemigrations users
python manage.py makemigrations projects
```

7. Apply migrations in order:

```powershell
python manage.py migrate auth
python manage.py migrate contenttypes
python manage.py migrate admin
python manage.py migrate sessions
python manage.py migrate users
python manage.py migrate projects
```

8. Create initial data:

```powershell
python manage.py ensure_default_categories
```

9. Create superuser:

```powershell
python manage.py createsuperuser
```

10. Run development server:

```powershell
python manage.py runserver
```

## Project Structure

```
Crowd-FundingProject/
├── crowdfunding/        # Project settings
├── projects/           # Projects app
├── users/             # Users app
├── static/            # Static files
├── media/            # User uploaded files
├── requirements.txt   # Project dependencies
└── manage.py         # Django management script
```

## Environment Variables

Create `.env` file in project root:

```plaintext
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=crowdfunding_db
DB_USER=crowdfunding
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
```

## Access Points

- Admin Interface: http://localhost:8000/admin/
- User Registration: http://localhost:8000/accounts/register/
- Project List: http://localhost:8000/projects/

## Troubleshooting

### Database Issues

If you encounter database errors:

```powershell
psql -U postgres -c "DROP DATABASE crowdfunding_db;"
psql -U postgres -c "CREATE DATABASE crowdfunding_db;"
```

Then repeat steps 6-8.

### Migration Issues

If migrations fail:

```powershell
python manage.py migrate projects zero --fake
python manage.py migrate projects --fake-initial
```

### Static Files

If static files aren't loading:

```powershell
python manage.py collectstatic
```

## Note

- Replace `123456` with a secure password
- Keep your `.env` file secure and never commit it
- Make sure PostgreSQL service is running before setup

## Database Reset Instructions

1. Drop and recreate database:

```powershell
psql -U postgres -c "DROP DATABASE IF EXISTS crowdfunding_db;"
psql -U postgres -c "CREATE DATABASE crowdfunding_db;"
```

2. Remove migrations:

```powershell
Remove-Item ".\projects\migrations\*.py"
Remove-Item ".\users\migrations\*.py"
New-Item -Path ".\projects\migrations\__init__.py" -ItemType File -Force
New-Item -Path ".\users\migrations\__init__.py" -ItemType File -Force
```

3. Create fresh migrations:

```powershell
python manage.py makemigrations users
python manage.py makemigrations projects
```

4. Apply migrations:

```powershell
python manage.py migrate auth
python manage.py migrate contenttypes
python manage.py migrate admin
python manage.py migrate sessions
python manage.py migrate users
python manage.py migrate projects
```

5. Create superuser:

```powershell
python manage.py createsuperuser
```

6. Create default categories:

```powershell
python manage.py ensure_default_categories
```

## Environment Setup

Create `.env` file:

```plaintext
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=crowdfunding_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Development Setup

1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Setup database
5. Run migrations
6. Create superuser
7. Run development server

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request
