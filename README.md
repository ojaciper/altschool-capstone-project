# Course Enrollment Platform

A modern FastAPI-based course enrollment management system that allows students to register for courses and administrators to manage the platform. Built with PostgreSQL for data persistence and Alembic for database migrations.

## Features

- **User Management**: Create and manage student and admin accounts with role-based access control
- **Course Management**: Create, update, and manage courses with capacity limits
- **Enrollment System**: Students can enroll in available courses
- **Authentication**: JWT-based authentication with secure password hashing
- **Database Migrations**: Automated schema management with Alembic
- **Testing**: Comprehensive test suite with pytest

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- **Database**: PostgreSQL - Robust relational database
- **ORM**: SQLAlchemy - Python SQL toolkit and Object-Relational Mapping
- **Migrations**: Alembic - Database versioning tool
- **Authentication**: JWT (PyJWT) with Argon2 password hashing
- **Testing**: pytest with coverage reporting
- **API Documentation**: Auto-generated with OpenAPI/Swagger

## Project Structure

```
course_enrollment_platform/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   └── v1/
│   │       └── routes/         # API route handlers
│   │           ├── auth.py     # Authentication endpoints
│   │           ├── user.py     # User management endpoints
│   │           ├── course.py   # Course management endpoints
│   │           └── enrollment.py # Enrollment endpoints
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── security.py        # Security and JWT utilities
│   ├── db/
│   │   ├── base.py            # SQLAlchemy base configuration
│   │   ├── session.py         # Database session management
│   │   └── models/            # Database models
│   │       ├── user.py        # User model with Role enum
│   │       ├── course.py      # Course model
│   │       └── enrollment.py  # Enrollment model
│   ├── schemas/               # Pydantic models for validation
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── course.py
│   │   └── enrollment.py
│   ├── services/              # Business logic layer
│   │   ├── user.py
│   │   ├── course.py
│   │   └── enrollment.py
│   ├── dependency/
│   │   └── deps.py            # Dependency injection
│   └── test/                  # Test suite
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_user.py
│       ├── test_course.py
│       ├── test_enrollment.py
│       └── helpers.py
├── alembic/                    # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/               # Migration scripts
├── alembic.ini                # Alembic configuration
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables (not in repo)
```

## Installation

### Prerequisites
- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip or poetry

### Setup Steps

1. **Clone or navigate to the project directory**:
   ```bash
   cd course_enrollment_platform
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root with the following variables:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/course_enrollment
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   ```

5. **Apply database migrations**:
   ```bash
   alembic upgrade head
   ```

## Running the Application

### Development Server

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /login` - User login and JWT token generation
- `POST /logout` - User logout

### Users (`/api/v1/user`)
- `POST /` - Create a new user (student or admin)
- `GET /` - List all users (admin only)
- `GET /{user_id}` - Get user details
- `PUT /{user_id}` - Update user information
- `DELETE /{user_id}` - Delete a user

### Courses (`/api/v1/course`)
- `POST /` - Create a new course (admin only)
- `GET /` - List all courses
- `GET /{course_id}` - Get course details
- `PUT /{course_id}` - Update course information
- `DELETE /{course_id}` - Delete a course

### Enrollments (`/api/v1/enrollment`)
- `POST /` - Enroll a student in a course
- `GET /` - List all enrollments
- `GET /{enrollment_id}` - Get enrollment details
- `DELETE /{enrollment_id}` - Cancel an enrollment

## Database Models

### User
- **id**: UUID (primary key)
- **full_name**: String (max 50 characters)
- **email**: String (unique)
- **hashed_password**: String
- **role**: String (student/admin)
- **is_active**: Boolean

### Course
- **id**: UUID (primary key)
- **title**: Text
- **course_code**: String (indexed, unique)
- **capacity**: Integer
- **is_active**: Boolean

### Enrollment
- **id**: UUID (primary key)
- **user_id**: UUID (foreign key to users)
- **course_id**: UUID (foreign key to courses)
- **created_at**: DateTime with timezone

## Testing

Run the test suite with pytest:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html
pytest --cov=.

# Run specific test file
pytest app/test/test_auth.py -v
```

Test files are located in `app/test/` directory and include:
- `test_auth.py` - Authentication tests
- `test_user.py` - User management tests
- `test_course.py` - Course management tests
- `test_enrollment.py` - Enrollment system tests

## Database Migrations

### Create a new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migrations

```bash
alembic downgrade -1
```

### View migration history

```bash
alembic history
```

## Environment Variables

The application requires the following environment variables in a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | Secret key for JWT signing | Required |
| `ALGORITHM` | JWT algorithm (HS256, HS512, etc.) | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time | 15 |

## Security Features

- **Password Hashing**: Argon2 for secure password storage
- **JWT Authentication**: Token-based authentication for API requests
- **Role-Based Access Control**: Separate permissions for students and admins
- **Email Validation**: Pydantic email validation for user creation
- **Database Connection**: Secure PostgreSQL connection with connection pooling

## Development Guidelines

### Code Organization
- Business logic resides in `services/` layer
- Database interactions through SQLAlchemy models
- Request/response validation using Pydantic schemas
- Route handlers delegate to service layer

### Adding New Features
1. Define Pydantic schema in `schemas/`
2. Create database model in `db/models/`
3. Implement business logic in `services/`
4. Create API routes in `api/v1/routes/`
5. Add tests in `test/`
6. Create migration if schema changed

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify `DATABASE_URL` is correct
- Check database credentials

### Migration Errors
- Run `alembic current` to check current state
- Review migration files in `alembic/versions/`
- Use `alembic downgrade -1` to rollback if needed

### Authentication Issues
- Verify `SECRET_KEY` and `ALGORITHM` are set correctly
- Check JWT token expiration time
- Ensure password hashing is working

## Future Enhancements

- Email notifications for enrollment
- Course prerequisites and dependencies
- Grade tracking system
- Student progress dashboard
- Course scheduling and calendar
- Payment integration for paid courses

## License

This project is provided as-is for educational purposes.

## Contact & Support

For issues or questions about the Course Enrollment Platform, please create an issue in the project repository.
