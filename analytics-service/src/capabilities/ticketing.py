capability_name = "Ticketing"
description = "Analyzes IT support tickets, resolution times, and ticket volumes."

supported_questions = [
    "How many IT tickets are currently open?",
    "What is the average resolution time for IT tickets?",
    "Show me the ticket volume by priority.",
    "Which category has the most tickets?",
]

required_data = {
    "facts": ["FactITTicket"],
    "dimensions": ["DimEmployee", "DimDate"],
    "events": ["it.ticket"]
}

allowed_filters = ["period", "status", "priority", "category"]

analytics_api = "GET /analytics/it/ticket-summary"
