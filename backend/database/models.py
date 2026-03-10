"""
Star Schema Database Models for Occupational Data Platform
Deterministic, enterprise-grade schema for US/Canada/EU compliance and automation scoring
"""
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey,
    create_engine, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timezone
import uuid

Base = declarative_base()


# =============================================================================
# DIMENSION TABLES (Star Schema)
# =============================================================================

class DimOccupation(Base):
    """
    Global anchor mapping occupations across international standards.
    Maps US O*NET codes with Canadian NOC 2026 and European ESCO URIs.
    """
    __tablename__ = 'dim_occupation'
    
    occupation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    standard_title = Column(String(500), nullable=False, index=True)
    
    # US: O*NET-SOC Code (e.g., "15-1252.00" for Software Developers)
    onet_code = Column(String(20), index=True)
    onet_description = Column(Text)
    
    # Canada: NOC 2026 Code with TEER (e.g., "21232" for Software Engineers)
    noc_2026_code = Column(String(10), index=True)
    noc_teer_category = Column(Integer)  # TEER 0-5
    noc_description = Column(Text)
    
    # Europe: ESCO URI (e.g., "http://data.europa.eu/esco/occupation/...")
    esco_uri = Column(String(500), index=True)
    esco_description = Column(Text)
    
    # Industry/Sector classification
    industry_sector = Column(String(200))
    
    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
    data_source_version = Column(String(50))  # e.g., "O*NET v30.2"
    
    # Relationships
    tasks = relationship("DimTask", back_populates="occupation", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_occupation_cross_region', 'onet_code', 'noc_2026_code', 'esco_uri'),
    )


class DimTask(Base):
    """
    Atomic unit of work. AI automates TASKS, not jobs.
    Pulls Detailed Work Activities (DWAs) from O*NET and cross-references with OaSIS.
    """
    __tablename__ = 'dim_task'
    
    task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    occupation_id = Column(UUID(as_uuid=True), ForeignKey('dim_occupation.occupation_id'), nullable=False, index=True)
    
    task_description = Column(Text, nullable=False)
    task_category = Column(String(100))  # e.g., "Data Processing", "Communication", "Analysis"
    
    # O*NET DWA alignment
    onet_dwa_id = Column(String(50))
    onet_element_id = Column(String(50))
    
    # Scoring attributes for automation calculation
    frequency_score = Column(Integer, CheckConstraint('frequency_score >= 1 AND frequency_score <= 5'))  # 1-5: How often performed daily
    human_interaction_level = Column(Integer, CheckConstraint('human_interaction_level >= 1 AND human_interaction_level <= 5'))  # 1-5: Physical/social interaction required
    cognitive_complexity = Column(Integer, CheckConstraint('cognitive_complexity >= 1 AND cognitive_complexity <= 5'))  # 1-5: Mental effort required
    physical_requirement = Column(Integer, CheckConstraint('physical_requirement >= 1 AND physical_requirement <= 5'))  # 1-5: Physical effort required
    
    # Task type classification (for deterministic scoring)
    is_routine = Column(Boolean, default=True)  # Routine vs Non-routine
    is_cognitive = Column(Boolean, default=True)  # Cognitive vs Manual
    is_digital_native = Column(Boolean, default=False)  # Already digital workflow
    requires_judgment = Column(Boolean, default=False)  # Requires human judgment
    requires_creativity = Column(Boolean, default=False)  # Creative/empathic tasks
    requires_physical_presence = Column(Boolean, default=False)  # On-site requirement
    
    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    source_system = Column(String(50))  # "ONET", "OASIS", "ESCO"
    
    # Relationships
    occupation = relationship("DimOccupation", back_populates="tasks")
    compliance_rules = relationship("FactComplianceMatrix", back_populates="task", cascade="all, delete-orphan")
    automation_scores = relationship("FactAutomationScore", back_populates="task", cascade="all, delete-orphan")


