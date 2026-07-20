from sqlalchemy import String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base, UUIDMixin, TimestampMixin


class Tenant(Base, UUIDMixin, TimestampMixin):
    """
    Core Tenant representation table.
    """
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    domain: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    subscription_tier: Mapped[str] = mapped_column(String(50), default="standard", nullable=False)

    # Relationships
    config: Mapped["TenantConfig"] = relationship(
        "TenantConfig",
        back_populates="tenant",
        uselist=False,
        cascade="all, delete-orphan"
    )
    users: Mapped[list["TenantUser"]] = relationship(
        "TenantUser",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )


class TenantConfig(Base, UUIDMixin, TimestampMixin):
    """
    Stores tenant-specific system settings, theme overrides, AI models, and feature toggles.
    """
    __tablename__ = "tenant_configs"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, unique=True)
    theme: Mapped[str] = mapped_column(String(50), default="dark", nullable=False)
    allowed_domains: Mapped[dict] = mapped_column(JSON, default=list, nullable=False) # standard serialization support
    ai_settings: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    security_policies: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="config")


class TenantUser(Base, UUIDMixin, TimestampMixin):
    """
    Represents users belonging to specific Tenants.
    """
    __tablename__ = "tenant_users"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="member", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="users")
