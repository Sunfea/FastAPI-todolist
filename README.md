# Modern Todo API with FastAPI and SQLite

A modern RESTful API for managing todo items built with FastAPI and SQLite database with full authentication system.

## Features

- User registration and login
- JWT token-based authentication (30-minute expiration)
- Create, read, update, and delete todo items
- Mark todos as completed
- View all todos or individual todos
- Persistent storage with SQLite database
- Responsive web interface
- Interactive API documentation

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python main.py
   ```

   Or using the startup scripts:
   - On Windows: `start.bat`
   - On Linux/Mac: `start.sh`

   Or using uvicorn directly:
   ```
   uvicorn main:app --reload
   ```

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /token` - Login and get access token
- `GET /users/me` - Get current user info

### Todos (Protected - Requires Authentication)
- `GET /` - Welcome message
- `GET /todos` - Get all todos
- `GET /todos/{id}` - Get a specific todo
- `POST /todos` - Create a new todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo

## Usage

After starting the server:

1. Access the API at `http://localhost:8000`
2. Visit the interactive API documentation at `http://localhost:8000/docs`
3. Open `http://localhost:8000/login.html` or `http://localhost:8000/register.html` in your browser to create an account or login
4. After logging in, you'll be redirected to `http://localhost:8000/client.html` to use the responsive web interface

## Database

The application uses SQLite for persistent storage. A `todos.db` file will be automatically created in the project directory when you run the application for the first time.

## Project Structure

- `main.py` - Main FastAPI application
- `backend/` - Backend components
  - `models.py` - Database models and setup
  - `auth.py` - Authentication logic and utilities
  - `frontend.py` - Frontend route handling
- `frontend/` - Frontend components
  - `login.html` - User login page
  - `register.html` - User registration page
  - `client.html` - Responsive web interface for todo management
- `requirements.txt` - Project dependencies
- `Dockerfile` - Docker configuration
- `start.sh` - Linux/Mac startup script
- `start.bat` - Windows startup script
- `todos.db` - SQLite database file (created automatically)

## Dependencies

- FastAPI - Web framework
- Uvicorn - ASGI server
- SQLAlchemy - Database ORM
- Pydantic - Data validation
- Passlib - Password hashing
- bcrypt - Password hashing algorithm
- python-jose - JWT token handling
- python-multipart - Form data parsing

## Deployment

### Docker Deployment

Build and run the Docker container:
```
docker build -t todo-api .
docker run -p 8000:8000 todo-api
```

The application will be available at `http://localhost:8000`

### Traditional Deployment

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. Access the application at `http://localhost:8000`