from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy.sql import func
from database import get_db
from models import User, Course, UserCourses
from math import ceil
from services.configs import users_logger as logger

# Criar roteador
router = APIRouter()

# Rota para adicionar curso para usuário
@router.post("/user_courses")
async def create_user_course(user_courses: UserCourses, db: Session = Depends(get_db)):
    try:
        logger.info(f"Adicionando um curso para usuário...")
        buyer = db.exec(select(User).where(User.id == user_courses.buyer_id)).first()
        if buyer is None:
            logger.warning(f"Usuário com ID {user_courses.buyer_id} não encontrado")
            raise HTTPException(status_code=404, detail="Buyer not found")
        
        seller = db.exec(select(User).where(User.id == user_courses.seller_id)).first()
        if seller is None:
            logger.warning(f"Usuário com ID {user_courses.seller_id} não encontrado")
            raise HTTPException(status_code=404, detail="Seller not found")
        
        course = db.exec(select(Course).where(Course.id == user_courses.course_id)).first()
        if course is None:
            logger.warning(f"Curso com ID {user_courses.course_id} não encontrado")
            raise HTTPException(status_code=404, detail="Course not found")
        
        db.add(user_courses)
        db.commit()
        db.refresh(user_courses)
        logger.info(f"Curso adicionado para usuário com sucesso!")
        return {"message": "Course added for user successfully", "data": user_courses}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao adicionar um novo curso a um usuário: {str(e)}")
        return {"error": str(e)}
    
# Rota para atualizar um curso para um usuário
@router.put("/user_courses/{id}")
async def update_user_course(id: int, updated_user_course: UserCourses, db: Session = Depends(get_db)):
    try:
        logger.info(f"Atualizando curso para usuário com ID: {id}")
        user_course = db.exec(select(UserCourses).where(UserCourses.id == id)).first()
        if user_course is None:
            logger.warning(f"Curso para usuário com ID {id} não encontrado")
            raise HTTPException(status_code=404, detail="Course not found")
        
        if user_course.purchased_at is not None:
            logger.warning(f"Curso para usuário com ID {id} ja foi comprado")
            raise HTTPException(status_code=400, detail="Course already purchased")
        
        buyer = db.exec(select(User).where(User.id == user_course.buyer_id)).first()
        if buyer is None:
            logger.warning(f"Usuário com ID {user_course.buyer_id} não encontrado")
            raise HTTPException(status_code=404, detail="User not found")
        
        seller = db.exec(select(User).where(User.id == user_course.seller_id)).first()
        if seller is None:
            logger.warning(f"Usuário com ID {user_course.seller_id} não encontrado")
            raise HTTPException(status_code=404, detail="User not found")
        
        course = db.exec(select(Course).where(Course.id == user_course.course_id)).first()
        if course is None:
            logger.warning(f"Curso com ID {user_course.course_id} não encontrado")
            raise HTTPException(status_code=404, detail="Course not found")
        
        user_course.purchased = updated_user_course.purchased
        user_course.purchased_at = datetime.now()
        
        db.commit()
        db.refresh(user_course)
        logger.info(f"Curso para usuário atualizado com sucesso!")
        return {"message": "Course for user updated successfully", "data": user_course}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar um curso para usuário: {str(e)}")
        return {"error": str(e)}
    
# Rota para deletar um curso de um usuário
@router.delete("/user_courses/{id}")
async def delete_user_course(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Removendo curso para usuário com ID: {id}")
        course = db.exec(select(Course).where(Course.id == id)).first()
        if course is None:
            logger.warning(f"Curso para usuário com ID {id} não encontrado")
            raise HTTPException(status_code=404, detail="Course for user not found")
        
        db.delete(course)
        db.commit()
        logger.info(f"Curso para usuário removido com sucesso!")
        return {"message": "Course for user deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover um curso para usuário: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# Rota para pegar curso para usuário pelo id
@router.get("/user_courses/{id}")
async def get_user_course(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Buscando curso para usuário com ID: {id}")
        user_course = db.exec(select(UserCourses).where(UserCourses.id == id)).first()
        if user_course is None:
            logger.warning(f"Curso para usuário com ID {id} não encontrado")
            raise HTTPException(status_code=404, detail="Course for user not found")
        
        logger.info(f"Curso para usuário encontrado: {user_course}")
        return {"message": "Course for user found successfully", "data": user_course}
    except Exception as e:
        return {"error": str(e)}
    
# Rota para listar cursos dos usuários
@router.get("/user_courses")
async def get_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page (max 100)"),
):
    try:
        logger.info(f"Buscando cursos dos usuários...")
        
        offset = (page - 1) * limit
        stmt = select(UserCourses).offset(offset).limit(limit)
        user_courses = db.exec(stmt).all()

        total_user_courses = db.exec(select(func.count()).select_from(UserCourses)).first()
        total_pages = ceil(total_user_courses / limit)
        
        if total_user_courses > 0:
            logger.info(f"Cursos dos usuários encontrados com sucesso!")
        else:
            logger.warning(f"Nenhum curso dos usuários encontrado!")
            raise HTTPException(status_code=404, detail="No courses for users found")
            
        return {
            "message": "Courses for users found successfully",
            "data": user_courses,
            "page": page,
            "limit": limit,
            "total_user_courses": total_user_courses,
            "total_pages": total_pages
        }
    except Exception as e:
        return {"error": str(e)}