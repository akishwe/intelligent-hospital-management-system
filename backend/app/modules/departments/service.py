from sqlalchemy.orm import Session
from backend.app.modules.departments.schemas import DepartmentCreate, DepartmentUpdate
from app.modules.departments.models import Department
from app.core.exceptions import PatientException

class DepartmentService:

    @staticmethod
    def create_department(db: Session, department_data: DepartmentCreate):
        existing = db.query(Department).filter(Department.name == department_data.name, Department.is_deleted == False).first()
        if existing:
            raise PatientException(f"Department '{department_data.name}' already exists.")
        department = Department(**department_data.model_dump())
        db.add(department)
        db.commit()
        db.refresh(department)
        return department

    @staticmethod
    def get_department(db: Session, department_id: int):
        department = db.query(Department).filter(Department.id == department_id, Department.is_deleted == False).first()
        if not department:
            raise PatientException("Department not found.")
        return department

    @staticmethod
    def get_departments(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Department).filter(Department.is_deleted == False).offset(skip).limit(limit).all()

    @staticmethod
    def update_department(db: Session, department_id: int, department_data: DepartmentUpdate):
        department = db.query(Department).filter(Department.id == department_id, Department.is_deleted == False).first()
        if not department:
            raise PatientException("Department not found.")
        for field, value in department_data.model_dump(exclude_unset=True).items():
            setattr(department, field, value)
        db.commit()
        db.refresh(department)
        return department

    @staticmethod
    def delete_department(db: Session, department_id: int):
        department = db.query(Department).filter(Department.id == department_id, Department.is_deleted == False).first()
        if not department:
            raise PatientException("Department not found.")
        department.soft_delete()
        db.commit()
        return {"detail": "Department deleted successfully."}