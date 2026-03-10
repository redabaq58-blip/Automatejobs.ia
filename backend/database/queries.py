"""
Query functions for the occupational data platform.
Provides deterministic, hallucination-free data retrieval.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc

from .models import (
    DimOccupation, DimTask, DimSkill, FactComplianceMatrix,
    FactAutomationScore, CrosswalkOccupation, DataSourceMetadata
)
from .db_manager import get_db_manager


def get_occupation_by_code(
    code: str,
    code_type: str = "onet"
) -> Optional[Dict[str, Any]]:
    """
    Get occupation by O*NET, NOC, or ESCO code.
    
    Args:
        code: The occupation code
        code_type: "onet", "noc", or "esco"
    
    Returns:
        Occupation data or None
    """
    manager = get_db_manager()
    session = manager.get_session()
    try:
        query = session.query(DimOccupation)
        
        if code_type == "onet":
            occupation = query.filter(DimOccupation.onet_code == code).first()
        elif code_type == "noc":
            occupation = query.filter(DimOccupation.noc_2026_code == code).first()
        elif code_type == "esco":
            occupation = query.filter(DimOccupation.esco_uri.contains(code)).first()
        else:
            return None
        
        if not occupation:
            return None
        
        return {
            "occupation_id": str(occupation.occupation_id),
            "standard_title": occupation.standard_title,
            "onet_code": occupation.onet_code,
            "noc_2026_code": occupation.noc_2026_code,
            "esco_uri": occupation.esco_uri,
            "industry_sector": occupation.industry_sector,
            "onet_description": occupation.onet_description,
            "noc_description": occupation.noc_description,
            "esco_description": occupation.esco_description,
        }
    finally:
        session.close()


def get_tasks_for_occupation(
    occupation_id: str,
    min_automation_score: Optional[float] = None,
    jurisdiction: str = "USA-Federal"
) -> List[Dict[str, Any]]:
    """
    Get all tasks for an occupation with their automation scores.
    
    Args:
        occupation_id: UUID of the occupation
        min_automation_score: Filter tasks with score >= this value
        jurisdiction: Jurisdiction for compliance scoring
    
    Returns:
        List of tasks with scores
    """
    manager = get_db_manager()
    session = manager.get_session()
    try:
        query = session.query(DimTask).filter(
            DimTask.occupation_id == occupation_id
        )
        
        tasks = query.all()
        result = []
        
        for task in tasks:
            # Get automation score for this jurisdiction
            score = session.query(FactAutomationScore).filter(
                and_(
                    FactAutomationScore.task_id == task.task_id,
                    FactAutomationScore.jurisdiction == jurisdiction
                )
            ).first()
            
            # Get compliance rules
            compliance = session.query(FactComplianceMatrix).filter(
                and_(
                    FactComplianceMatrix.task_id == task.task_id,
                    FactComplianceMatrix.jurisdiction == jurisdiction
                )
            ).first()
            
            task_data = {
                "task_id": str(task.task_id),
                "task_description": task.task_description,
                "task_category": task.task_category,
                "frequency_score": task.frequency_score,
                "human_interaction_level": task.human_interaction_level,
                "cognitive_complexity": task.cognitive_complexity,
                "is_routine": task.is_routine,
                "is_digital_native": task.is_digital_native,
                "requires_judgment": task.requires_judgment,
                "requires_physical_presence": task.requires_physical_presence,
            }
            
            if score:
                task_data["automation_score"] = {
                    "final_score": score.final_automation_score,
                    "tier": score.automation_tier,
                    "recommended_approach": score.recommended_approach,
                    "digital_feasibility": score.digital_feasibility,
                    "cognitive_routine_index": score.cognitive_routine_index,
                    "llm_suitability": score.llm_suitability,
                    "rpa_suitability": score.rpa_suitability,
                    "compliance_penalty": score.compliance_penalty,
                }
            
            if compliance:
                task_data["compliance"] = {
                    "eu_ai_act_risk_level": compliance.eu_ai_act_risk_level,
                    "hitl_required": compliance.hitl_required,
                    "human_signature_required": compliance.human_signature_required,
                    "audit_trail_required": compliance.audit_trail_required,
                    "legal_reference": compliance.legal_reference,
                }
            
            # Apply filter
            if min_automation_score is not None:
                if score and score.final_automation_score >= min_automation_score:
                    result.append(task_data)
            else:
                result.append(task_data)
        
        return result
    finally:
        session.close()


def get_high_automation_tasks(
    min_score: float = 80.0,
    jurisdiction: str = "USA-Federal",
    limit: int = 50
) -> List[Dict[str, Any]]:
    """
    Get tasks with high automation potential.
    Perfect for finding quick automation wins.
    
    Args:
        min_score: Minimum automation score (0-100)
        jurisdiction: Filter by jurisdiction
        limit: Maximum results to return
    
    Returns:
        List of highly automatable tasks
    """
    manager = get_db_manager()
    session = manager.get_session()
    try:
        scores = session.query(FactAutomationScore).filter(
            and_(
                FactAutomationScore.final_automation_score >= min_score,
                FactAutomationScore.jurisdiction == jurisdiction
            )
        ).order_by(
            desc(FactAutomationScore.final_automation_score)
        ).limit(limit).all()
        
        result = []
        for score in scores:
            task = session.query(DimTask).filter(
                DimTask.task_id == score.task_id
            ).first()
            
            occupation = session.query(DimOccupation).filter(
                DimOccupation.occupation_id == task.occupation_id
            ).first()
            
            result.append({
                "task_description": task.task_description,
                "occupation_title": occupation.standard_title,
                "industry_sector": occupation.industry_sector,
                "automation_score": score.final_automation_score,
                "automation_tier": score.automation_tier,
                "recommended_approach": score.recommended_approach,
                "llm_suitability": score.llm_suitability,
                "rpa_suitability": score.rpa_suitability,
            })
        
        return result
    finally:
        session.close()


def get_compliance_blocked_tasks(
    jurisdiction: str = "EU"
) -> List[Dict[str, Any]]:
    """
    Get tasks that are blocked or restricted due to compliance rules.
    Critical for avoiding legal issues when building AI agents.
    
    Args:
        jurisdiction: Filter by jurisdiction (EU has strictest rules)
    
    Returns:
        List of blocked/restricted tasks with reasons
    """
    manager = get_db_manager()
    session = manager.get_session()
    try:
        # Get tasks with HITL required or blocked
        compliance_rules = session.query(FactComplianceMatrix).filter(
            and_(
                FactComplianceMatrix.jurisdiction == jurisdiction,
                or_(
                    FactComplianceMatrix.hitl_required.is_(True),
                    FactComplianceMatrix.human_signature_required.is_(True),
                    FactComplianceMatrix.eu_ai_act_risk_level == "High-Risk",
                    FactComplianceMatrix.eu_ai_act_risk_level == "Prohibited"
                )
            )
        ).all()
        
        result = []
        for rule in compliance_rules:
            task = session.query(DimTask).filter(
                DimTask.task_id == rule.task_id
            ).first()
            
            occupation = session.query(DimOccupation).filter(
                DimOccupation.occupation_id == task.occupation_id
            ).first()
            
            restrictions = []
            if rule.human_signature_required:
                restrictions.append("BLOCKED: Human signature required")
            if rule.eu_ai_act_risk_level == "Prohibited":
                restrictions.append("BLOCKED: EU AI Act Prohibited")
            if rule.eu_ai_act_risk_level == "High-Risk":
                restrictions.append("RESTRICTED: EU AI Act High-Risk")
            if rule.hitl_required:
                restrictions.append("RESTRICTED: Human-in-the-loop required")
            
            result.append({
                "task_description": task.task_description,
                "occupation_title": occupation.standard_title,
                "jurisdiction": rule.jurisdiction,
                "eu_ai_act_risk_level": rule.eu_ai_act_risk_level,
                "restrictions": restrictions,
                "compliance_penalty_factor": rule.compliance_penalty_factor,
                "legal_reference": rule.legal_reference,
                "regulatory_body": rule.regulatory_body,
            })
        
        return result
    finally:
        session.close()


def search_occupations(
    query: str,
    industry_filter: Optional[str] = None,
    region: Optional[str] = None,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """
    Search occupations by title or description.
    
    Args:
        query: Search query
        industry_filter: Filter by industry sector
        region: Filter to show only codes for specific region
        limit: Maximum results
    
    Returns:
        List of matching occupations
    """
    manager = get_db_manager()
    session = manager.get_session()
    try:
        q = session.query(DimOccupation).filter(
            or_(
                DimOccupation.standard_title.ilike(f"%{query}%"),
                DimOccupation.onet_description.ilike(f"%{query}%"),
                DimOccupation.noc_description.ilike(f"%{query}%"),
            )
        )
        
        if industry_filter:
            q = q.filter(DimOccupation.industry_sector == industry_filter)
        
        occupations = q.limit(limit).all()
        
        result = []
        for occ in occupations:
            data = {
                "occupation_id": str(occ.occupation_id),
                "standard_title": occ.standard_title,
                "industry_sector": occ.industry_sector,
            }
            
            if region == "USA" or region is None:
                data["onet_code"] = occ.onet_code
            if region == "Canada" or region is None:
                data["noc_2026_code"] = occ.noc_2026_code
            if region == "EU" or region is None:
                data["esco_uri"] = occ.esco_uri
            
            result.append(data)
        
        return result
    finally:
        session.close()


def get_crosswalk(
    code: str,
    source_system: str = "onet"
) -> Optional[Dict[str, Any]]:
    """
    Get cross-reference mapping for an occupation code.
    Translate between O*NET, NOC, and ESCO.
    
    Args:
        code: Source occupation code
        source_system: "onet", "noc", or "esco"
    
    Returns:
        Crosswalk mapping with all equivalent codes
    """
    manager = get_db_manager()
    session = manager.get_session()
    try:
        q = session.query(CrosswalkOccupation)
        
        if source_system == "onet":
            crosswalk = q.filter(CrosswalkOccupation.onet_code == code).first()
        elif source_system == "noc":
            crosswalk = q.filter(CrosswalkOccupation.noc_2026_code == code).first()
        elif source_system == "esco":
            crosswalk = q.filter(CrosswalkOccupation.esco_uri.contains(code)).first()
        else:
            return None
        
        if not crosswalk:
            return None
        
        return {
            "onet_code": crosswalk.onet_code,
            "noc_2021_code": crosswalk.noc_2021_code,
            "noc_2026_code": crosswalk.noc_2026_code,
            "esco_uri": crosswalk.esco_uri,
            "isco_08_code": crosswalk.isco_08_code,
            "match_quality": crosswalk.match_quality,
            "match_confidence": crosswalk.match_confidence,
            "mapping_notes": crosswalk.mapping_notes,
        }
    finally:
        session.close()


def get_data_source_info() -> List[Dict[str, Any]]:
    """
    Get information about all data sources.
    Important for attribution and compliance.
    
    Returns:
        List of data source metadata
    """
    manager = get_db_manager()
    session = manager.get_session()
    try:
        sources = session.query(DataSourceMetadata).all()
        return [
            {
                "source_name": s.source_name,
                "source_version": s.source_version,
                "source_url": s.source_url,
                "license_type": s.license_type,
                "attribution_text": s.attribution_text,
                "data_coverage": s.data_coverage,
                "record_count": s.record_count,
            }
            for s in sources
        ]
    finally:
        session.close()


def get_occupation_automation_summary(
    occupation_id: str,
    jurisdiction: str = "USA-Federal"
) -> Dict[str, Any]:
    """
    Get aggregated automation summary for an occupation.
    Shows overall automation potential across all tasks.
    
    Args:
        occupation_id: UUID of the occupation
        jurisdiction: Jurisdiction for compliance scoring
    
    Returns:
        Aggregated automation statistics
    """
    manager = get_db_manager()
    session = manager.get_session()
    try:
        occupation = session.query(DimOccupation).filter(
            DimOccupation.occupation_id == occupation_id
        ).first()
        
        if not occupation:
            return {"error": "Occupation not found"}
        
        tasks = session.query(DimTask).filter(
            DimTask.occupation_id == occupation_id
        ).all()
        
        scores = []
        blocked_count = 0
        hitl_required_count = 0
        
        for task in tasks:
            score = session.query(FactAutomationScore).filter(
                and_(
                    FactAutomationScore.task_id == task.task_id,
                    FactAutomationScore.jurisdiction == jurisdiction
                )
            ).first()
            
            if score:
                scores.append(score.final_automation_score)
                if score.compliance_penalty == 0:
                    blocked_count += 1
                elif score.compliance_penalty < 1:
                    hitl_required_count += 1
        
        if not scores:
            return {
                "occupation_title": occupation.standard_title,
                "total_tasks": len(tasks),
                "error": "No automation scores calculated"
            }
        
        avg_score = sum(scores) / len(scores)
        
        # Categorize tasks by tier
        tier_counts = {
            "None": len([s for s in scores if s <= 10]),
            "Low": len([s for s in scores if 10 < s <= 30]),
            "Medium": len([s for s in scores if 30 < s <= 60]),
            "High": len([s for s in scores if 60 < s <= 85]),
            "Full": len([s for s in scores if s > 85]),
        }
        
        return {
            "occupation_title": occupation.standard_title,
            "onet_code": occupation.onet_code,
            "noc_2026_code": occupation.noc_2026_code,
            "industry_sector": occupation.industry_sector,
            "jurisdiction": jurisdiction,
            "total_tasks": len(tasks),
            "average_automation_score": round(avg_score, 1),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "blocked_tasks": blocked_count,
            "hitl_required_tasks": hitl_required_count,
            "fully_automatable_tasks": tier_counts["Full"],
            "tier_distribution": tier_counts,
        }
    finally:
        session.close()


def get_industry_automation_summary(industry_sector: str = None) -> List[Dict[str, Any]]:
    """
    Get automation summary grouped by industry.
    
    Args:
        industry_sector: Optional filter by specific industry
    
    Returns:
        List of industries with automation statistics
    """
    manager = get_db_manager()
    session = manager.get_session()
    try:
        query = session.query(DimOccupation)
        if industry_sector:
            query = query.filter(DimOccupation.industry_sector == industry_sector)
        
        occupations = query.all()
        
        # Group by industry
        industry_data = {}
        for occ in occupations:
            industry = occ.industry_sector or "Other"
            if industry not in industry_data:
                industry_data[industry] = {
                    "industry": industry,
                    "occupations": [],
                    "total_tasks": 0,
                    "all_scores": [],
                }
            
            tasks = session.query(DimTask).filter(
                DimTask.occupation_id == occ.occupation_id
            ).all()
            
            for task in tasks:
                score = session.query(FactAutomationScore).filter(
                    and_(
                        FactAutomationScore.task_id == task.task_id,
                        FactAutomationScore.jurisdiction == "USA-Federal"
                    )
                ).first()
                if score:
                    industry_data[industry]["all_scores"].append(score.final_automation_score)
            
            industry_data[industry]["occupations"].append(occ.standard_title)
            industry_data[industry]["total_tasks"] += len(tasks)
        
        # Calculate summaries
        result = []
        for industry, data in industry_data.items():
            scores = data["all_scores"]
            if scores:
                result.append({
                    "industry": industry,
                    "occupation_count": len(data["occupations"]),
                    "task_count": data["total_tasks"],
                    "average_automation_score": round(sum(scores) / len(scores), 1),
                    "highest_score": max(scores),
                    "lowest_score": min(scores),
                    "high_automation_tasks": len([s for s in scores if s > 80]),
                    "blocked_or_restricted_tasks": len([s for s in scores if s < 30]),
                })
        
        # Sort by average score descending
        result.sort(key=lambda x: x["average_automation_score"], reverse=True)
        return result
    finally:
        session.close()


def get_frey_osborne_comparison(onet_code: str = None) -> List[Dict[str, Any]]:
    """
    Get Frey-Osborne automation probability comparison with our scores.
    
    Args:
        onet_code: Optional filter by specific O*NET code
    
    Returns:
        List of occupations with F-O probability vs our score
    """
    from .seed_data_extended import FREY_OSBORNE_BASELINES
    
    manager = get_db_manager()
    session = manager.get_session()
    try:
        query = session.query(DimOccupation)
        if onet_code:
            query = query.filter(DimOccupation.onet_code == onet_code)
        
        occupations = query.all()
        result = []
        
        for occ in occupations:
            fo_prob = FREY_OSBORNE_BASELINES.get(occ.onet_code)
            if fo_prob is None:
                continue
            
            # Get average task score for this occupation
            tasks = session.query(DimTask).filter(
                DimTask.occupation_id == occ.occupation_id
            ).all()
            
            scores = []
            for task in tasks:
                score = session.query(FactAutomationScore).filter(
                    and_(
                        FactAutomationScore.task_id == task.task_id,
                        FactAutomationScore.jurisdiction == "USA-Federal"
                    )
                ).first()
                if score:
                    scores.append(score.final_automation_score)
            
            if scores:
                avg_score = sum(scores) / len(scores)
                result.append({
                    "occupation_title": occ.standard_title,
                    "onet_code": occ.onet_code,
                    "industry_sector": occ.industry_sector,
                    "frey_osborne_probability": fo_prob,
                    "frey_osborne_percentage": round(fo_prob * 100, 1),
                    "our_automation_score": round(avg_score, 1),
                    "score_difference": round(avg_score - (fo_prob * 100), 1),
                    "task_count": len(scores),
                })
        
        # Sort by F-O probability descending
        result.sort(key=lambda x: x["frey_osborne_probability"], reverse=True)
        return result
    finally:
        session.close()


def get_quebec_compliance_summary() -> List[Dict[str, Any]]:
    """
    Get Quebec-specific compliance summary.
    Critical for applications targeting Quebec market.
    
    Returns:
        List of Quebec compliance rules with affected tasks
    """
    manager = get_db_manager()
    session = manager.get_session()
    try:
        rules = session.query(FactComplianceMatrix).filter(
            FactComplianceMatrix.jurisdiction == "Quebec"
        ).all()
        
        result = []
        for rule in rules:
            task = session.query(DimTask).filter(
                DimTask.task_id == rule.task_id
            ).first()
            
            occupation = session.query(DimOccupation).filter(
                DimOccupation.occupation_id == task.occupation_id
            ).first()
            
            # Determine restriction level
            if rule.compliance_penalty_factor == 0:
                restriction_level = "BLOCKED"
            elif rule.compliance_penalty_factor < 0.5:
                restriction_level = "SEVERELY_RESTRICTED"
            elif rule.compliance_penalty_factor < 1.0:
                restriction_level = "RESTRICTED"
            else:
                restriction_level = "PERMITTED"
            
            result.append({
                "task_description": task.task_description,
                "occupation_title": occupation.standard_title,
                "regulatory_body": rule.regulatory_body,
                "restriction_level": restriction_level,
                "hitl_required": rule.hitl_required,
                "human_signature_required": rule.human_signature_required,
                "audit_trail_required": rule.audit_trail_required,
                "compliance_penalty_factor": rule.compliance_penalty_factor,
                "legal_reference": rule.legal_reference,
            })
        
        return result
    finally:
        session.close()
