from typing import List, Optional, Sequence, Dict, Any
from sqlalchemy.future import select
from sqlalchemy import func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.base import BaseRepository
from models.report import ESGReport, Scorecard, AuditLog, ReportExport, ReportFramework
from middleware.tenant import get_current_tenant

class ReportRepository(BaseRepository[ESGReport]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(ESGReport, db_session)

    async def get_by_framework_and_year(self, framework: ReportFramework, year: int) -> Optional[ESGReport]:
        tenant_id = get_current_tenant()
        query = select(ESGReport).filter_by(
            tenant_id=tenant_id,
            framework=framework,
            reporting_year=year
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


class ScorecardRepository(BaseRepository[Scorecard]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Scorecard, db_session)

    async def get_scorecards_by_year(self, year: int) -> Sequence[Scorecard]:
        tenant_id = get_current_tenant()
        query = select(Scorecard).filter_by(
            tenant_id=tenant_id,
            assessment_year=year
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_aggregates_by_category(self, year: int) -> Dict[str, Any]:
        tenant_id = get_current_tenant()
        query = (
            select(
                Scorecard.category,
                func.avg(Scorecard.compliance_pct).label("avg_compliance"),
                func.count(Scorecard.id).label("metric_count")
            )
            .filter_by(tenant_id=tenant_id, assessment_year=year)
            .group_by(Scorecard.category)
        )
        result = await self.db.execute(query)
        
        aggregates = {}
        for row in result.all():
            aggregates[row.category] = {
                "average_compliance": round(float(row.avg_compliance or 0.0), 2),
                "metric_count": int(row.metric_count or 0)
            }
        return aggregates


class AuditLogRepository(BaseRepository[AuditLog]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(AuditLog, db_session)

    async def get_audit_trail(self, entity_type: Optional[str] = None, skip: int = 0, limit: int = 100) -> Sequence[AuditLog]:
        tenant_id = get_current_tenant()
        query = select(AuditLog).filter_by(tenant_id=tenant_id)
        if entity_type:
            query = query.filter_by(entity_type=entity_type)
            
        query = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def log_event(self, action: str, entity_type: str, entity_id: str, operator: str, details: str = "") -> AuditLog:
        payload = {
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "changed_by": operator,
            "details": details
        }
        return await self.create(payload, created_by=operator)


class ExportRepository(BaseRepository[ReportExport]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(ReportExport, db_session)

    async def get_by_report_id(self, report_id: str) -> Sequence[ReportExport]:
        tenant_id = get_current_tenant()
        query = select(ReportExport).filter_by(
            tenant_id=tenant_id,
            report_id=report_id
        )
        result = await self.db.execute(query)
        return result.scalars().all()
