from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from user_courses import UserCourses

# Course Entity
class Course(SQLModel, table=True):
    __tablename__ = "courses"  # Table name
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    workload: int
    price: float
    banner_url: str
    course_url: str
    seller_id: int = Field(foreign_key="users.id")
    
    # Relacionamentos
    user_courses: List["UserCourses"] = Relationship(
        back_populates="course"
    )