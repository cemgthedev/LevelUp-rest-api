from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from user import User
    from course import Course

# UserCourses Entity
class UserCourses(SQLModel, table=True):
    __tablename__ = "user_courses"  # Table name
    id: int = Field(default=None, primary_key=True)
    buyer_id: int = Field(foreign_key="users.id")  # Foreign Key for User Buyer
    seller_id: int = Field(foreign_key="users.id")  # Foreign Key for User Seller
    course_id: int = Field(foreign_key="courses.id")  # Foreign Key for Course
    purchased: bool = Field(default=False)
    purchased_at: Optional[datetime]
    created_at: datetime = Field(default_factory=datetime.now)
    buyer: "User" = Relationship(
        sa_relationship_kwargs={"primaryjoin": "UserCourses.buyer_id == User.id"},
        back_populates="purchased_courses"
    )
    seller: "User" = Relationship(
        sa_relationship_kwargs={"primaryjoin": "UserCourses.seller_id == User.id"},
        back_populates="sold_courses"
    )
    course: "Course" = Relationship(back_populates="user_courses")