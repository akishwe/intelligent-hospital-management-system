from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.modules.departments.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.modules.departments.service import DepartmentService
from app.core.database import get_db
from app.core.security import require_roles
from app.core.enums import UserRole


router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([UserRole.SUPER_ADMIN, UserRole.ADMIN]))
):
    return DepartmentService.create_department(db, department_data)

@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE
    ]))
):
    return DepartmentService.get_department(db, department_id)

@router.get("/", response_model=List[DepartmentResponse])
def get_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([
        UserRole.SUPER_ADMIN,
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE
    ]))
):
    return DepartmentService.get_departments(db, skip, limit)

@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([UserRole.SUPER_ADMIN, UserRole.ADMIN]))
):
    return DepartmentService.update_department(db, department_id, department_data)

@router.delete("/{department_id}", status_code=status.HTTP_200_OK)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles([UserRole.SUPER_ADMIN]))
):
    return DepartmentService.delete_department(db, department_id)