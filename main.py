from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLAlchemy To-Do Model
class ToDoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# Pydantic To-Do Model for API
class ToDoSchema(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class ToDoResponse(ToDoSchema):
    id: int

    class Config:
        orm_mode = True

# CRUD Operations

# Create a To-Do
@app.post("/todos/", response_model=ToDoResponse)
def create_todo(todo: ToDoSchema, db: Session = Depends(get_db)):
    db_todo = ToDoDB(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Get all To-Dos
@app.get("/todos/", response_model=List[ToDoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(ToDoDB).all()

# Get a single To-Do by ID
@app.get("/todos/{todo_id}", response_model=ToDoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    return todo

# Update a To-Do
@app.put("/todos/{todo_id}", response_model=ToDoResponse)
def update_todo(todo_id: int, updated_todo: ToDoSchema, db: Session = Depends(get_db)):
    todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    for key, value in updated_todo.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

# Delete a To-Do
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    db.delete(todo)
    db.commit()
    return {"message": "To-Do deleted successfully"}
