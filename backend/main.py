from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from sqlalchemy.orm import Session
from datetime import timedelta

from .models import TodoDB, SessionLocal
from .auth import (
    authenticate_user, create_access_token, get_current_active_user, 
    User, UserCreate, UserOut, create_user, Token, get_db,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from .frontend import frontend_router

app = FastAPI(title="Todo API", description="A simple todo list API with SQLite database", version="1.0.0")

# Include the frontend router
app.include_router(frontend_router)

# Dependency
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API with SQLite database and authentication"}

# Authentication endpoints
@app.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db_session)):
    # Check if user already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = create_user(db, user)
    return new_user

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer"
    )

@app.get("/users/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Protected todo endpoints
@app.get("/todos", response_model=List[Todo])
def get_todos(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    todos = db.query(TodoDB).filter(TodoDB.user_id == current_user.id).all()
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id, TodoDB.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    # Create a dictionary with the todo data
    todo_data = {
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "user_id": current_user.id
    }
    
    # Create the TodoDB instance using the dictionary
    db_todo = TodoDB(**todo_data)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id, TodoDB.user_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update fields only if provided
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
        
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_active_user)):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id, TodoDB.user_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)