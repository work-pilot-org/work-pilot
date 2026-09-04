export interface EmployeeCreateRequest {
  employee_code: string;
  first_name: string;
  last_name: string;
  email: string;
  role: string;
  joining_date: string;
  employment_type: string;
  employment_status?: string;
  phone?: string;
  gender?: string;
  date_of_birth?: string;
  department_id?: string;
  designation_id?: string;
  manager_id?: string;
  work_location?: string;
}

export interface EmployeeResponse {
  id: string;
  auth_user_id?: string;
  employee_code: string;
  first_name: string;
  last_name: string;
  phone?: string;
  gender?: string;
  date_of_birth?: string;
  joining_date: string;
  employment_type: string;
  employment_status: string;
  department_id?: string;
  designation_id?: string;
  manager_id?: string;
  work_location?: string;
  profile_photo?: string;
  is_active: boolean;
  invitation_status?: string;
  created_at: string;
  updated_at: string;
}

export interface AttendanceResponse {
  id: number;
  employee_id: string;
  attendance_date: string;
  check_in?: string;
  check_out?: string;
  status: string;
  working_minutes: number;
  overtime_minutes: number;
  remarks?: string;
  created_at: string;
  updated_at: string;
}

export type LeaveStatus = "PENDING" | "APPROVED" | "REJECTED" | "CANCELLED";
export type LeaveType = "CASUAL" | "SICK" | "EARNED" | "MATERNITY" | "PATERNITY" | "COMP_OFF" | "UNPAID" | "OTHER";

export interface LeaveRequestResponse {
  id: string;
  employee_id: string;
  leave_type: LeaveType;
  start_date: string;
  end_date: string;
  total_days: number;
  reason: string;
  is_half_day: boolean;
  attachment_url?: string;
  emergency_contact?: string;
  status: LeaveStatus;
  workflow_instance_id?: string;
  created_at: string;
  updated_at: string;
}

export interface DepartmentResponse {
  id: number;
  name: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface DesignationResponse {
  id: number;
  name: string;
  department_id?: number;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface BranchResponse {
  id: number;
  name: string;
  location?: string;
  address?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ShiftResponse {
  id: number;
  name: string;
  start_time: string;
  end_time: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LeaveTypeResponse {
  id: number;
  name: string;
  description?: string;
  days_per_year: number;
  is_paid: boolean;
  carry_forward: boolean;
  is_active: boolean;
}

export interface LeaveBalanceResponse {
  id: string;
  employee_id: string;
  leave_type: LeaveType;
  year: number;
  allocated_days: number;
  used_days: number;
  carried_forward_days: number;
  remaining_days: number;
}

export interface HolidayResponse {
  id: string;
  name: string;
  date: string;
  is_optional: boolean;
  created_at: string;
  updated_at: string;
}

export interface LeaveReportItem {
  leave_type: LeaveType;
  total_requested: number;
  total_approved: number;
  total_pending: number;
  total_rejected: number;
}

export interface OrganizationLeaveReportResponse {
  start_date?: string;
  end_date?: string;
  total_employees_on_leave: number;
  report_items: LeaveReportItem[];
}

export interface PolicyBaseResponse {
  id: string;
  name: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LeavePolicyResponse extends PolicyBaseResponse {
  casual_leave_days: number;
  sick_leave_days: number;
  earned_leave_days: number;
  maternity_leave_days: number;
  paternity_leave_days: number;
  carry_forward_enabled: boolean;
  max_carry_forward: number;
  half_day_allowed: boolean;
  minimum_notice_days: number;
  requires_attachment: boolean;
}

export interface AttendancePolicyResponse extends PolicyBaseResponse {
  working_hours: number;
  grace_period: number;
  late_mark_limit: number;
  half_day_after_hours: number;
  auto_checkout: boolean;
  weekend_policy?: string;
}

export interface ShiftPolicyResponse extends PolicyBaseResponse {
  shift_start: string;
  shift_end: string;
  break_duration: number;
  weekly_off?: string;
  night_shift: boolean;
}

export interface HolidayPolicyResponse extends PolicyBaseResponse {
  calendar_name: string;
  country: string;
  state?: string;
  floating_holidays: number;
}

export interface ProbationPolicyResponse extends PolicyBaseResponse {
  duration_months: number;
  review_after_months: number;
  confirmation_required: boolean;
  notice_period: number;
}
