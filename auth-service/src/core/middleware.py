from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.infrastructure.database.session import SessionLocal
from src.modules.tenant.repository import TenantRepository
from src.infrastructure.database.tenant_session import set_tenant_schema, set_public_schema

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Create a single database session for the lifetime of this request
        db = SessionLocal()
        
        # 2. Attach it to the request state so endpoints can use `request.state.db`
        request.state.db = db
        
        try:
            # 3. Read the Host header to determine the subdomain/tenant
            host = request.headers.get("host", "").split(":")[0]
            
            # 4. Resolve the Tenant based on the Domain
            tenant_repo = TenantRepository()
            domain = tenant_repo.get_domain(db, host)
            
            if domain:
                tenant = tenant_repo.get_tenant_by_id(db, domain.tenant_id)
                if tenant:
                    request.state.tenant = tenant
                    set_tenant_schema(db, tenant.schema_name)
                else:
                    set_public_schema(db)
            else:
                set_public_schema(db)
                
            # 5. Process the request (this passes control to the router/endpoint)
            response = await call_next(request)
            return response
            
        finally:
            # 6. Critical: Reset the PostgreSQL search_path before returning the connection to the pool
            set_public_schema(db)
            db.close()
