from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.infrastructure.database.base import PublicBase, TenantBase


class TestPublicBase:
    def test_is_a_declarative_base(self):
        assert issubclass(PublicBase, DeclarativeBase)

    def test_can_be_subclassed_to_define_a_model(self):
        class SamplePublicModel(PublicBase):
            __tablename__ = "sample_public_model"

            id: Mapped[int] = mapped_column(Integer, primary_key=True)

        assert "sample_public_model" in PublicBase.metadata.tables


class TestTenantBase:
    def test_is_a_declarative_base(self):
        assert issubclass(TenantBase, DeclarativeBase)

    def test_can_be_subclassed_to_define_a_model(self):
        class SampleTenantModel(TenantBase):
            __tablename__ = "sample_tenant_model"

            id: Mapped[int] = mapped_column(Integer, primary_key=True)

        assert "sample_tenant_model" in TenantBase.metadata.tables


class TestBaseIsolation:
    def test_public_and_tenant_bases_are_distinct_classes(self):
        assert PublicBase is not TenantBase

    def test_public_and_tenant_bases_have_independent_metadata(self):
        assert PublicBase.metadata is not TenantBase.metadata

    def test_models_registered_on_one_base_do_not_leak_into_the_other(self):
        class OnlyOnPublicBase(PublicBase):
            __tablename__ = "only_on_public_base"

            id: Mapped[int] = mapped_column(Integer, primary_key=True)

        assert "only_on_public_base" in PublicBase.metadata.tables
        assert "only_on_public_base" not in TenantBase.metadata.tables