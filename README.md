# Task Management API

A production-ready Task Management REST API built with FastAPI, SQLAlchemy 2.0, PostgreSQL, Alembic, Pydantic v2, JWT authentication, and pytest.

## Features
- User registration and login with JWT authentication
- CRUD operations for tasks
- Task fields: title, description, status, priority, due date
- Pagination, filtering, and search for task listing
- User-based data isolation
- Health check endpoint
- Environment-based configuration
- Global exception handling and logging

## Project Structure
- app/api: API routes and endpoints
- app/core: configuration, security, logging, exceptions
- app/database: SQLAlchemy engine/session and base model
- app/models: ORM models
- app/schemas: request and response schemas
- app/services: business logic
- app/repositories: data access layer
- tests: pytest-based tests

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Copy .env.example to .env and adjust values.
4. Create the PostgreSQL database.
5. Run Alembic migrations:
   `alembic upgrade head`
6. Start the app:
   `uvicorn app.main:app --reload`

## Environment Variables
- DATABASE_URL
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- ENVIRONMENT
- LOG_LEVEL

## API Endpoints
### Authentication
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me

### Tasks
- POST /api/v1/tasks
- GET /api/v1/tasks
- GET /api/v1/tasks/{task_id}
- PUT /api/v1/tasks/{task_id}
- DELETE /api/v1/tasks/{task_id}

### Health
- GET /health

## Sample Requests
### Register
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret123"}'
```

### Create Task
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Write docs","description":"Document the API","status":"pending","priority":"high"}'
```

## Sample Responses
### Register/Login Response
```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

### Task Response
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Write docs",
  "description": "Document the API",
  "status": "pending",
  "priority": "high",
  "due_date": null,
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2026-08-01T00:00:00",
  "updated_at": "2026-08-01T00:00:00"
}
```

## Testing
Run tests with:
```bash
pytest -q
```
