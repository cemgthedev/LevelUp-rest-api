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