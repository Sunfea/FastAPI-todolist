from models import TodoDB, SessionLocal

# Test database connection and basic operations
def test_db():
    db = SessionLocal()
    
    # Create a test todo
    todo = TodoDB(title="Test Todo", description="This is a test todo item")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    print(f"Created todo: {todo.title}")
    
    # Retrieve all todos
    todos = db.query(TodoDB).all()
    print(f"Total todos: {len(todos)}")
    
    for t in todos:
        print(f"- {t.title}: {t.description} (Completed: {t.completed})")
    
    # Clean up
    db.delete(todo)
    db.commit()
    db.close()
    print("Test completed successfully!")

if __name__ == "__main__":
    test_db()