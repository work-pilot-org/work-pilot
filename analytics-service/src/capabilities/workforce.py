capability_name = "Workforce"
description = "Analyzes employee headcount, status, and demographic distributions."

supported_questions = [
    "How many active employees do we have?",
    "How many employees are in Engineering?",
    "What is our total headcount?",
    "Show me employee distribution by department.",
]

required_data = {
    "facts": [],  # Current headcount derives directly from DimEmployee
    "dimensions": ["DimEmployee", "DimDepartment", "DimDesignation"],
    "events": ["hr.employee"]
}

allowed_filters = ["department", "employment_type", "status", "designation"]

analytics_api = "GET /analytics/hr/headcount"
