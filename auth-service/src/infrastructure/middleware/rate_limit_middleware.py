import time
from collections import defaultdict
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Store requests as { "ip_address": [timestamp1, timestamp2, ...] }
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Identify the user by IP address
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Get the request history for this IP
        history = self.requests[client_ip]
        
        # Remove old requests that are outside our time window (e.g., older than 60 seconds)
        history = [ts for ts in history if current_time - ts < self.window_seconds]
        
        # Check if they have exceeded the limit
        if len(history) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."}
            )
            
        # Add the current request to their history
        history.append(current_time)
        self.requests[client_ip] = history
        
        # Process the request normally
        return await call_next(request)
