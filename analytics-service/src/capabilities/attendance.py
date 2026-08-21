capability_name = "Attendance"
description = "Analyzes employee attendance, worked hours, and overtime metrics."

supported_questions = [
    "Who worked the most overtime?",
    "What is our attendance rate?",
    "Which department worked the most hours?",
    "How much overtime did we have last month?",
]

required_data = {
    "facts": ["FactAttendance"],
    "dimensions": ["DimEmployee", "DimDepartment", "DimDate"],
    "events": ["hr.attendance"]
}

allowed_filters = ["period", "department", "employee", "status"]

analytics_api = "GET /analytics/hr/attendance-summary"
