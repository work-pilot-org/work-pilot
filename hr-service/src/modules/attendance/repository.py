from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from src.modules.attendance.models import Attendance, AttendanceStatus


class AttendanceRepository:
    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # Create
    # =====================================================

    def create(self, attendance: Attendance) -> Attendance:
        self.db.add(attendance)
        self.db.flush()
        self.db.refresh(attendance)
        return attendance

    # =====================================================
    # Get By ID
    # =====================================================

    def get_by_id(
        self,
        attendance_id: int,
    ) -> Optional[Attendance]:
        return self.db.get(Attendance, attendance_id)

    # =====================================================
    # Get All
    # =====================================================

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Attendance]:

        stmt = (
            select(Attendance)
            .order_by(Attendance.attendance_date.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        attendance: Attendance,
    ) -> Attendance:

        self.db.flush()
        self.db.refresh(attendance)
        return attendance

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        attendance: Attendance,
    ) -> None:

        self.db.delete(attendance)
        self.db.flush()

    # =====================================================
    # Employee Attendance
    # =====================================================

    def get_by_employee(
        self,
        employee_id: UUID,
    ) -> list[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                Attendance.employee_id == employee_id
            )
            .order_by(
                Attendance.attendance_date.desc()
            )
        )

        return list(self.db.scalars(stmt).all())

    # =====================================================
    # Employee Attendance By Date
    # =====================================================

    def get_by_employee_and_date(
        self,
        employee_id: UUID,
        attendance_date: date,
    ) -> Optional[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                and_(
                    Attendance.employee_id == employee_id,
                    Attendance.attendance_date == attendance_date,
                )
            )
        )

        return self.db.scalar(stmt)

    # =====================================================
    # Attendance By Date
    # =====================================================

    def get_by_date(
        self,
        attendance_date: date,
    ) -> list[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                Attendance.attendance_date == attendance_date
            )
            .order_by(Attendance.employee_id)
        )

        return list(self.db.scalars(stmt).all())

    # =====================================================
    # Today's Attendance
    # =====================================================

    def get_today(
        self,
        today: date,
    ) -> list[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                Attendance.attendance_date == today
            )
            .order_by(Attendance.employee_id)
        )

        return list(self.db.scalars(stmt).all())

    # =====================================================
    # Active Check-ins
    # =====================================================

    def get_active(self) -> list[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                Attendance.attendance_date == date.today(),
                Attendance.check_in.is_not(None),
                Attendance.check_out.is_(None),
            )
            .order_by(Attendance.check_in)
        )

        return list(self.db.scalars(stmt).all())

    # =====================================================
    # Monthly Attendance
    # =====================================================

    def get_monthly(
        self,
        month: int,
        year: int,
    ) -> list[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                func.extract(
                    "month",
                    Attendance.attendance_date,
                )
                == month,
                func.extract(
                    "year",
                    Attendance.attendance_date,
                )
                == year,
            )
            .order_by(
                Attendance.employee_id,
                Attendance.attendance_date,
            )
        )

        return list(self.db.scalars(stmt).all())

    # =====================================================
    # Employee Summary
    # =====================================================

    def get_summary(
        self,
        employee_id: UUID,
    ) -> dict:

        records = self.get_by_employee(employee_id)

        return {
            "total_days": len(records),
            "present_days": sum(
                record.status == AttendanceStatus.PRESENT
                for record in records
            ),
            "absent_days": sum(
                record.status == AttendanceStatus.ABSENT
                for record in records
            ),
            "half_days": sum(
                record.status == AttendanceStatus.HALF_DAY
                for record in records
            ),
            "late_days": sum(
                record.status == AttendanceStatus.LATE
                for record in records
            ),
            "total_working_minutes": sum(
                record.working_minutes
                for record in records
            ),
            "total_overtime_minutes": sum(
                record.overtime_minutes
                for record in records
            ),
        }
