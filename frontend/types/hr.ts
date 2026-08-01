export interface EmployeeResponse {
  id: string;
  auth_user_id: string;
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

export interface LeaveRequestResponse {
  id: string;
  employee_id: string;
  leave_type: string;
  start_date: string;
  end_date: string;
  total_days: number;
  reason: string;
  is_half_day: boolean;
  attachment_url?: string;
  emergency_contact?: string;
  status: string;
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
