"""
Aurex Shared Database Framework - Base Model Module.

Hosts the shared Enterprise Declarative Base containing timestamp attributes,
conversions, and multi-tenant schema isolation contracts.
"""

import datetime
from typing import Any, Dict, List
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from aurex.backend.shared.database.tenant_context import TenantContext
from aurex.backend.shared.database.exceptions import TenantResolutionError


class Base(DeclarativeBase):
    """
    Unified declarative base representing the baseline metadata standard for
    every SQLAlchemy schema model within the Aurex estate.
    """
    
    # Trackers for auditing lifecycles
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=func.now(), 
        nullable=False,
        sort_order=998
    )
    
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=func.now(), 
        onupdate=func.now(), 
        nullable=False,
        sort_order=999
    )

    def to_dict(self, exclude_fields: List[str] = None) -> Dict[str, Any]:
        """
        Helper method converting a model instance recursively into a standard dictionary.
        Safe against cyclic recursion.
        """
        exclude = set(exclude_fields or [])
        res: Dict[str, Any] = {}
        
        for c in self.__table__.columns:
            if c.name in exclude:
                continue
            val = getattr(self, c.name)
            if isinstance(val, (datetime.datetime, datetime.date)):
                res[c.name] = val.isoformat()
            else:
                res[c.name] = val
                
        return res


class TenantScopedModel:
    """
    Mixin/Interface designed to be inherited alongside standard models that demands
    strict cell/row-level multi-tenant isolation guarantees.
    
    Guarantees 'tenant_id' column is active and binds automatic tenant isolation filters hook.
    """
    
    # Cell level key ensuring logical segmentation on shared relational tables
    tenant_id: Mapped[str] = mapped_column(
        String(64), 
        nullable=False, 
        index=True,
        sort_order=100
    )

    def enforce_tenant_context_bound(self) -> None:
        """
        Forces alignment of local model state with active global task boundary.
        Prevents a tenant from writing data labeled for another division.
        """
        active_tenant = TenantContext.get_tenant_id()
        if not active_tenant:
            raise TenantResolutionError(
                f"MUTATION BLOCKED: Attempting to save tenant-scoped object ({self.__class__.__name__}) "
                "without an active. TenantContext bound in the current task context."
            )
            
        if self.tenant_id and self.tenant_id != active_tenant:
             raise TenantResolutionError(
                f"MUTATION BLOCKED: Attempting to save data with custom tenant_id [{self.tenant_id}] "
                f"which violates current task's active context filter boundary [{active_tenant}]."
             )
        
        self.tenant_id = active_tenant