class DimSkill(Base):
    """
    Capability matrix for skills/competencies.
    Links to OaSIS SCT 2025 and ESCO skill taxonomies.
    """
    __tablename__ = 'dim_skill'
    
    skill_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_name = Column(String(300), nullable=False, index=True)
    skill_description = Column(Text)
    
    # Taxonomy source
    taxonomy_source = Column(String(100))  # e.g., "OaSIS SCT 2025", "ESCO", "O*NET"
    taxonomy_code = Column(String(50))
    
    # Skill classification
    skill_type = Column(String(50))  # "Hard", "Soft", "Digital", "Technical"
    skill_category = Column(String(100))  # e.g., "Programming", "Communication", "Management"
    
    # Competency metrics
    competency_level_required = Column(Integer, CheckConstraint('competency_level_required >= 1 AND competency_level_required <= 5'))  # 1-5
    importance_level = Column(Float)  # 0.0-1.0
    
    # Automation characteristics
    is_automatable = Column(Boolean, default=False)
    automation_tool_category = Column(String(100))  # e.g., "LLM", "RPA", "Computer Vision"
    
    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DimSkillTaskMapping(Base):
    """
    Junction table linking skills to tasks (many-to-many).
    """
    __tablename__ = 'dim_skill_task_mapping'
    
    mapping_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_id = Column(UUID(as_uuid=True), ForeignKey('dim_skill.skill_id'), nullable=False, index=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey('dim_task.task_id'), nullable=False, index=True)
    relevance_score = Column(Float)  # 0.0-1.0: How relevant the skill is to the task


# =============================================================================
# FACT TABLES (Proprietary Logic Engine)
# =============================================================================

class FactComplianceMatrix(Base):
    """
    Legal gatekeeper mapping tasks to regional laws.
    Enforces EU AI Act, Quebec CNESST, and other jurisdictional rules.
    """
    __tablename__ = 'fact_compliance_matrix'
    
    compliance_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('dim_task.task_id'), nullable=False, index=True)
    
    # Jurisdiction
    jurisdiction = Column(String(50), nullable=False, index=True)  # "EU", "Quebec", "USA-Federal", "Canada-Federal"
    jurisdiction_subdivision = Column(String(100))  # Province/State if applicable
    regulatory_body = Column(String(200))  # e.g., "CNESST", "AMF", "EU AI Office", "FTC"
    
    # EU AI Act Classification (2024/2026 enforcement)
    eu_ai_act_risk_level = Column(String(50))  # "Prohibited", "High-Risk", "Limited-Risk", "Minimal"
    eu_ai_act_annex = Column(String(20))  # "Annex I", "Annex III", etc.
    
    # Compliance requirements
    hitl_required = Column(Boolean, default=False)  # Human-in-the-Loop required
    human_signature_required = Column(Boolean, default=False)  # Legal signature needed
    audit_trail_required = Column(Boolean, default=False)  # Must log all AI decisions
    transparency_notice_required = Column(Boolean, default=False)  # Must disclose AI usage
    data_retention_days = Column(Integer)  # How long to retain records
    
    # Specific legal references
    legal_reference = Column(Text)  # Citation to specific law/regulation
    compliance_notes = Column(Text)  # Additional guidance
    
    # Compliance penalty factor (0.0 = fully blocked, 1.0 = no penalty)
    compliance_penalty_factor = Column(Float, default=1.0)
    
    # Metadata
    effective_date = Column(DateTime)
    expiry_date = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship
    task = relationship("DimTask", back_populates="compliance_rules")
    
    __table_args__ = (
        Index('ix_compliance_jurisdiction_task', 'jurisdiction', 'task_id'),
    )


