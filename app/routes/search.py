from fastapi import APIRouter, Query, HTTPException, status
from typing import List

from app.models.student import StudentResponse
from app.services import search_students, create_backup

router = APIRouter(tags=["Search & Backup"])


# ── GET /search/?q=... ─────────────────────────────────────────────────────
@router.get(
    "/search/",
    response_model=List[StudentResponse],
    summary="Search students by name",
    description="Returns all students whose name contains the query string (case-insensitive).",
)
def search(q: str = Query(..., min_length=1, description="Name search query")):
    results = search_students(q)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No students found matching '{q}'",
        )
    return results


# ── POST /backup/ ──────────────────────────────────────────────────────────
@router.post(
    "/backup/",
    summary="Create a data backup",
    description="Saves a timestamped backup of the current students JSON file.",
    tags=["Backup"],
)
def backup():
    path = create_backup()
    return {"message": "Backup created successfully", "backup_file": path}
