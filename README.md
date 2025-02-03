# FastAPI To-Do Application

This project is a simple **To-Do Application** built using **FastAPI** and **SQLAlchemy**. It provides CRUD (Create, Read, Update, Delete) operations for managing To-Do items.

## Features 🚀
- Create a To-Do item ✅
- Get all To-Do items 📜
- Retrieve a single To-Do by ID 🔍
- Update a To-Do item ✏️
- Delete a To-Do item 🗑️
- Uses **FastAPI**, **SQLAlchemy**, and **Pydantic** for data validation
- Database session management using **Dependency Injection**

---

## Setup and Installation ⚙️
### 1. Install Dependencies
```sh
pip install fastapi uvicorn sqlalchemy sqlite3 pydantic
```

### 2. Run the FastAPI Server
```sh
uvicorn main:app --reload
```

---

## Code Implementation 💻

### **1. Import Required Libraries**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from typing import List
```

### **2. Initialize FastAPI and Database**
```python
app = FastAPI()
Base.metadata.create_all(bind=engine)
```

### **3. Database Session Dependency**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### **4. SQLAlchemy To-Do Model**
```python
class ToDoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
```

### **5. Pydantic Models**
```python
class ToDoSchema(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class ToDoResponse(ToDoSchema):
    id: int
    class Config:
        orm_mode = True
```

### **6. CRUD Operations**
#### **Create a To-Do**
```python
@app.post("/todos/", response_model=ToDoResponse)
def create_todo(todo: ToDoSchema, db: Session = Depends(get_db)):
    db_todo = ToDoDB(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
```

#### **Get All To-Dos**
```python
@app.get("/todos/", response_model=List[ToDoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(ToDoDB).all()
```

#### **Get a Single To-Do by ID**
```python
@app.get("/todos/{todo_id}", response_model=ToDoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    return todo
```

#### **Update a To-Do**
```python
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
```

#### **Delete a To-Do**
```python
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDoDB).filter(ToDoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    db.delete(todo)
    db.commit()
    return {"message": "To-Do deleted successfully"}
```

---

## **Testing the API 🔍**
Once the server is running, visit the **interactive API docs**:
- Open **http://127.0.0.1:8000/docs** 📜
- You can test all the API endpoints from the Swagger UI

---

## **Next Steps**
This was our **first project** to understand the basics of FastAPI. We will now move on to **four more projects**, gradually increasing complexity. Stay tuned! 🚀🔥

