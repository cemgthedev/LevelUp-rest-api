from fastapi import FastAPI, Depends
from sqlmodel import Session
from database import get_db
from models import *
from services.users import router as users_router
from services.courses import router as courses_router
from services.user_courses import router as user_courses_router

app = FastAPI()

@app.get("/")
def get_db(db: Session = Depends(get_db)):
    if db is None:
        return {"message": "Database not connected"}
    return {"message": "Database connected"}

# Adicionando rotas de usuários
app.include_router(users_router)

# Adicionando rotas de cursos
app.include_router(courses_router)

# Adicionando rotas de cursos dos usuários
app.include_router(user_courses_router)