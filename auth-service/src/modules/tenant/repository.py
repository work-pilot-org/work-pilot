from sqlalchemy.orm import Session

from src.modules.tenant.models import Tenant, Domain


class TenantRepository:

    def create_tenant(
        self,
        db: Session,
        tenant: Tenant
    ) -> Tenant:

        db.add(tenant)
        db.flush()
        db.refresh(tenant)

        return tenant

    def create_domain(
        self,
        db: Session,
        domain: Domain
    ) -> Domain:

        db.add(domain)
        db.flush()
        db.refresh(domain)

        return domain

    def get_by_company_name(
        self,
        db: Session,
        company_name: str
    ) -> Tenant | None:

        return (
            db.query(Tenant)
            .filter(Tenant.company_name == company_name)
            .first()
        )

    def get_by_schema_name(
        self,
        db: Session,
        schema_name: str
    ) -> Tenant | None:

        return (
            db.query(Tenant)
            .filter(Tenant.schema_name == schema_name)
            .first()
        )

    def get_domain(
        self,
        db: Session,
        domain: str
    ) -> Domain | None:

        return (
            db.query(Domain)
            .filter(Domain.domain == domain)
            .first()
        )

    def get_tenant_by_id(
        self,
        db: Session,
        tenant_id: int
    ) -> Tenant | None:

        return (
            db.query(Tenant)
            .filter(Tenant.id == tenant_id)
            .first()
        )