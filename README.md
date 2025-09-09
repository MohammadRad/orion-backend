# Orion Backend

This repository contains a simple yet professional‑quality web backend built with
**FastAPI** and **SQLAlchemy**.  It provides user authentication using JSON Web
Tokens (JWT), project and task management endpoints, and uses a relational
database for persistence.  The design follows common best practices such as
password hashing, separate data models and schemas, and dependency‑injected
database sessions.  It is intended to serve as a portfolio piece and starting
point for more complex applications.

## Features

- **User registration and login** with hashed passwords and JWT‑based access
  tokens.  The access token must be supplied in the `Authorization` header
  (`Bearer <token>`) for authenticated routes.
- **CRUD for projects and tasks**.  Each project is owned by a user and can
  contain multiple tasks.  Projects and tasks can be created and listed; the
  code structure makes it easy to extend these endpoints with update and
  delete operations.
- **SQLite database** via SQLAlchemy ORM.  The database is automatically
  created on first run (`orion.db` in the project root).  To switch to
  PostgreSQL or another database, update the connection string in
  `app/database.py`.
- **Modular structure** with clearly separated modules for models, schemas,
  authentication utilities and the main application.  This encourages
  maintainability and extensibility.

## Running the service

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Start the application using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The API will be available at <http://localhost:8000>.  Interactive
documentation is served at `/docs`.

## Endpoints

### Authentication

- `POST /auth/register` – Create a new user.  Request body: `{ "email": "...", "password": "..." }`.
- `POST /auth/login` – Log in and receive a JWT.  Request body: `{ "email": "...", "password": "..." }`.  Response: `{ "access_token": "...", "token_type": "bearer" }`.

### Projects

- `POST /projects` – Create a project.  Requires authentication.  Request body:
  `{ "name": "Project name", "description": "Optional description" }`.
- `GET /projects` – List all projects owned by the authenticated user.

### Tasks

- `POST /tasks/{project_id}` – Create a task under the specified project.
  Request body: `{ "title": "Task title", "status": "todo" }`.
- `GET /tasks/{project_id}` – List all tasks belonging to the specified
  project.

## License

This project is provided under the MIT License.  See the `LICENSE` file for
details.
