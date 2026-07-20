from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# ==========================================
# Tenant Configuration Schemas
# ==========================================
class TenantConfigBase(BaseModel):
    theme: str = Field(default="dark", max_length=50)
    allowed_domains: List[str] = Field(default_factory=list)
    ai_settings: Dict[str, Any] = Field(default_factory=dict)
    security_policies: Dict[str, Any] = Field(default_factory=dict)


class TenantConfigCreate(TenantConfigBase):
    pass


class TenantConfigResponse(TenantConfigBase):
    id: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# Tenant Schemas
# ==========================================
class TenantBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    domain: Optional[str] = Field(None, max_length=255)
    subscription_tier: str = Field(default="standard", max_length=50)


class TenantCreate(TenantBase):
    admin_email: EmailStr
    admin_name: str
    config: Optional[TenantConfigCreate] = None


class TenantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    domain: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None
    subscription_tier: Optional[str] = Field(None, max_length=50)


class TenantResponse(TenantBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config: Optional[TenantConfigResponse] = None

    class Config:
        from_attributes = True


# ==========================================
# Tenant User Schemas
# ==========================================
class TenantUserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(default="member", max_length=50)


class TenantUserCreate(TenantUserBase):
    tenant_id: UUID


class TenantUserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class TenantUserResponse(TenantUserBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# Tenant Onboarding Schemas
# ==========================================
class TenantOnboardRequest(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=100)
    domain: Optional[str] = Field(None)
    admin_email: EmailStr
    admin_name: str
    subscription_tier: str = Field(default="standard")
    theme_preference: str = Field(default="dark")


class TenantOnboardResponse(BaseModel):
    success: bool
    message: str
    tenant_id: UUID
    admin_user_id: UUID
    api_endpoint: str
