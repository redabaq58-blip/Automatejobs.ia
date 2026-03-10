"""
Database Manager for PostgreSQL operations.
Handles connection, schema creation, and data seeding.
Falls back to SQLite for environments without PostgreSQL.
"""
import os
import logging
from typing import Optional
from datetime import datetime, timezone

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

from .models import (
    Base, DimOccupation, DimTask, DimSkill, DimSkillTaskMapping,
    FactComplianceMatrix, FactAutomationScore, DimKnowledge, DimAbility,
    DimTool, CrosswalkOccupation, DataSourceMetadata
)
from .seed_data import (
    DATA_SOURCES, OCCUPATIONS, TASKS, COMPLIANCE_RULES, SKILLS, CROSSWALKS
)
from .seed_data_extended import (
    EXTENDED_OCCUPATIONS, EXTENDED_TASKS, QUEBEC_COMPLIANCE_RULES,
    EU_AI_ACT_EXTENDED, EXTENDED_SKILLS, EXTENDED_CROSSWALKS,
    FREY_OSBORNE_BASELINES
)
from .scoring_engine import (
    DeterministicScoringEngine, TaskAttributes, ComplianceConstraints
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages database connections and operations for the occupational data platform.
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            database_url: PostgreSQL connection string. If None, uses SQLite fallback.
        """
        if database_url:
            self.database_url = database_url
        else:
            # Default to SQLite for development/testing
            self.database_url = os.environ.get(
                'DATABASE_URL',
                'sqlite:///./occupational_data.db'
            )
        
        # Create engine
        connect_args = {}
        if self.database_url.startswith('sqlite'):
            connect_args = {"check_same_thread": False}
        
        self.engine = create_engine(
            self.database_url,
            connect_args=connect_args,
            echo=False,  # Set True for SQL logging
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def create_tables(self) -> bool:
        """
        Create all database tables defined in models.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            return False
    
    def drop_tables(self) -> bool:
        """
        Drop all database tables. USE WITH CAUTION.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to drop tables: {e}")
            return False
    
    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()
    
    def seed_data_sources(self, session: Session) -> int:
        """Seed data source metadata."""
        count = 0
        for source_data in DATA_SOURCES:
            source = DataSourceMetadata(
                source_name=source_data["source_name"],
                source_version=source_data["source_version"],
                source_url=source_data["source_url"],
                license_type=source_data["license_type"],
                attribution_text=source_data["attribution_text"],
                data_coverage=source_data["data_coverage"],
                record_count=source_data["record_count"],
                download_date=datetime.now(timezone.utc),
            )
            session.add(source)
            count += 1
        session.commit()
        logger.info(f"Seeded {count} data sources")
        return count
    
    def seed_occupations(self, session: Session) -> dict:
        """Seed occupations and return ID mapping."""
        id_map = {}
        
        # Seed base occupations
        for occ_data in OCCUPATIONS:
            occupation = DimOccupation(
                standard_title=occ_data["standard_title"],
                onet_code=occ_data["onet_code"],
                onet_description=occ_data["onet_description"],
                noc_2026_code=occ_data["noc_2026_code"],
                noc_teer_category=occ_data["noc_teer_category"],
                noc_description=occ_data["noc_description"],
                esco_uri=occ_data["esco_uri"],
                esco_description=occ_data["esco_description"],
                industry_sector=occ_data["industry_sector"],
                data_source_version=occ_data.get("data_source_version", "O*NET v30.2"),
            )
            session.add(occupation)
            session.flush()
            id_map[occ_data["occupation_id"]] = occupation.occupation_id
        
        # Seed extended occupations
        for occ_data in EXTENDED_OCCUPATIONS:
            occupation = DimOccupation(
                standard_title=occ_data["standard_title"],
                onet_code=occ_data["onet_code"],
                onet_description=occ_data["onet_description"],
                noc_2026_code=occ_data["noc_2026_code"],
                noc_teer_category=occ_data["noc_teer_category"],
                noc_description=occ_data["noc_description"],
                esco_uri=occ_data["esco_uri"],
                esco_description=occ_data["esco_description"],
                industry_sector=occ_data["industry_sector"],
                data_source_version="O*NET v30.2 + Frey-Osborne",
            )
            session.add(occupation)
            session.flush()
            id_map[occ_data["occupation_id"]] = occupation.occupation_id
        
        session.commit()
        logger.info(f"Seeded {len(id_map)} occupations")
        return id_map
    
    def seed_tasks(self, session: Session, occupation_id_map: dict) -> dict:
        """Seed tasks and return ID mapping."""
        task_id_map = {}
        
        # Seed base tasks
        for task_data in TASKS:
            occ_uuid = occupation_id_map.get(task_data["occupation_id"])
            if not occ_uuid:
                logger.warning(f"Occupation not found for task: {task_data['task_id']}")
                continue
            
            task = DimTask(
                occupation_id=occ_uuid,
                task_description=task_data["task_description"],
                task_category=task_data["task_category"],
                onet_dwa_id=task_data.get("onet_dwa_id"),
                frequency_score=task_data["frequency_score"],
                human_interaction_level=task_data["human_interaction_level"],
                cognitive_complexity=task_data["cognitive_complexity"],
                physical_requirement=task_data["physical_requirement"],
                is_routine=task_data["is_routine"],
                is_cognitive=task_data["is_cognitive"],
                is_digital_native=task_data["is_digital_native"],
                requires_judgment=task_data["requires_judgment"],
                requires_creativity=task_data["requires_creativity"],
                requires_physical_presence=task_data["requires_physical_presence"],
                source_system=task_data.get("source_system", "ONET"),
            )
            session.add(task)
            session.flush()
            task_id_map[task_data["task_id"]] = task.task_id
        
        # Seed extended tasks
        for task_data in EXTENDED_TASKS:
            occ_uuid = occupation_id_map.get(task_data["occupation_id"])
            if not occ_uuid:
                logger.warning(f"Occupation not found for extended task: {task_data['task_id']}")
                continue
            
            task = DimTask(
                occupation_id=occ_uuid,
                task_description=task_data["task_description"],
                task_category=task_data["task_category"],
                frequency_score=task_data["frequency_score"],
                human_interaction_level=task_data["human_interaction_level"],
                cognitive_complexity=task_data["cognitive_complexity"],
                physical_requirement=task_data["physical_requirement"],
                is_routine=task_data["is_routine"],
                is_cognitive=task_data["is_cognitive"],
                is_digital_native=task_data["is_digital_native"],
                requires_judgment=task_data["requires_judgment"],
                requires_creativity=task_data["requires_creativity"],
                requires_physical_presence=task_data["requires_physical_presence"],
                source_system="ONET-Extended",
            )
            session.add(task)
            session.flush()
            task_id_map[task_data["task_id"]] = task.task_id
        
        session.commit()
        logger.info(f"Seeded {len(task_id_map)} tasks")
        return task_id_map
    
    def seed_compliance_rules(self, session: Session, task_id_map: dict) -> int:
        """Seed compliance rules."""
        count = 0
        
        # Seed base compliance rules
        for rule_data in COMPLIANCE_RULES:
            task_uuid = task_id_map.get(rule_data["task_id"])
            if not task_uuid:
                logger.warning(f"Task not found for compliance rule: {rule_data['task_id']}")
                continue
            
            rule = FactComplianceMatrix(
                task_id=task_uuid,
                jurisdiction=rule_data["jurisdiction"],
                regulatory_body=rule_data["regulatory_body"],
                eu_ai_act_risk_level=rule_data.get("eu_ai_act_risk_level"),
                eu_ai_act_annex=rule_data.get("eu_ai_act_annex"),
                hitl_required=rule_data["hitl_required"],
                human_signature_required=rule_data["human_signature_required"],
                audit_trail_required=rule_data["audit_trail_required"],
                transparency_notice_required=rule_data["transparency_notice_required"],
                compliance_penalty_factor=rule_data["compliance_penalty_factor"],
                legal_reference=rule_data["legal_reference"],
            )
            session.add(rule)
            count += 1
        
        # Seed Quebec-specific compliance rules
        for rule_data in QUEBEC_COMPLIANCE_RULES:
            task_uuid = task_id_map.get(rule_data["task_id"])
            if not task_uuid:
                logger.warning(f"Task not found for Quebec rule: {rule_data['task_id']}")
                continue
            
            rule = FactComplianceMatrix(
                task_id=task_uuid,
                jurisdiction=rule_data["jurisdiction"],
                regulatory_body=rule_data["regulatory_body"],
                eu_ai_act_risk_level=rule_data.get("eu_ai_act_risk_level"),
                eu_ai_act_annex=rule_data.get("eu_ai_act_annex"),
                hitl_required=rule_data["hitl_required"],
                human_signature_required=rule_data["human_signature_required"],
                audit_trail_required=rule_data["audit_trail_required"],
                transparency_notice_required=rule_data["transparency_notice_required"],
                compliance_penalty_factor=rule_data["compliance_penalty_factor"],
                legal_reference=rule_data["legal_reference"],
            )
            session.add(rule)
            count += 1
        
        # Seed EU AI Act extended rules
        for rule_data in EU_AI_ACT_EXTENDED:
            task_uuid = task_id_map.get(rule_data["task_id"])
            if not task_uuid:
                logger.warning(f"Task not found for EU rule: {rule_data['task_id']}")
                continue
            
            rule = FactComplianceMatrix(
                task_id=task_uuid,
                jurisdiction=rule_data["jurisdiction"],
                regulatory_body=rule_data["regulatory_body"],
                eu_ai_act_risk_level=rule_data.get("eu_ai_act_risk_level"),
                eu_ai_act_annex=rule_data.get("eu_ai_act_annex"),
                hitl_required=rule_data["hitl_required"],
                human_signature_required=rule_data["human_signature_required"],
                audit_trail_required=rule_data["audit_trail_required"],
                transparency_notice_required=rule_data["transparency_notice_required"],
                compliance_penalty_factor=rule_data["compliance_penalty_factor"],
                legal_reference=rule_data["legal_reference"],
            )
            session.add(rule)
            count += 1
        
        session.commit()
        logger.info(f"Seeded {count} compliance rules")
        return count
    
    def seed_skills(self, session: Session) -> int:
        """Seed skills."""
        count = 0
        
        # Seed base skills
        for skill_data in SKILLS:
            skill = DimSkill(
                skill_name=skill_data["skill_name"],
                skill_description=skill_data["skill_description"],
                taxonomy_source=skill_data["taxonomy_source"],
                skill_type=skill_data["skill_type"],
                skill_category=skill_data["skill_category"],
                competency_level_required=skill_data["competency_level_required"],
                importance_level=skill_data["importance_level"],
                is_automatable=skill_data["is_automatable"],
                automation_tool_category=skill_data.get("automation_tool_category"),
            )
            session.add(skill)
            count += 1
        
        # Seed extended skills
        for skill_data in EXTENDED_SKILLS:
            skill = DimSkill(
                skill_name=skill_data["skill_name"],
                skill_description=skill_data["skill_description"],
                taxonomy_source=skill_data["taxonomy_source"],
                skill_type=skill_data["skill_type"],
                skill_category=skill_data["skill_category"],
                competency_level_required=skill_data["competency_level_required"],
                importance_level=skill_data["importance_level"],
                is_automatable=skill_data["is_automatable"],
                automation_tool_category=skill_data.get("automation_tool_category"),
            )
            session.add(skill)
            count += 1
        
        session.commit()
        logger.info(f"Seeded {count} skills")
        return count
    
    def seed_crosswalks(self, session: Session) -> int:
        """Seed crosswalk mappings."""
        count = 0
        
        # Seed base crosswalks
        for cw_data in CROSSWALKS:
            crosswalk = CrosswalkOccupation(
                onet_code=cw_data["onet_code"],
                noc_2021_code=cw_data["noc_2021_code"],
                noc_2026_code=cw_data["noc_2026_code"],
                esco_uri=cw_data["esco_uri"],
                isco_08_code=cw_data["isco_08_code"],
                match_quality=cw_data["match_quality"],
                match_confidence=cw_data["match_confidence"],
                mapping_notes=cw_data["mapping_notes"],
            )
            session.add(crosswalk)
            count += 1
        
        # Seed extended crosswalks
        for cw_data in EXTENDED_CROSSWALKS:
            crosswalk = CrosswalkOccupation(
                onet_code=cw_data["onet_code"],
                noc_2021_code=cw_data["noc_2021_code"],
                noc_2026_code=cw_data["noc_2026_code"],
                esco_uri=cw_data["esco_uri"],
                isco_08_code=cw_data["isco_08_code"],
                match_quality=cw_data["match_quality"],
                match_confidence=cw_data["match_confidence"],
                mapping_notes=cw_data["mapping_notes"],
            )
            session.add(crosswalk)
            count += 1
        
        session.commit()
        logger.info(f"Seeded {count} crosswalk mappings")
        return count
    
    def calculate_automation_scores(self, session: Session, task_id_map: dict) -> int:
        """
        Calculate and store automation scores for all tasks.
        Uses the deterministic scoring engine with Frey-Osborne baselines.
        """
        count = 0
        
        # Combine all task data
        all_tasks = TASKS + EXTENDED_TASKS
        task_data_lookup = {t["task_id"]: t for t in all_tasks}
        
        # Combine all compliance rules
        all_compliance = COMPLIANCE_RULES + QUEBEC_COMPLIANCE_RULES + EU_AI_ACT_EXTENDED
        compliance_lookup = {}
        for rule in all_compliance:
            key = rule["task_id"]
            if key not in compliance_lookup:
                compliance_lookup[key] = []
            compliance_lookup[key].append(rule)
        
        for task_key, task_uuid in task_id_map.items():
            task_data = task_data_lookup.get(task_key)
            if not task_data:
                continue
            
            # Build task attributes
            attrs = TaskAttributes(
                frequency_score=task_data["frequency_score"],
                human_interaction_level=task_data["human_interaction_level"],
                cognitive_complexity=task_data["cognitive_complexity"],
                physical_requirement=task_data["physical_requirement"],
                is_routine=task_data["is_routine"],
                is_cognitive=task_data["is_cognitive"],
                is_digital_native=task_data["is_digital_native"],
                requires_judgment=task_data["requires_judgment"],
                requires_creativity=task_data["requires_creativity"],
                requires_physical_presence=task_data["requires_physical_presence"],
            )
            
            # Score for each jurisdiction with compliance rules
            jurisdictions = ["USA-Federal", "Canada-Federal", "EU", "Quebec"]
            compliance_rules = compliance_lookup.get(task_key, [])
            
            for jurisdiction in jurisdictions:
                # Find matching compliance rule
                matching_rule = next(
                    (r for r in compliance_rules if r["jurisdiction"] == jurisdiction),
                    None
                )
                
                if matching_rule:
                    constraints = ComplianceConstraints(
                        hitl_required=matching_rule["hitl_required"],
                        human_signature_required=matching_rule["human_signature_required"],
                        eu_ai_act_risk_level=matching_rule.get("eu_ai_act_risk_level"),
                        jurisdiction=jurisdiction,
                    )
                else:
                    constraints = ComplianceConstraints(jurisdiction=jurisdiction)
                
                # Calculate score
                result = DeterministicScoringEngine.score_task(attrs, constraints)
                
                # Store score
                score = FactAutomationScore(
                    task_id=task_uuid,
                    jurisdiction=jurisdiction,
                    digital_feasibility=result.digital_feasibility,
                    cognitive_routine_index=result.cognitive_routine_index,
                    llm_suitability=result.llm_suitability,
                    rpa_suitability=result.rpa_suitability,
                    compliance_penalty=result.compliance_penalty,
                    final_automation_score=result.final_score,
                    automation_tier=result.tier.value,
                    recommended_approach=result.recommended_approach.value,
                    scoring_methodology="Deterministic-v1.0 + Frey-Osborne",
                    confidence_level=result.confidence,
                )
                session.add(score)
                count += 1
        
        session.commit()
        logger.info(f"Calculated {count} automation scores")
        return count
    
    def seed_all(self) -> dict:
        """
        Seed all data into the database.
        
        Returns:
            Dictionary with counts of seeded records.
        """
        session = self.get_session()
        try:
            results = {
                "data_sources": self.seed_data_sources(session),
                "skills": self.seed_skills(session),
                "crosswalks": self.seed_crosswalks(session),
            }
            
            occupation_id_map = self.seed_occupations(session)
            results["occupations"] = len(occupation_id_map)
            
            task_id_map = self.seed_tasks(session, occupation_id_map)
            results["tasks"] = len(task_id_map)
            
            results["compliance_rules"] = self.seed_compliance_rules(session, task_id_map)
            results["automation_scores"] = self.calculate_automation_scores(session, task_id_map)
            
            return results
        finally:
            session.close()
    
    def get_table_counts(self) -> dict:
        """Get record counts for all tables."""
        session = self.get_session()
        try:
            return {
                "occupations": session.query(DimOccupation).count(),
                "tasks": session.query(DimTask).count(),
                "skills": session.query(DimSkill).count(),
                "compliance_rules": session.query(FactComplianceMatrix).count(),
                "automation_scores": session.query(FactAutomationScore).count(),
                "crosswalks": session.query(CrosswalkOccupation).count(),
                "data_sources": session.query(DataSourceMetadata).count(),
            }
        finally:
            session.close()
    
    def initialize_database(self, force_reseed: bool = False) -> dict:
        """
        Initialize database: create tables and seed data.
        
        Args:
            force_reseed: If True, drops and recreates all tables.
        
        Returns:
            Dictionary with initialization results.
        """
        if force_reseed:
            self.drop_tables()
        
        self.create_tables()
        
        # Check if data exists
        counts = self.get_table_counts()
        if counts.get("occupations", 0) > 0 and not force_reseed:
            logger.info("Database already seeded, skipping...")
            return {"status": "existing", "counts": counts}
        
        # Seed data
        seed_results = self.seed_all()
        return {"status": "seeded", "counts": seed_results}


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Get or create the global database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def init_db(force_reseed: bool = False) -> dict:
    """Initialize the database."""
    manager = get_db_manager()
    return manager.initialize_database(force_reseed)
