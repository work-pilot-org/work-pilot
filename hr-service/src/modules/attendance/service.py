import csv
from datetime import date, datetime, timedelta
from pathlib import Path
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.attendance.models import Attendance, AttendanceStatus
from src.modules.attendance.repository import AttendanceRepository
from src.modules.attendance.schemas import (
    AttendanceCheckIn,
    AttendanceCheckOut,
    AttendanceCreate,
    AttendanceStatusUpdate,
    AttendanceUpdate,
)


class AttendanceService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AttendanceRepository(db)

    # --------------------------------------------------
    # Create Attendance
    # --------------------------------------------------

    def create_attendance(
        self,
        attendance_data: AttendanceCreate,
    ) -> Attendance:
        existing = self.repository.get_by_employee_and_date(
            attendance_data.employee_id,
            attendance_data.attendance_date,
        )

        if existing:
            raise ValueError("Attendance already exists for this employee.")

        attendance = Attendance(**attendance_data.model_dump())

        try:
            attendance = self.repository.create(attendance)
            self.db.commit()
            return attendance
        except Exception:
            self.db.rollback()
            raise

    # --------------------------------------------------
    # Get All Attendance
    # --------------------------------------------------

    def get_all_attendance(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Attendance]:
        return self.repository.get_all(skip, limit)

    # --------------------------------------------------
    # Get Attendance By Id
    # --------------------------------------------------

    def get_attendance(
        self,
        attendance_id: int,
    ) -> Attendance:
        attendance = self.repository.get_by_id(attendance_id)

        if not attendance:
            raise ValueError("Attendance not found.")

        return attendance

    # --------------------------------------------------
    # Update Attendance
    # --------------------------------------------------

    def update_attendance(
        self,
        attendance_id: int,
        attendance_data: AttendanceUpdate,
    ) -> Attendance:
        attendance = self.get_attendance(attendance_id)

        for field, value in attendance_data.model_dump(exclude_unset=True).items():
            setattr(attendance, field, value)

        try:
            attendance = self.repository.update(attendance)
            self.db.commit()
            return attendance
        except Exception:
            self.db.rollback()
            raise

    # --------------------------------------------------
    # Delete Attendance
    # --------------------------------------------------

    def delete_attendance(
        self,
        attendance_id: int,
    ) -> None:
        attendance = self.get_attendance(attendance_id)

        try:
            self.repository.delete(attendance)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    # --------------------------------------------------
    # Employee Check In
    # --------------------------------------------------

    def check_in(
        self,
        checkin_data: AttendanceCheckIn,
    ) -> Attendance:
        today = date.today()

        attendance = self.repository.get_by_employee_and_date(
            checkin_data.employee_id,
            today,
        )

        if attendance and attendance.check_in:
            raise ValueError("Employee already checked in.")

        if not attendance:
            attendance = Attendance(
                employee_id=checkin_data.employee_id,
                attendance_date=today,
                check_in=datetime.now().time(),
                status=AttendanceStatus.PRESENT,
            )

            try:
                attendance = self.repository.create(attendance)
                self.db.commit()
                return attendance
            except Exception:
                self.db.rollback()
                raise

        attendance.check_in = datetime.now().time()
        if attendance.status == AttendanceStatus.ABSENT:
            attendance.status = AttendanceStatus.PRESENT

        try:
            attendance = self.repository.update(attendance)
            self.db.commit()
            return attendance
        except Exception:
            self.db.rollback()
            raise

    # --------------------------------------------------
    # Employee Check Out
    # --------------------------------------------------

    def check_out(
        self,
        checkout_data: AttendanceCheckOut,
    ) -> Attendance:
        today = date.today()

        attendance = self.repository.get_by_employee_and_date(
            checkout_data.employee_id,
            today,
        )

        if not attendance:
            yesterday = today - timedelta(days=1)
            attendance = self.repository.get_by_employee_and_date(
                checkout_data.employee_id,
                yesterday,
            )
            if not attendance or attendance.check_out:
                raise ValueError("Employee has not checked in.")

        if attendance.check_out:
            raise ValueError("Employee already checked out.")

        attendance.check_out = datetime.now().time()

        if attendance.check_in:
            checkin = datetime.combine(attendance.attendance_date, attendance.check_in)
            checkout = datetime.combine(today, attendance.check_out)

            if checkout < checkin:
                checkout += timedelta(days=1)

            total_minutes = int((checkout - checkin).total_seconds() / 60)

            attendance.working_minutes = total_minutes
            attendance.overtime_minutes = max(total_minutes - 480, 0)

        try:
            attendance = self.repository.update(attendance)
            self.db.commit()
            return attendance
        except Exception:
            self.db.rollback()
            raise

    # --------------------------------------------------
    # Update Attendance Status
    # --------------------------------------------------

    def update_status(
        self,
        attendance_id: int,
        status_data: AttendanceStatusUpdate,
    ) -> Attendance:
        attendance = self.get_attendance(attendance_id)
        attendance.status = status_data.status

        try:
            attendance = self.repository.update(attendance)
            self.db.commit()
            return attendance
        except Exception:
            self.db.rollback()
            raise

    # --------------------------------------------------
    # Get Employee Attendance
    # GET /attendance/employee/{employee_id}
    # --------------------------------------------------

    def get_employee_attendance(self, employee_id: UUID) -> list[Attendance]:
        return self.repository.get_by_employee(employee_id)

    # --------------------------------------------------
    # Employee Attendance Summary
    # GET /attendance/employee/{employee_id}/summary
    # --------------------------------------------------

    def get_employee_summary(self, employee_id: UUID) -> dict[str, object]:
        summary = self.repository.get_summary(employee_id)
        summary["employee_id"] = employee_id
        return summary

    # --------------------------------------------------
    # Attendance By Date
    # GET /attendance/date/{date}
    # --------------------------------------------------

    def get_attendance_by_date(self, attendance_date: date) -> list[Attendance]:
        return self.repository.get_by_date(attendance_date)

    # --------------------------------------------------
    # Today's Attendance
    # GET /attendance/today
    # --------------------------------------------------

    def get_today_attendance(self) -> list[Attendance]:
        return self.repository.get_today(date.today())

    # --------------------------------------------------
    # Active Employees
    # GET /attendance/active
    # --------------------------------------------------

    def get_active_attendance(self) -> list[Attendance]:
        return self.repository.get_active()

    # --------------------------------------------------
    # Monthly Report
    # GET /attendance/report/monthly
    # --------------------------------------------------

    def get_monthly_report(
        self,
        month: int,
        year: int,
    ) -> dict[str, object]:
        records = self.repository.get_monthly(month, year)

        return {
            "month": month,
            "year": year,
            "total_days": len(records),
            "present_days": sum(
                record.status == AttendanceStatus.PRESENT for record in records
            ),
            "absent_days": sum(
                record.status == AttendanceStatus.ABSENT for record in records
            ),
            "half_days": sum(
                record.status == AttendanceStatus.HALF_DAY for record in records
            ),
            "late_days": sum(
                record.status == AttendanceStatus.LATE for record in records
            ),
            "total_working_minutes": sum(
                record.working_minutes for record in records
            ),
            "total_overtime_minutes": sum(
                record.overtime_minutes for record in records
            ),
            "records": records,
        }

    # --------------------------------------------------
    # Export Attendance
    # GET /attendance/export
    # --------------------------------------------------

    def export_attendance(
        self,
        month: int,
        year: int,
    ) -> dict[str, str]:
        if month < 1 or month > 12:
            raise ValueError("month must be between 1 and 12")
        if year < 1900 or year > 2100:
            raise ValueError("year must be between 1900 and 2100")

        records = self.repository.get_monthly(month, year)

        export_dir = Path("exports").resolve()
        export_dir.mkdir(exist_ok=True)

        file_path = (export_dir / f"attendance_{year}_{month}.csv").resolve()
        try:
            file_path.relative_to(export_dir)
        except ValueError as exc:
            raise ValueError("Invalid export path.") from exc

        with open(
            file_path,
            mode="w",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(
                [
                    "Employee ID",
                    "Date",
                    "Check In",
                    "Check Out",
                    "Status",
                    "Working Minutes",
                    "Overtime Minutes",
                    "Remarks",
                ]
            )

            for record in records:
                writer.writerow(
                    [
                        record.employee_id,
                        record.attendance_date,
                        record.check_in,
                        record.check_out,
                        record.status.value,
                        record.working_minutes,
                        record.overtime_minutes,
                        record.remarks,
                    ]
                )

        return {
            "message": "Attendance exported successfully.",
            "file_path": str(file_path),
        }
