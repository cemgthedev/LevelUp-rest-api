from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from user_courses import UserCourses

# User Entity
class User(SQLModel, table=True):
    __tablename__ = "users"  # Table name
    id: int = Field(default=None, primary_key=True)
    name: str
    cpf: str
    email: str
    password: str
    age: Optional[int]
    phone_number: str
    address: Optional[str]
    gender: Optional[str]
    sold_courses: List["UserCourses"] = Relationship(
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "foreign_keys": "[UserCourses.seller_id]"
        },
    )
    purchased_courses: List["UserCourses"] = Relationship( 
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "foreign_keys": "[UserCourses.buyer_id]"
        },
        back_populates="buyer",
    )