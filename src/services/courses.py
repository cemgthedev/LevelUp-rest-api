from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, and_, select
from sqlalchemy.sql import func
from database import get_db
from models.course import Course
from math import ceil
from services.configs import users_logger as logger

# Criar roteador
router = APIRouter()

# Rota para criar um novo curso
@router.post("/courses")
async def create_course(course: Course, db: Session = Depends(get_db)):
    try:
        logger.info(f"Criando um novo curso...")
        db.add(course)
        db.commit()
        db.refresh(course)
        logger.info(f"Curso criado com sucesso!")
        return {"message": "Course created successfully", "data": course}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar um novo curso: {str(e)}")
        return {"error": str(e)}
    
# Rota para atualizar um curso
@router.put("/courses/{id}")
async def update_course(id: int, updated_course: Course, db: Session = Depends(get_db)):
    try:
        logger.info(f"Atualizando curso com ID: {id}")
        course = db.exec(select(Course).where(Course.id == id)).first()
        if course is None:
            logger.warning(f"Curso com ID {id} não encontrado")
            raise HTTPException(status_code=404, detail="Course not found")
        course.title = updated_course.title
        course.description = updated_course.description
        course.workload = updated_course.workload
        course.price = updated_course.price
        course.url = updated_course.url
        
        db.commit()
        db.refresh(course)
        logger.info(f"Curso atualizado com sucesso!")
        return {"message": "Course updated successfully", "data": course}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar um curso: {str(e)}")
        return {"error": str(e)}
    
# Rota para deletar um curso
@router.delete("/courses/{id}")
async def delete_course(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Removendo curso com ID: {id}")
        course = db.exec(select(Course).where(Course.id == id)).first()
        if course is None:
            logger.warning(f"Curso com ID {id} não encontrado")
            raise HTTPException(status_code=404, detail="Course not found")
        
        db.delete(course)
        db.commit()
        logger.info(f"Curso removido com sucesso!")
        return {"message": "Course deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao remover um curso: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# Rota para pegar curso pelo id
@router.get("/courses/{id}")
async def get_course(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Buscando curso com ID: {id}")
        course = db.exec(select(Course).where(Course.id == id)).first()
        if course is None:
            logger.warning(f"Curso com ID {id} não encontrado")
            raise HTTPException(status_code=404, detail="Course not found")
        
        logger.info(f"Curso encontrado: {course}")
        return {"message": "Course found successfully", "data": course}
    except Exception as e:
        return {"error": str(e)}
    
# Rota para listar cursos
@router.get("/courses")
async def get_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page (max 100)"),
    title: Optional[str] = Query(None, description="Filter by course title"),
    min_price: Optional[float] = Query(None, description="Filter by minimum price"),
    max_price: Optional[float] = Query(None, description="Filter by maximum price"),
    min_workload: Optional[int] = Query(None, description="Filter by minimum workload"),
    max_workload: Optional[int] = Query(None, description="Filter by maximum workload"),
):
    try:
        logger.info(f"Buscando cursos...")
        filters = []
        if title:
            filters.append(Course.title.ilike(f"%{title}%"))
        if min_price is not None:
            filters.append(Course.price >= min_price)
        if max_price is not None:
            filters.append(Course.price <= max_price)
        if min_workload is not None:
            filters.append(Course.workload >= min_workload)
        if max_workload is not None:
            filters.append(Course.workload <= max_workload)
        
        offset = (page - 1) * limit
        stmt = select(Course).where(and_(*filters)).offset(offset).limit(limit) if filters else select(Course).offset(offset).limit(limit)
        courses = db.exec(stmt).all()

        total_courses = db.exec(select(func.count()).select_from(Course).where(and_(*filters))).first() if filters else db.exec(select(func.count()).select_from(Course)).first()
        total_pages = ceil(total_courses / limit)
        
        if total_courses > 0:
            logger.info(f"Cursos encontrados com sucesso!")
        else:
            logger.warning(f"Nenhum curso encontrado!")
            raise HTTPException(status_code=404, detail="No courses found")
            
        return {
            "message": "Courses found successfully",
            "data": courses,
            "page": page,
            "limit": limit,
            "total_courses": total_courses,
            "total_pages": total_pages
        }
    except Exception as e:
        return {"error": str(e)}