from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class StudentBase(BaseModel):
    name: str
    major: str
    gpa: float
    email: Optional[EmailStr] = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name must not be empty")
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return v

    @field_validator("major")
    @classmethod
    def major_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Major must not be empty")
        return v

    @field_validator("gpa")
    @classmethod
    def gpa_must_be_valid(cls, v: float) -> float:
        if v < 0.0 or v > 20.0:
            raise ValueError("GPA must be between 0.0 and 20.0")
        return round(v, 2)

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        v = v.strip().lower()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v


class StudentCreate(StudentBase):
    id: int

    @field_validator("id")
    @classmethod
    def id_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("ID must be a positive integer")
        return v


class StudentUpdate(StudentBase):
    """Used for full update (PUT). All fields required."""
    pass


class StudentResponse(StudentBase):
    id: int

    model_config = {"from_attributes": True}
