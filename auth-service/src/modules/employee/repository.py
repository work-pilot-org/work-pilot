from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.employee.models import Employee


class EmployeeRepository:

    def create_employee(
        self,
        db: Session,
        employee: Employee
    ) -> Employee:
        db.add(employee)
        db.flush()
        db.refresh(employee)

        return employee

    def get_employee_by_id(
        self,
        db: Session,
        employee_id: UUID
    ) -> Employee | None:
        return (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

    def get_employee_by_user_id(
        self,
        db: Session,
        user_id: UUID
    ) -> Employee | None:
        return (
            db.query(Employee)
            .filter(Employee.user_id == user_id)
            .first()
        )

    def get_all_employees(
        self,
        db: Session
    ) -> list[Employee]:
        return (
            db.query(Employee)
            .all()
        )

    def update_employee(
        self,
        db: Session,
        employee: Employee
    ) -> Employee:
        db.flush()
        db.refresh(employee)

        return employee

    def delete_employee(
        self,
        db: Session,
        employee: Employee
    ) -> None:
        db.delete(employee)
        db.flush()