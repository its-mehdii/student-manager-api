import json
import shutil
import logging
from pathlib import Path
from typing import List, Optional, Literal
from datetime import datetime

from app.models.student import StudentCreate, StudentUpdate, StudentResponse

# ─────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = BASE_DIR / "data" / "students.json"
BACKUP_DIR = BASE_DIR / "data" / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("student_service")


# ─────────────────────────────────────────────
# JSON I/O helpers
# ─────────────────────────────────────────────
def _load_students() -> List[dict]:
    """Read all students from the JSON file."""
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        logger.error("Corrupted JSON file: %s", exc)
        return []


def _save_students(students: List[dict]) -> None:
    """Write students list back to the JSON file atomically."""
    tmp = DATA_FILE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)
    tmp.replace(DATA_FILE)  # atomic replace
    logger.debug("Saved %d students to %s", len(students), DATA_FILE)


# ─────────────────────────────────────────────
# Backup helper
# ─────────────────────────────────────────────
def create_backup() -> str:
    """Copy the current JSON file to the backups folder."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = BACKUP_DIR / f"students_backup_{timestamp}.json"
    shutil.copy2(DATA_FILE, dest)
    logger.info("Backup created: %s", dest)
    return str(dest)


# ─────────────────────────────────────────────
# CRUD operations
# ─────────────────────────────────────────────
def get_all_students(
    page: int = 1,
    page_size: int = 10,
    sort_by: Literal["id", "name", "gpa"] = "id",
    order: Literal["asc", "desc"] = "asc",
) -> dict:
    """Return a paginated, sorted list of students."""
    students = _load_students()

    # Sort
    reverse = order == "desc"
    students.sort(key=lambda s: s.get(sort_by, 0), reverse=reverse)

    # Paginate
    total = len(students)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = students[start:end]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, -(-total // page_size)),  # ceiling division
        "students": [StudentResponse(**s) for s in page_items],
    }


def get_student_by_id(student_id: int) -> Optional[StudentResponse]:
    """Return a single student or None if not found."""
    students = _load_students()
    for s in students:
        if s["id"] == student_id:
            return StudentResponse(**s)
    return None


def search_students(query: str) -> List[StudentResponse]:
    """Case-insensitive substring search on the name field."""
    students = _load_students()
    q = query.strip().lower()
    results = [s for s in students if q in s["name"].lower()]
    return [StudentResponse(**s) for s in results]


def create_student(data: StudentCreate) -> StudentResponse:
    """Add a new student; raise ValueError if ID already exists."""
    students = _load_students()
    if any(s["id"] == data.id for s in students):
        raise ValueError(f"Student with ID {data.id} already exists")
    new_student = data.model_dump()
    students.append(new_student)
    _save_students(students)
    logger.info("Created student id=%d name=%s", data.id, data.name)
    return StudentResponse(**new_student)


def update_student(student_id: int, data: StudentUpdate) -> Optional[StudentResponse]:
    """Full update of an existing student. Returns None if not found."""
    students = _load_students()
    for idx, s in enumerate(students):
        if s["id"] == student_id:
            updated = {"id": student_id, **data.model_dump()}
            students[idx] = updated
            _save_students(students)
            logger.info("Updated student id=%d", student_id)
            return StudentResponse(**updated)
    return None


def delete_student(student_id: int) -> bool:
    """Delete a student. Returns True on success, False if not found."""
    students = _load_students()
    new_list = [s for s in students if s["id"] != student_id]
    if len(new_list) == len(students):
        return False  # not found
    _save_students(new_list)
    logger.info("Deleted student id=%d", student_id)
    return True
