from shared_infrastructure.database.base import PublicBase, TenantBase

# We re-export these from shared-infrastructure so our analytics models
# can easily inherit from them.
# 
# Use TenantBase for data that belongs to a specific company (like FactAttendance).
# Use PublicBase for data that is shared globally (like DimDate).

__all__ = ["PublicBase", "TenantBase"]