class FactAutomationScore(Base):
    """
    Deterministic AI Index - calculates automation score using mathematical formula.
    Formula: S_task = (D * w_d + C * w_c) * P
    Where: D = digital feasibility, C = cognitive routine index, P = compliance penalty
    """
    __tablename__ = 'fact_automation_score'
    
    score_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('dim_task.task_id'), nullable=False, index=True)
    jurisdiction = Column(String(50), index=True)  # Score may vary by jurisdiction
    
    # Core metrics (0.0 - 1.0)
    digital_feasibility = Column(Float, CheckConstraint('digital_feasibility >= 0 AND digital_feasibility <= 1'))
    cognitive_routine_index = Column(Float, CheckConstraint('cognitive_routine_index >= 0 AND cognitive_routine_index <= 1'))
    
    # Additional scoring factors
    data_structure_score = Column(Float)  # 0.0-1.0: How structured is the data
    decision_tree_complexity = Column(Float)  # 0.0-1.0: Can decisions be modeled as rules
    error_tolerance = Column(Float)  # 0.0-1.0: Acceptable error rate
    
    # AI capability alignment
    llm_suitability = Column(Float)  # 0.0-1.0: Suitable for LLM automation
    rpa_suitability = Column(Float)  # 0.0-1.0: Suitable for RPA
    computer_vision_suitability = Column(Float)  # 0.0-1.0: Suitable for CV
    
    # Weights (configurable per methodology)
    weight_digital = Column(Float, default=0.5)
    weight_cognitive = Column(Float, default=0.5)
    
    # Compliance penalty (from fact_compliance_matrix)
    compliance_penalty = Column(Float, default=1.0)  # 0.0 = blocked, 1.0 = no penalty
    
    # Final calculated score (0-100)
    final_automation_score = Column(Float, CheckConstraint('final_automation_score >= 0 AND final_automation_score <= 100'))
    
    # Score interpretation
    automation_tier = Column(String(20))  # "None", "Low", "Medium", "High", "Full"
    recommended_approach = Column(String(100))  # e.g., "RPA + HITL", "Full LLM", "Manual only"
    
    # Methodology reference
    scoring_methodology = Column(String(100))  # e.g., "Frey-Osborne-2013", "OECD-2016", "Custom-2026"
    confidence_level = Column(Float)  # 0.0-1.0: Confidence in the score
    
    # Metadata
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_validated = Column(DateTime)
    
    # Relationship
    task = relationship("DimTask", back_populates="automation_scores")


class DimKnowledge(Base):
    """
    Knowledge areas required for occupations.
    Maps to O*NET Knowledge elements.
    """
    __tablename__ = 'dim_knowledge'
    
    knowledge_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_name = Column(String(300), nullable=False, index=True)
    knowledge_description = Column(Text)
    onet_element_id = Column(String(50))
    knowledge_category = Column(String(100))
    importance_level = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DimAbility(Base):
    """
    Abilities required for occupations.
    Maps to O*NET Ability elements.
    """
    __tablename__ = 'dim_ability'
    
    ability_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ability_name = Column(String(300), nullable=False, index=True)
    ability_description = Column(Text)
    onet_element_id = Column(String(50))
    ability_category = Column(String(100))  # Cognitive, Physical, Sensory, Psychomotor
    importance_level = Column(Float)
    is_automatable = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DimTool(Base):
    """
    Tools and technologies used in occupations.
    Maps to O*NET Tools & Technology elements.
    """
    __tablename__ = 'dim_tool'
    
    tool_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tool_name = Column(String(300), nullable=False, index=True)
    tool_description = Column(Text)
    tool_category = Column(String(100))  # Software, Hardware, Equipment
    onet_commodity_code = Column(String(50))
    is_digital = Column(Boolean, default=True)
    automation_enabler = Column(Boolean, default=False)  # Can this tool enable automation
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# =============================================================================
# CROSSWALK / MAPPING TABLES
# =============================================================================

class CrosswalkOccupation(Base):
    """
    Cross-reference table for occupation codes across systems.
    Enables fuzzy matching + manual curation between O*NET, NOC, ESCO.
    """
    __tablename__ = 'crosswalk_occupation'
    
    crosswalk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Source codes
    onet_code = Column(String(20), index=True)
    noc_2021_code = Column(String(10))  # Legacy
    noc_2026_code = Column(String(10), index=True)
    esco_uri = Column(String(500), index=True)
    isco_08_code = Column(String(10))  # ILO standard
    
    # Mapping quality
    match_quality = Column(String(20))  # "Exact", "Close", "Partial", "Manual"
    match_confidence = Column(Float)  # 0.0-1.0
    
    # Notes
    mapping_notes = Column(Text)
    verified_by = Column(String(100))
    verified_at = Column(DateTime)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataSourceMetadata(Base):
    """
    Tracks data sources, versions, and licensing information.
    """
    __tablename__ = 'data_source_metadata'
    
    source_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_name = Column(String(200), nullable=False)  # e.g., "O*NET", "NOC 2026", "ESCO"
    source_version = Column(String(50))  # e.g., "v30.2", "2026.1"
    source_url = Column(String(500))
    download_date = Column(DateTime)
    license_type = Column(String(100))  # e.g., "Public Domain", "CC BY 4.0", "Open Government"
    attribution_text = Column(Text)
    data_coverage = Column(String(200))  # e.g., "USA", "Canada", "EU"
    record_count = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
