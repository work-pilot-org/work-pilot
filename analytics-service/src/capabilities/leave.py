capability_name = "Leave"
description = "Analyzes employee leave requests, pending approvals, and leave utilization."

supported_questions = [
    "How many leave requests are pending?",
    "Which department took the most leave?",
    "How many leaves were approved this month?",
    "What type of leave is used the most?",
    "What is our leave utilization?",
]

required_data = {
    "facts": ["FactLeave"],
    "dimensions": ["DimEmployee", "DimDepartment", "DimDate"],
    "events": ["hr.leave"]
}

allowed_filters = ["period", "department", "employee", "status", "leave_type"]

analytics_api = "GET /analytics/hr/leave-utilization"
