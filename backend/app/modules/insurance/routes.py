from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.modules.departments.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.modules.departments.service import DepartmentService
from app.core.database import get_db
from app.core.deps import require_roles
from app.core.enums import UserRole

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/", response_model=List[DepartmentResponse])
def list_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE
    ]))
):
    service = DepartmentService(db)
    return service.get_departments(skip, limit)


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE
    ]))
):
    service = DepartmentService(db)
    department = service.get_department(department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN
    ]))
):
    service = DepartmentService(db)
    return service.create_department(department)


@router.patch("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    update_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN
    ]))
):
    service = DepartmentService(db)
    department = service.update_department(department_id, update_data)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN
    ]))
):
    service = DepartmentService(db)
    success = service.delete_department(department_id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")
    return None