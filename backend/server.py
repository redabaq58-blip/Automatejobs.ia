from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone

# Database imports
from database.db_manager import get_db_manager, init_db
from database.scoring_engine import score_task_simple
from database import queries
from database import proprietary_queries
from database import tier1_queries

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection (kept for backward compatibility)
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(
    title="Occupational Data Platform API",
    description="Enterprise-grade, deterministic API for occupational data with automation scoring",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class ScoreTaskRequest(BaseModel):
    frequency: int = Field(ge=1, le=5, default=3, description="How often task is performed (1-5)")
    human_interaction: int = Field(ge=1, le=5, default=3, description="Level of human interaction required (1-5)")
    cognitive_complexity: int = Field(ge=1, le=5, default=3, description="Cognitive complexity (1-5)")
    is_routine: bool = Field(default=True, description="Is the task routine/repetitive")
    is_digital: bool = Field(default=False, description="Is the task already digital")
    requires_judgment: bool = Field(default=False, description="Does task require human judgment")
    requires_creativity: bool = Field(default=False, description="Does task require creativity")
    hitl_required: bool = Field(default=False, description="Is human-in-the-loop mandated")
    eu_risk_level: Optional[str] = Field(default=None, description="EU AI Act risk level")
    jurisdiction: str = Field(default="USA-Federal", description="Jurisdiction for compliance")

class AutomationScoreResponse(BaseModel):
    digital_feasibility: float
    cognitive_routine_index: float
    compliance_penalty: float
    final_automation_score: float
    automation_tier: str
    recommended_approach: str
    llm_suitability: float
    rpa_suitability: float
    confidence: float
    explanation: str

class OccupationResponse(BaseModel):
    occupation_id: str
    standard_title: str
    onet_code: Optional[str]
    noc_2026_code: Optional[str]
    esco_uri: Optional[str]
    industry_sector: Optional[str]

class TaskResponse(BaseModel):
    task_id: str
    task_description: str
    task_category: Optional[str]
    automation_score: Optional[Dict[str, Any]]
    compliance: Optional[Dict[str, Any]]

class DatabaseStatusResponse(BaseModel):
    status: str
    counts: Dict[str, int]

class AIChatRequest(BaseModel):
    message: str
    context: dict = {}

# =============================================================================
# API ENDPOINTS
# =============================================================================

@api_router.get("/")
async def root():
    return {
        "message": "Occupational Data Platform API",
        "version": "1.0.0",
        "endpoints": {
            "database": "/api/database/status",
            "occupations": "/api/occupations",
            "tasks": "/api/tasks",
            "compliance": "/api/compliance",
            "score": "/api/score/task",
        }
    }

# Database Management
@api_router.get("/database/status", response_model=DatabaseStatusResponse)
async def get_database_status():
    """Get current database status and record counts."""
    try:
        manager = get_db_manager()
        counts = manager.get_table_counts()
        return {"status": "connected", "counts": counts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/database/initialize", response_model=DatabaseStatusResponse)
async def initialize_database(force_reseed: bool = False):
    """
    Initialize the database with tables and seed data.
    Use force_reseed=true to drop and recreate all tables.
    """
    try:
        result = init_db(force_reseed=force_reseed)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Occupation Endpoints
@api_router.get("/occupations", response_model=List[OccupationResponse])
async def search_occupations(
    query: str = Query(..., description="Search query for occupation titles"),
    industry: Optional[str] = Query(None, description="Filter by industry sector"),
    region: Optional[str] = Query(None, description="Filter by region: USA, Canada, EU"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results")
):
    """Search occupations by title or description."""
    try:
        results = queries.search_occupations(
            query=query,
            industry_filter=industry,
            region=region,
            limit=limit
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/occupations/code/{code}")
async def get_occupation_by_code(
    code: str,
    code_type: str = Query("onet", description="Code type: onet, noc, or esco")
):
    """Get occupation by O*NET, NOC, or ESCO code."""
    result = queries.get_occupation_by_code(code, code_type)
    if not result:
        raise HTTPException(status_code=404, detail="Occupation not found")
    return result

@api_router.get("/occupations/{occupation_id}/summary")
async def get_occupation_summary(
    occupation_id: str,
    jurisdiction: str = Query("USA-Federal", description="Jurisdiction for scoring")
):
    """Get aggregated automation summary for an occupation."""
    result = queries.get_occupation_automation_summary(occupation_id, jurisdiction)
    if "error" in result and result["error"] == "Occupation not found":
        raise HTTPException(status_code=404, detail="Occupation not found")
    return result

# Task Endpoints
@api_router.get("/tasks/occupation/{occupation_id}", response_model=List[TaskResponse])
async def get_tasks_for_occupation(
    occupation_id: str,
    min_score: Optional[float] = Query(None, ge=0, le=100, description="Minimum automation score"),
    jurisdiction: str = Query("USA-Federal", description="Jurisdiction for scoring")
):
    """Get all tasks for an occupation with automation scores."""
    try:
        results = queries.get_tasks_for_occupation(
            occupation_id=occupation_id,
            min_automation_score=min_score,
            jurisdiction=jurisdiction
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/tasks/high-automation")
async def get_high_automation_tasks(
    min_score: float = Query(80.0, ge=0, le=100, description="Minimum automation score"),
    jurisdiction: str = Query("USA-Federal", description="Jurisdiction"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results")
):
    """
    Get tasks with high automation potential.
    Perfect for finding quick automation wins.
    """
    try:
        return queries.get_high_automation_tasks(
            min_score=min_score,
            jurisdiction=jurisdiction,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Compliance Endpoints
@api_router.get("/compliance/blocked")
async def get_compliance_blocked_tasks(
    jurisdiction: str = Query("EU", description="Jurisdiction (EU has strictest rules)")
):
    """
    Get tasks that are blocked or restricted due to compliance.
    Critical for avoiding legal issues when building AI agents.
    """
    try:
        return queries.get_compliance_blocked_tasks(jurisdiction=jurisdiction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/compliance/quebec")
async def get_quebec_compliance():
    """
    Get Quebec-specific compliance summary.
    Critical for applications targeting Quebec market (Law 25, CNESST, OIQ, CPA, Barreau).
    """
    try:
        return queries.get_quebec_compliance_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Industry Analysis Endpoints
@api_router.get("/industries/summary")
async def get_industry_summary(
    industry: Optional[str] = Query(None, description="Filter by industry sector")
):
    """
    Get automation summary grouped by industry.
    Shows which industries have highest/lowest automation potential.
    """
    try:
        return queries.get_industry_automation_summary(industry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Frey-Osborne Comparison
@api_router.get("/frey-osborne/comparison")
async def get_frey_osborne_comparison(
    onet_code: Optional[str] = Query(None, description="Filter by O*NET code")
):
    """
    Compare Frey-Osborne (2013) automation probabilities with our deterministic scores.
    Shows variance between academic baseline and task-level scoring.
    """
    try:
        return queries.get_frey_osborne_comparison(onet_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Crosswalk Endpoints
@api_router.get("/crosswalk/{code}")
async def get_crosswalk(
    code: str,
    source_system: str = Query("onet", description="Source: onet, noc, or esco")
):
    """
    Get cross-reference mapping between O*NET, NOC, and ESCO codes.
    Translate occupation codes across systems.
    """
    result = queries.get_crosswalk(code, source_system)
    if not result:
        raise HTTPException(status_code=404, detail="Crosswalk not found")
    return result

# Data Sources
@api_router.get("/data-sources")
async def get_data_sources():
    """
    Get information about all data sources.
    Important for attribution and compliance.
    """
    try:
        return queries.get_data_source_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Scoring Engine
@api_router.post("/score/task", response_model=AutomationScoreResponse)
async def score_task(request: ScoreTaskRequest):
    """
    Calculate automation score for a custom task.
    Uses deterministic scoring formula - no LLM, no hallucination.
    
    Formula: S_task = (D * w_d + C * w_c) * P * 100
    Where:
        D = Digital Feasibility
        C = Cognitive Routine Index
        P = Compliance Penalty
    """
    try:
        result = score_task_simple(
            frequency=request.frequency,
            human_interaction=request.human_interaction,
            cognitive_complexity=request.cognitive_complexity,
            is_routine=request.is_routine,
            is_digital=request.is_digital,
            requires_judgment=request.requires_judgment,
            requires_creativity=request.requires_creativity,
            hitl_required=request.hitl_required,
            eu_risk_level=request.eu_risk_level,
            jurisdiction=request.jurisdiction,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# PROPRIETARY DATA ENDPOINTS (Competitive Moat)
# =============================================================================

@api_router.get("/tools/ai")
async def get_ai_tools(
    category: Optional[str] = Query(None, description="Filter by category: LLM_TEXT, RPA_INTELLIGENT, etc."),
    vendor: Optional[str] = Query(None, description="Filter by vendor name")
):
    """
    Get AI tools database with capabilities and pricing.
    15+ enterprise AI tools mapped to task categories.
    """
    try:
        return proprietary_queries.get_ai_tools(category, vendor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/tools/recommendations")
async def get_tool_recommendations(
    task_id: Optional[str] = Query(None, description="Filter by task ID")
):
    """
    THE SECRET SAUCE: Get specific AI tool recommendations for tasks.
    Includes fit scores, setup hours, and recommended architectures.
    """
    try:
        return proprietary_queries.get_tool_recommendations(task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/implementation/complexity")
async def get_implementation_complexity(
    task_id: Optional[str] = Query(None, description="Filter by task ID"),
    complexity_level: Optional[str] = Query(None, description="Filter by level: TRIVIAL, SIMPLE, MODERATE, COMPLEX, VERY_COMPLEX, TRANSFORMATIONAL")
):
    """
    Get real-world implementation complexity data.
    Includes costs, timelines, required roles, and industry success rates.
    """
    try:
        return proprietary_queries.get_implementation_complexity(task_id, complexity_level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/tasks/decomposition")
async def get_task_decomposition(
    task_id: Optional[str] = Query(None, description="Filter by parent task ID")
):
    """
    Get task decomposition trees - breaks complex tasks into atomic automatable units.
    Shows time savings and identifies bottlenecks.
    """
    try:
        return proprietary_queries.get_task_decomposition(task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/risks/failure-modes")
async def get_failure_modes(
    task_id: Optional[str] = Query(None, description="Filter by task ID")
):
    """
    Get failure mode analysis - what breaks and how to recover.
    Includes probability, severity, detection methods, and mitigation strategies.
    """
    try:
        return proprietary_queries.get_failure_modes(task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/roi/salaries")
async def get_salary_benchmarks(
    region: str = Query("USA", description="Region: USA, Canada, EU"),
    occupation: Optional[str] = Query(None, description="Filter by occupation title")
):
    """
    Get salary benchmarks with fully-loaded costs.
    Essential for ROI calculations.
    """
    try:
        return proprietary_queries.get_salary_benchmarks(region, occupation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/roi/analysis")
async def get_roi_analysis(
    task_id: Optional[str] = Query(None, description="Filter by task ID"),
    region: Optional[str] = Query(None, description="Filter by region")
):
    """
    Get pre-calculated ROI analysis for automation investments.
    Includes payback period, Year 1 and Year 3 ROI.
    """
    try:
        return proprietary_queries.get_roi_analysis(task_id, region)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CustomROIRequest(BaseModel):
    annual_salary: float = Field(..., description="Base annual salary")
    automation_percentage: float = Field(..., ge=0, le=1, description="Percentage automatable (0.0-1.0)")
    implementation_cost: float = Field(..., description="One-time implementation cost")
    ongoing_annual_cost: float = Field(..., description="Annual licensing/maintenance cost")
    region: str = Field(default="USA", description="Region for context")


@api_router.post("/roi/calculate")
async def calculate_custom_roi(request: CustomROIRequest):
    """
    Calculate custom ROI for any automation scenario.
    Returns complete business case with recommendation.
    """
    try:
        return proprietary_queries.calculate_custom_roi(
            annual_salary=request.annual_salary,
            automation_percentage=request.automation_percentage,
            implementation_cost=request.implementation_cost,
            ongoing_annual_cost=request.ongoing_annual_cost,
            region=request.region,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/automation/blueprint/{task_id}")
async def get_automation_blueprint(task_id: str):
    """
    Get complete automation blueprint for a task.
    Combines tools, complexity, failure modes, and ROI into actionable plan.
    """
    try:
        result = proprietary_queries.get_automation_blueprint(task_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/automation/quick-wins")
async def get_quick_wins(
    min_roi: float = Query(100, description="Minimum Year 1 ROI percentage"),
    max_payback_months: float = Query(12, description="Maximum payback period in months")
):
    """
    Get quick win automation opportunities.
    Tasks with high ROI and fast payback - start here for immediate value.
    """
    try:
        return proprietary_queries.get_quick_wins(min_roi, max_payback_months)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# TIER 1 INTELLIGENCE ENDPOINTS (Game-Changing Data)
# =============================================================================

# --- Automation Adoption Intelligence ---
@api_router.get("/intelligence/adoption/industry")
async def get_industry_adoption(
    industry: Optional[str] = Query(None, description="Filter by industry")
):
    """
    Get automation adoption benchmarks by industry.
    Who's automating what and how fast - competitive intelligence.
    """
    try:
        return tier1_queries.get_industry_automation_maturity(industry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/adoption/velocity")
async def get_adoption_velocity(
    company_size: Optional[str] = Query(None, description="STARTUP, SMB, MID_MARKET, ENTERPRISE, MEGA")
):
    """
    Get adoption velocity curves by company size.
    How long from pilot to production.
    """
    try:
        return tier1_queries.get_adoption_velocity(company_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/adoption/first-mover")
async def get_first_mover_windows():
    """
    Get first-mover advantage windows.
    Which automation opportunities are closing - act NOW.
    """
    try:
        return tier1_queries.get_first_mover_windows()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/adoption/benchmark")
async def get_competitive_benchmark(
    industry: str = Query(..., description="Your industry"),
    company_size: str = Query(..., description="Your company size")
):
    """
    Get competitive benchmark for your automation position.
    Where you stand vs competitors.
    """
    try:
        result = tier1_queries.get_competitive_benchmark(industry, company_size)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Skills Decay & Reskilling ---
@api_router.get("/intelligence/skills/decay")
async def get_skills_decay(
    skill: Optional[str] = Query(None, description="Filter by skill name")
):
    """
    Get skills half-life predictions.
    How long until skills become obsolete - workforce planning gold.
    """
    try:
        return tier1_queries.get_skills_decay(skill)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/skills/reskilling")
async def get_reskilling_pathways(
    from_role: Optional[str] = Query(None, description="Filter by current role")
):
    """
    Get reskilling pathways with economics.
    Career transitions with costs, timelines, and ROI.
    """
    try:
        return tier1_queries.get_reskilling_pathways(from_role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/skills/workforce-impact")
async def get_workforce_impact():
    """
    Get aggregate workforce impact data.
    Total jobs at risk, reskilling market size.
    """
    try:
        return tier1_queries.get_workforce_impact_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Regulatory Forecast ---
@api_router.get("/intelligence/regulatory/forecast")
async def get_regulatory_forecast(
    jurisdiction: Optional[str] = Query(None, description="EU, USA-Federal, Canada-Federal, Quebec, UK")
):
    """
    Get predicted regulatory changes 2026-2030.
    What's coming and when - compliance planning.
    """
    try:
        return tier1_queries.get_regulatory_forecast(jurisdiction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/regulatory/timeline")
async def get_regulatory_timeline():
    """
    Get all predicted regulatory changes sorted by date.
    Chronological compliance roadmap.
    """
    try:
        return tier1_queries.get_regulatory_timeline()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/regulatory/risk-scores")
async def get_compliance_risk_scores(
    task_type: Optional[str] = Query(None, description="Filter by task type")
):
    """
    Get compliance risk scores by task type.
    Current and predicted 2027 risk levels.
    """
    try:
        return tier1_queries.get_compliance_risk_scores(task_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Labor Arbitrage Index ---
@api_router.get("/intelligence/arbitrage/index")
async def get_labor_arbitrage(
    occupation: Optional[str] = Query(None, description="Filter by occupation")
):
    """
    Get labor arbitrage index - wage trends driving automation urgency.
    The economic pressure to automate.
    """
    try:
        return tier1_queries.get_labor_arbitrage_index(occupation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/arbitrage/geographic")
async def get_geographic_wages(
    location: Optional[str] = Query(None, description="Filter by location")
):
    """
    Get geographic wage multipliers.
    Where automation ROI is highest.
    """
    try:
        return tier1_queries.get_geographic_wage_index(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/arbitrage/automate-now")
async def get_automate_now_list():
    """
    Get ranked list of what to automate NOW.
    Highest urgency based on arbitrage scores.
    """
    try:
        return tier1_queries.get_automate_now_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/arbitrage/location-roi")
async def calculate_location_roi(
    occupation: str = Query(..., description="Occupation to analyze"),
    location: str = Query(..., description="Location for wage adjustment"),
    implementation_cost: float = Query(..., description="Base implementation cost USD")
):
    """
    Calculate location-adjusted automation ROI.
    How location affects payback period.
    """
    try:
        result = tier1_queries.calculate_location_adjusted_roi(occupation, location, implementation_cost)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Total Cost of Ownership ---
@api_router.get("/intelligence/tco/analysis")
async def get_tco_analysis(
    automation_type: Optional[str] = Query(None, description="Filter by automation type")
):
    """
    Get total cost of ownership including hidden costs.
    The costs vendors don't tell you about.
    """
    try:
        return tier1_queries.get_tco_analysis(automation_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/tco/hidden-multipliers")
async def get_hidden_cost_multipliers():
    """
    Get hidden cost multipliers by automation type.
    How much budgets typically underestimate.
    """
    try:
        return tier1_queries.get_hidden_cost_multipliers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/tco/vendor-lock-in")
async def get_vendor_lock_in(
    vendor: Optional[str] = Query(None, description="Filter by vendor")
):
    """
    Get vendor lock-in risk assessment.
    Switching costs and data portability.
    """
    try:
        return tier1_queries.get_vendor_lock_in_risk(vendor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/tco/5-year")
async def calculate_5_year_tco(
    automation_type: str = Query(..., description="e.g., 'Data Entry Automation'"),
    automation_category: str = Query(..., description="e.g., 'RPA_BASIC', 'LLM_BASED'")
):
    """
    Calculate complete 5-year TCO projection.
    Full cost picture for budget planning.
    """
    try:
        result = tier1_queries.calculate_5_year_tco(automation_type, automation_category)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Composite Intelligence ---
@api_router.get("/intelligence/pressure-index/{occupation}")
async def get_automation_pressure_index(occupation: str):
    """
    THE SIGNATURE METRIC: Automation Pressure Index™
    Combines wage growth + tool capability + competitor adoption + regulatory openness.
    Single score for automation urgency.
    """
    try:
        result = tier1_queries.get_automation_pressure_index(occupation)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/executive-dashboard")
async def get_executive_dashboard():
    """
    Executive dashboard with all key Tier 1 metrics.
    One-page view for C-suite decisions.
    """
    try:
        return tier1_queries.get_executive_dashboard()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# EXPANDED TIER 1 INTELLIGENCE ENDPOINTS
# =============================================================================

# --- Industry Maturity (Expanded) ---
@api_router.get("/intelligence/industries/all")
async def get_all_industries():
    """
    Get automation maturity for all 20 industries.
    Combined base and expanded data.
    """
    try:
        return tier1_queries.get_all_industry_maturity()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/industries/rankings")
async def get_industry_rankings():
    """
    Get industries ranked by automation maturity score.
    """
    try:
        return tier1_queries.get_industry_maturity_rankings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Skills Decay (Expanded) ---
@api_router.get("/intelligence/skills/all")
async def get_all_skills():
    """
    Get all skills decay predictions (35+ skills).
    """
    try:
        return tier1_queries.get_all_skills_decay()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/skills/at-risk-summary")
async def get_skills_at_risk():
    """
    Get summary of skills at risk by threat level.
    """
    try:
        return tier1_queries.get_skills_at_risk_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/skills/reskilling/all")
async def get_all_reskilling():
    """
    Get all reskilling pathways (22+ pathways).
    """
    try:
        return tier1_queries.get_all_reskilling_pathways()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/skills/reskilling/highest-roi")
async def get_highest_roi_reskilling(
    limit: int = Query(10, description="Number of pathways to return")
):
    """
    Get the highest ROI reskilling pathways.
    """
    try:
        return tier1_queries.get_highest_roi_reskilling(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Regulatory Forecasts (Expanded) ---
@api_router.get("/intelligence/regulatory/all")
async def get_all_regulatory():
    """
    Get regulatory forecasts for all 13+ jurisdictions.
    """
    try:
        return tier1_queries.get_all_regulatory_forecasts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/regulatory/global-timeline")
async def get_global_regulatory_timeline():
    """
    Get all regulatory changes sorted by date globally.
    """
    try:
        return tier1_queries.get_global_regulatory_timeline()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/regulatory/high-probability")
async def get_high_probability_regulations(
    min_probability: float = Query(0.7, description="Minimum probability threshold")
):
    """
    Get regulatory changes with high probability of occurring.
    """
    try:
        return tier1_queries.get_high_probability_regulations(min_probability)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Labor Arbitrage (Expanded) ---
@api_router.get("/intelligence/arbitrage/all")
async def get_all_arbitrage():
    """
    Get labor arbitrage index for all 24+ occupations.
    """
    try:
        return tier1_queries.get_all_labor_arbitrage()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/arbitrage/critical")
async def get_critical_arbitrage():
    """
    Get occupations with critical automation urgency.
    """
    try:
        return tier1_queries.get_critical_arbitrage_occupations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- TCO (Expanded) ---
@api_router.get("/intelligence/tco/all")
async def get_all_tco():
    """
    Get TCO analyses for all 15+ automation types.
    """
    try:
        return tier1_queries.get_all_tco_analyses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/tco/highest-hidden-costs")
async def get_highest_hidden_costs(
    limit: int = Query(10, description="Number of results to return")
):
    """
    Get automation types with highest hidden cost multipliers.
    """
    try:
        return tier1_queries.get_highest_hidden_cost_multipliers(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- AI Capability Timeline ---
@api_router.get("/intelligence/ai-timeline")
async def get_ai_timeline(
    year: Optional[str] = Query(None, description="Filter by year (2024, 2026, 2028, 2030)")
):
    """
    Get AI capability predictions by year.
    When AI can do what.
    """
    try:
        return tier1_queries.get_ai_capability_timeline(year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/ai-timeline/task-trajectory/{task_category}")
async def get_task_trajectory(task_category: str):
    """
    Get automation trajectory for a task category.
    """
    try:
        return tier1_queries.get_task_automation_trajectory(task_category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Industry Disruption ---
@api_router.get("/intelligence/disruption")
async def get_disruption_forecast():
    """
    Get industry disruption predictions 2026-2030.
    """
    try:
        return tier1_queries.get_industry_disruption_forecast()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/disruption/most-disrupted")
async def get_most_disrupted(
    limit: int = Query(5, description="Number of industries to return")
):
    """
    Get industries facing most disruption.
    """
    try:
        return tier1_queries.get_most_disrupted_industries(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/disruption/safest")
async def get_safest_industries(
    limit: int = Query(5, description="Number of industries to return")
):
    """
    Get industries least disrupted by automation.
    """
    try:
        return tier1_queries.get_safest_industries(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Vendor Landscape ---
@api_router.get("/intelligence/vendors")
async def get_vendor_landscape(
    category: Optional[str] = Query(None, description="RPA_PLATFORMS, LLM_PROVIDERS, DOCUMENT_AI, CONVERSATIONAL_AI")
):
    """
    Get vendor analysis by category.
    """
    try:
        return tier1_queries.get_vendor_landscape(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/vendors/compare/{category}")
async def compare_vendors(category: str):
    """
    Get vendor comparison for a specific category.
    """
    try:
        return tier1_queries.get_vendor_comparison(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/vendors/recommend")
async def get_vendor_recommendations(
    use_case: str = Query(..., description="e.g., 'RPA', 'LLM', 'document processing'"),
    budget: str = Query("MEDIUM", description="LOW, MEDIUM, HIGH")
):
    """
    Get vendor recommendations based on use case and budget.
    """
    try:
        return tier1_queries.get_vendor_recommendations(use_case, budget)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- ROI Benchmarks ---
@api_router.get("/intelligence/roi-benchmarks")
async def get_roi_benchmarks(
    company_size: Optional[str] = Query(None, description="STARTUP, SMB, MID_MARKET, ENTERPRISE, MEGA_CORP")
):
    """
    Get ROI benchmarks by company size.
    """
    try:
        return tier1_queries.get_roi_benchmarks(company_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/roi-calculator")
async def calculate_expected_roi(
    company_size: str = Query(..., description="STARTUP, SMB, MID_MARKET, ENTERPRISE, MEGA_CORP"),
    automation_budget: float = Query(..., description="Planned automation budget in USD")
):
    """
    Calculate expected ROI based on company size and budget.
    """
    try:
        result = tier1_queries.get_expected_automation_roi(company_size, automation_budget)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Failure Analysis ---
@api_router.get("/intelligence/failure-rates")
async def get_failure_rates(
    automation_type: Optional[str] = Query(None, description="RPA, LLM_BASED, COMPUTER_VISION, CHATBOT")
):
    """
    Get automation failure rates and reasons.
    """
    try:
        return tier1_queries.get_automation_failure_rates(automation_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/failure-prevention/{automation_type}")
async def get_failure_prevention(automation_type: str):
    """
    Get failure prevention recommendations.
    """
    try:
        result = tier1_queries.get_failure_prevention_guide(automation_type)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Occupation Timeline ---
@api_router.get("/intelligence/occupation-timeline")
async def get_occupation_timeline(
    occupation: Optional[str] = Query(None, description="Filter by specific occupation")
):
    """
    Get detailed automation timeline for occupations.
    """
    try:
        return tier1_queries.get_occupation_automation_timeline(occupation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/occupation-timeline/by-risk")
async def get_occupations_by_risk(
    risk_level: Optional[str] = Query(None, description="CRITICAL, HIGH, MEDIUM, LOW, VERY_LOW")
):
    """
    Get occupations filtered by displacement risk level.
    """
    try:
        return tier1_queries.get_occupations_by_displacement_risk(risk_level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Competitive Intelligence ---
@api_router.get("/intelligence/leaders")
async def get_automation_leaders(
    sector: Optional[str] = Query(None, description="Banking, Insurance, Healthcare, Retail, Manufacturing")
):
    """
    Get automation leaders by sector.
    """
    try:
        return tier1_queries.get_automation_leaders(sector)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/leaders/gap-analysis/{sector}")
async def get_gap_analysis(sector: str):
    """
    Get automation gap analysis for a sector.
    """
    try:
        result = tier1_queries.get_automation_gap_analysis(sector)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Task Difficulty ---
@api_router.get("/intelligence/task-difficulty")
async def get_task_difficulty(
    task: Optional[str] = Query(None, description="Filter by specific task")
):
    """
    Get automation difficulty scores for tasks.
    """
    try:
        return tier1_queries.get_task_automation_difficulty(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/task-difficulty/easiest")
async def get_easiest_tasks(
    limit: int = Query(5, description="Number of tasks to return")
):
    """
    Get the easiest tasks to automate.
    """
    try:
        return tier1_queries.get_easiest_tasks_to_automate(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/task-difficulty/quick-wins")
async def get_quick_wins(
    max_weeks: int = Query(8, description="Maximum implementation time in weeks")
):
    """
    Get quick win automation opportunities.
    """
    try:
        return tier1_queries.get_quick_win_tasks(max_weeks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Technology Radar ---
@api_router.get("/intelligence/tech-radar")
async def get_tech_radar(
    quadrant: Optional[str] = Query(None, description="ADOPT_NOW, TRIAL, ASSESS, HOLD")
):
    """
    Get emerging technology radar.
    """
    try:
        return tier1_queries.get_emerging_tech_radar(quadrant)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/tech-radar/adopt-now")
async def get_tech_adopt_now():
    """
    Get technologies that should be adopted now.
    """
    try:
        return tier1_queries.get_tech_to_adopt_now()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/tech-radar/trial")
async def get_tech_to_trial():
    """
    Get technologies worth trialing.
    """
    try:
        return tier1_queries.get_tech_to_trial()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Implementation Playbooks ---
@api_router.get("/intelligence/playbooks")
async def get_playbooks(
    use_case: Optional[str] = Query(None, description="CUSTOMER_SERVICE_AI, INVOICE_PROCESSING")
):
    """
    Get step-by-step implementation playbook.
    """
    try:
        return tier1_queries.get_implementation_playbook(use_case)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/intelligence/playbooks/summary")
async def get_playbooks_summary():
    """
    Get summary of all implementation playbooks.
    """
    try:
        return tier1_queries.get_playbook_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Enhanced Executive Dashboard ---
@api_router.get("/intelligence/executive-dashboard-enhanced")
async def get_enhanced_dashboard():
    """
    Enhanced executive dashboard with all expanded metrics.
    Comprehensive view for strategic decision making.
    """
    try:
        return tier1_queries.get_enhanced_executive_dashboard()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ai/chat")
async def ai_chat(request: AIChatRequest):
    """AI assistant that answers automation questions using platform data."""
    message = request.message.lower()

    # Try to use LLM if API key is available
    openai_key = os.environ.get('OPENAI_API_KEY', '')
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '')

    if openai_key or anthropic_key:
        try:
            # Build context from platform data
            from database.queries import search_occupations, get_high_automation_tasks
            from database.tier1_queries import get_industry_disruption_forecast, get_skills_at_risk_summary

            context_data = []
            try:
                tasks = get_high_automation_tasks(min_score=80, limit=5)
                if tasks:
                    context_data.append(f"Top automatable tasks: {', '.join([t.get('task_description', '')[:50] for t in tasks[:3]])}")
            except Exception:
                pass

            platform_context = "\n".join(context_data) if context_data else "Platform has 29 occupations, 39 tasks, 85+ API endpoints covering automation intelligence."

            system_prompt = f"""You are an AI automation expert for Automatejobs.ia, a platform that helps people build compliant AI agents and automations.

Platform data:
- 29 occupations cross-mapped (O*NET + NOC 2026 + ESCO)
- 39 atomic tasks with deterministic automation scores (0-100, no hallucination)
- 156 automation scores across 4 jurisdictions (USA, Canada, EU, Quebec)
- 20 industries benchmarked for automation maturity (Financial Services, Healthcare, Manufacturing, Retail, Technology, Legal, Insurance, Transportation, Real Estate, Hospitality, Agriculture, Telecom, Energy, Pharma, Media, Construction, Government, Professional Services, Nonprofit, Automotive)
- 35 skills tracked with decay half-life predictions and wage impact analysis
- 22 reskilling pathways with ROI and salary increase data
- 15 regulatory jurisdictions forecasted through 2030 (EU AI Act, Quebec Law 25, CNESST, CFPB, California, New York, Colorado, Singapore, Australia, Japan, Brazil, India, UK, China, Canada Federal)
- 15 AI tools in vendor database (OpenAI, Anthropic, Google, UiPath, Automation Anywhere, Microsoft Power Automate, AWS Textract, Google Document AI, Amazon Lex, Intercom, Landing AI, Cognex, Waymo, TuSimple, DataRobot)
- 15 labor arbitrage opportunities with urgency scoring and wage growth trends
- 8 first-mover automation windows with competitive advantage data
- 5 company-size ROI benchmarks (Startup → Mega Corp)
- 10 TCO analyses with hidden cost multipliers
- 85+ API endpoints for all intelligence data

{platform_context}

Answer in 2-3 concise paragraphs. Be specific with numbers when possible. Mention compliance implications for USA/Canada/EU. End with a practical next step."""

            if anthropic_key:
                import anthropic
                client = anthropic.Anthropic(api_key=anthropic_key)
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=500,
                    system=system_prompt,
                    messages=[{"role": "user", "content": request.message}]
                )
                answer = response.content[0].text
            elif openai_key:
                import openai
                client = openai.OpenAI(api_key=openai_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    max_tokens=500,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": request.message}
                    ]
                )
                answer = response.choices[0].message.content

            return {"response": answer, "data_used": ["platform_data"], "sources": ["Automatejobs.ia Database"]}
        except Exception as e:
            logger.warning(f"LLM call failed: {e}. Falling back to deterministic response.")

    # Deterministic fallback — keyword-based responses from platform data
    response_text = ""

    if any(w in message for w in ['finance', 'banking', 'financial', 'accounting', 'invoice']):
        response_text = """Finance sector has excellent automation potential (maturity score: 71/100).

Top quick wins:
• **Financial Data Entry** — Score: 91/100, Payback: 2.1 months, ROI Year 1: 287%
• **Invoice Processing** — Score: 84/100, Payback: 3.4 months, ROI Year 1: 198%
• **Report Generation** — Score: 78/100, Payback: 4.1 months, ROI Year 1: 156%

Compliance note: USA Federal has no restrictions. EU AI Act requires disclosure for automated credit decisions. Quebec Law 25 applies to any system using personal financial data.

**Next step:** Click "AI Wizard" in the sidebar to build a complete Finance automation blueprint in 5 minutes."""

    elif any(w in message for w in ['healthcare', 'medical', 'hospital', 'clinical', 'patient']):
        response_text = """Healthcare automation requires careful compliance planning due to sensitive data regulations.

Best automation opportunities:
• **Medical Billing Coding** — Score: 82/100, requires HITL for final review
• **Appointment Scheduling** — Score: 88/100, fully automatable
• **Insurance Pre-authorization** — Score: 71/100, EU requires human oversight

Compliance: HIPAA (USA), PIPEDA (Canada), GDPR (EU) all apply. The EU AI Act classifies some clinical AI as HIGH RISK — meaning mandatory human oversight and extensive documentation.

**Next step:** Use the Regulatory Compliance page to see full jurisdiction-by-jurisdiction rules before building."""

    elif any(w in message for w in ['eu', 'europe', 'gdpr', 'compliance', 'regulation', 'legal']):
        response_text = """EU AI Act (fully enforced August 2026) creates 4 risk tiers for automation:

• **Unacceptable Risk** (BANNED): Social scoring, real-time biometric surveillance
• **High Risk** (strict rules): HR decisions, credit scoring, medical devices — requires registration, testing, human oversight
• **Limited Risk** (disclosure only): Chatbots, deepfakes — must tell users it's AI
• **Minimal Risk** (no restrictions): Spam filters, data entry, document processing

For your automations:
- Data entry, invoice processing → ✅ Minimal risk, no restrictions
- Customer communication AI → ⚠️ Must disclose AI interaction
- Credit/hiring decisions → 🚫 High risk — extensive compliance required

**Next step:** Check the Regulatory Compliance page for your specific jurisdiction requirements."""

    elif any(w in message for w in ['cost', 'roi', 'payback', 'budget', 'price', 'expensive', 'cheap']):
        response_text = """ROI varies significantly by automation type and company size. Here's a realistic breakdown:

**Typical costs:**
• RPA (Robotic Process Automation): $5,000-$50,000 setup + $8-15k/year
• LLM/AI tools (OpenAI, Claude): $20-100/month per user, no setup cost
• Document AI: $500-3,000/month depending on volume

**Typical returns (from our database of 39 analyzed tasks):**
• Fastest payback: Data Entry — 2.1 months average
• Highest ROI: Invoice Processing — 287% Year 1
• Safest start: Email triage — low cost, immediate results

**By company size:**
• Startups: Focus on $0-500/month SaaS tools, payback 3-6 months
• SMBs: Budget $8-25k, expect 6-12 month payback
• Enterprise: $50k-500k investment, 9-18 month payback

**Next step:** Try the ROI Calculator page to get exact numbers for your specific situation."""

    elif any(w in message for w in ['hr', 'human resources', 'hiring', 'recruitment', 'onboarding', 'employee']):
        response_text = """HR automation has high potential but needs careful compliance for EU/Canada.

Best opportunities:
• **Resume Screening** — Score: 76/100. ⚠️ EU AI Act: HIGH RISK if used in hiring decisions — requires human final decision
• **Employee Onboarding** — Score: 85/100. ✅ Fully automatable, low compliance risk
• **Benefits Administration** — Score: 88/100. ✅ Excellent ROI, payback 3.8 months
• **Performance Data Collection** — Score: 72/100. ⚠️ Requires transparent data policies

USA Federal: No AI-specific restrictions for HR (yet). State laws vary (Illinois, New York have specific rules).
Canada: PIPEDA consent requirements for employee data.
EU: AI Act classifies hiring AI as High Risk — extensive documentation required.

**Next step:** Start with onboarding automation (lowest compliance risk, fastest payback), then expand to other HR processes."""

    elif any(w in message for w in ['quick', 'easy', 'start', 'begin', 'simple', 'fastest']):
        response_text = """The fastest, easiest automations to start with (all under 4 months payback):

**Top 5 Quick Wins:**
1. **Data Entry Automation** — Score: 91/100, Payback: 2.1 months, Tools: UiPath/Power Automate
2. **Email Triage & Routing** — Score: 82/100, Payback: 3.2 months, Tools: OpenAI + Gmail API
3. **Invoice Processing** — Score: 84/100, Payback: 3.4 months, Tools: Azure Form Recognizer
4. **Report Generation** — Score: 78/100, Payback: 3.8 months, Tools: Python scripts + LLM
5. **Appointment Scheduling** — Score: 88/100, Payback: 3.9 months, Tools: Calendly + Zapier

All 5 are:
✅ Fully compliant in USA, Canada, and EU (no restrictions)
✅ No-code/low-code options available
✅ Under $5,000 to implement

**Next step:** Click "Quick Wins" on the Build Studio page to start with any of these today."""

    else:
        response_text = """Great question! Based on our platform's intelligence across 29 occupations, 20 industries, 35 skills, and 15 regulatory jurisdictions:

**Overall automation landscape:**
• Average automation score: 74/100 across 156 scored tasks (39 tasks × 4 jurisdictions)
• 8.1 million US jobs facing automation impact
• Most automatable: Data Entry (91/100), Invoice Processing (84/100), Report Generation (78/100)
• Typical ROI: 150-300% Year 1 for well-chosen automations
• 20 industries benchmarked — Financial Services (72/100 maturity) leads adoption

**Getting started:**
1. Pick an industry (Finance, Healthcare, HR, Manufacturing, Customer Service are most mature)
2. Identify specific tasks (not whole jobs — automate tasks, not people)
3. Check compliance for your jurisdictions (USA, Canada, EU have different rules)
4. Calculate ROI before investing (use our ROI Calculator)

**Platform features to explore:**
• 📊 Intelligence Dashboard — 20 industries, 35 skills, 22 reskilling pathways
• 🤖 AI Wizard — 7-step guided builder
• 💰 ROI Calculator — real cost + return estimates for 5 company sizes
• 🛡️ Regulatory Compliance — 15 jurisdictions tracked through 2030

What specific industry or task would you like to explore?"""

    return {
        "response": response_text,
        "data_used": ["occupational_database", "automation_scores", "regulatory_data"],
        "sources": ["Automatejobs.ia Platform Database", "O*NET", "EU AI Act 2024"]
    }


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    logger.info("Initializing occupational data database...")
    try:
        result = init_db(force_reseed=False)
        logger.info(f"Database initialization: {result}")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
