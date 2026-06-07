from typing import Literal

from fastapi import APIRouter, HTTPException, Query, status

from app.models.student import StudentCreate, StudentUpdate, StudentResponse
from app.services import (
    get_all_students,
    get_student_by_id,
    search_students,
    create_student,
    update_student,
    delete_student,
    create_backup,
)

router = APIRouter(prefix="/students", tags=["Students"])


# ── GET /students/ ─────────────────────────────────────────────────────────
@router.get(
    "/",
    summary="Get all students",
    description="Returns a paginated, sortable list of all stored students.",
)
def list_students(
    page: int = Query(default=1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(default=10, ge=1, le=100, description="Items per page"),
    sort_by: Literal["id", "name", "gpa"] = Query(default="id", description="Sort field"),
    order: Literal["asc", "desc"] = Query(default="asc", description="Sort direction"),
):
    return get_all_students(page=page, page_size=page_size, sort_by=sort_by, order=order)


# ── GET /students/{id} ─────────────────────────────────────────────────────
@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get student by ID",
)
def read_student(student_id: int):
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )
    return student


# ── POST /students/ ────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new student",
)
def add_student(student: StudentCreate):
    try:
        return create_student(student)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


# ── PUT /students/{id} ─────────────────────────────────────────────────────
@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update student data",
)
def modify_student(student_id: int, student: StudentUpdate):
    updated = update_student(student_id, student)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )
    return updated


# ── DELETE /students/{id} ──────────────────────────────────────────────────
@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a student",
)
def remove_student(student_id: int):
    success = delete_student(student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )
    return {"message": f"Student with ID {student_id} deleted successfully"}
