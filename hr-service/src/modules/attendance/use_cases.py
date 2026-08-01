from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.attendance.models import Attendance
from src.modules.attendance.schemas import (
    AttendanceCheckIn,
    AttendanceCheckOut,
    AttendanceCreate,
    AttendanceStatusUpdate,
    AttendanceUpdate,
)
from src.modules.attendance.service import AttendanceService

class AttendanceUseCases:
    def __init__(self, db: Session):
        self.service = AttendanceService(db)
        
    def create_attendance(self, data: AttendanceCreate) -> Attendance:
        return self.service.create_attendance(data)
        
    def get_all_attendance(self, skip: int = 0, limit: int = 100) -> list[Attendance]:
        return self.service.get_all_attendance(skip, limit)
        
    def get_attendance(self, attendance_id: int) -> Attendance:
        return self.service.get_attendance(attendance_id)
        
    def update_attendance(self, attendance_id: int, data: AttendanceUpdate) -> Attendance:
        return self.service.update_attendance(attendance_id, data)
        
    def delete_attendance(self, attendance_id: int) -> None:
        return self.service.delete_attendance(attendance_id)
        
    def check_in(self, data: AttendanceCheckIn) -> Attendance:
        return self.service.check_in(data)
        
    def check_out(self, data: AttendanceCheckOut) -> Attendance:
        return self.service.check_out(data)
        
    def update_status(self, attendance_id: int, data: AttendanceStatusUpdate) -> Attendance:
        return self.service.update_status(attendance_id, data)
        
    def get_employee_attendance(self, employee_id: UUID) -> list[Attendance]:
        return self.service.get_employee_attendance(employee_id)
        
    def get_employee_summary(self, employee_id: UUID) -> dict[str, object]:
        return self.service.get_employee_summary(employee_id)
        
    def get_attendance_by_date(self, attendance_date: date) -> list[Attendance]:
        return self.service.get_attendance_by_date(attendance_date)
        
    def get_today_attendance(self) -> list[Attendance]:
        return self.service.get_today_attendance()
        
    def get_active_attendance(self) -> list[Attendance]:
        return self.service.get_active_attendance()
        
    def get_monthly_report(self, month: int, year: int) -> dict[str, object]:
        return self.service.get_monthly_report(month, year)
        
    def export_attendance(self, month: int, year: int) -> dict[str, str]:
        return self.service.export_attendance(month, year)
