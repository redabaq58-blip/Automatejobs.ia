"""
Tier 1 Intelligence Queries - Game-Changing Data APIs
The data that makes investors say "holy shit"
"""
from typing import List, Dict, Any, Optional
from .tier1_intelligence import (
    INDUSTRY_AUTOMATION_MATURITY,
    ADOPTION_VELOCITY_BY_SIZE,
    FIRST_MOVER_WINDOWS,
    SKILLS_DECAY_PREDICTIONS,
    RESKILLING_PATHWAYS,
    SKILLS_ADJACENCY_GRAPH,
    REGULATORY_FORECAST,
    COMPLIANCE_RISK_SCORES,
    LABOR_ARBITRAGE_INDEX,
    GEOGRAPHIC_WAGE_INDEX,
    TCO_HIDDEN_COSTS,
    MAINTENANCE_BURDEN,
    VENDOR_LOCK_IN_RISK,
)
from .tier1_expansion import (
    EXPANDED_INDUSTRY_MATURITY,
    EXPANDED_SKILLS_DECAY,
    EXPANDED_RESKILLING_PATHWAYS,
    EXPANDED_REGULATORY_PREDICTIONS,
    EXPANDED_LABOR_ARBITRAGE,
    EXPANDED_TCO,
    AI_CAPABILITY_TIMELINE,
    INDUSTRY_DISRUPTION_FORECAST,
    VENDOR_LANDSCAPE,
    ROI_BENCHMARKS_BY_SIZE,
    AUTOMATION_FAILURE_RATES,
    OCCUPATION_AUTOMATION_TIMELINE,
    AUTOMATION_LEADERS,
    TASK_AUTOMATION_DIFFICULTY,
    EMERGING_TECH_RADAR,
    IMPLEMENTATION_PLAYBOOKS,
)


# =============================================================================
# 1. AUTOMATION ADOPTION INTELLIGENCE
# =============================================================================

def get_industry_automation_maturity(industry: str = None) -> Dict[str, Any]:
    """
    Get automation adoption benchmarks by industry.
    Shows who's automating what and how fast.
    """
    if industry:
        if industry in INDUSTRY_AUTOMATION_MATURITY:
            return {industry: INDUSTRY_AUTOMATION_MATURITY[industry]}
        return {"error": f"Industry not found. Available: {list(INDUSTRY_AUTOMATION_MATURITY.keys())}"}
    return INDUSTRY_AUTOMATION_MATURITY


def get_adoption_velocity(company_size: str = None) -> Dict[str, Any]:
    """
    Get adoption velocity curves by company size.
    How long it takes to go from pilot to mature.
    """
    if company_size:
        if company_size in ADOPTION_VELOCITY_BY_SIZE:
            return {company_size: ADOPTION_VELOCITY_BY_SIZE[company_size]}
        return {"error": f"Size not found. Available: {list(ADOPTION_VELOCITY_BY_SIZE.keys())}"}
    return ADOPTION_VELOCITY_BY_SIZE


def get_first_mover_windows() -> List[Dict[str, Any]]:
    """
    Get first-mover advantage windows.
    Shows which automation opportunities are closing.
    """
    windows = []
    for task, data in FIRST_MOVER_WINDOWS.items():
        windows.append({
            "automation_type": task,
            **data
        })
    # Sort by window_months ascending (most urgent first)
    windows.sort(key=lambda x: x["window_months"])
    return windows


def get_competitive_benchmark(industry: str, company_size: str) -> Dict[str, Any]:
    """
    Get competitive benchmark for your automation position.
    """
    if industry not in INDUSTRY_AUTOMATION_MATURITY:
        return {"error": "Industry not found"}
    if company_size not in ADOPTION_VELOCITY_BY_SIZE:
        return {"error": "Company size not found"}
    
    industry_data = INDUSTRY_AUTOMATION_MATURITY[industry]
    velocity_data = ADOPTION_VELOCITY_BY_SIZE[company_size]
    
    return {
        "industry": industry,
        "company_size": company_size,
        "industry_maturity_score": industry_data["overall_maturity_score"],
        "your_expected_timeline": {
            "pilot_to_scale_months": velocity_data["pilot_to_scale_months"],
            "scale_to_mature_months": velocity_data["scale_to_mature_months"],
            "expected_success_rate": velocity_data["success_rate"],
        },
        "top_tasks_to_automate": industry_data["top_automated_tasks"][:3],
        "industry_leaders": industry_data["leaders"],
        "typical_blockers": velocity_data["typical_blockers"],
        "recommendation": _get_adoption_recommendation(
            industry_data["overall_maturity_score"],
            velocity_data["success_rate"]
        ),
    }


def _get_adoption_recommendation(maturity_score: int, success_rate: float) -> str:
    if maturity_score < 40:
        return "FIRST MOVER OPPORTUNITY - Industry is early; aggressive automation creates competitive advantage"
    elif maturity_score < 60:
        return "GROWTH PHASE - Industry adopting rapidly; match pace or fall behind"
    elif maturity_score < 75:
        return "MATURATION PHASE - Automation is table stakes; focus on optimization"
    else:
        return "SATURATION - Automation is expected; differentiate through advanced capabilities"


# =============================================================================
# 2. SKILLS DECAY & RESKILLING
# =============================================================================

def get_skills_decay(skill: str = None) -> Dict[str, Any]:
    """
    Get skills half-life predictions.
    How long until skills become obsolete.
    """
    if skill:
        if skill in SKILLS_DECAY_PREDICTIONS:
            return {skill: SKILLS_DECAY_PREDICTIONS[skill]}
        return {"error": f"Skill not found. Available: {list(SKILLS_DECAY_PREDICTIONS.keys())}"}
    
    # Sort by half-life ascending (most urgent first)
    sorted_skills = sorted(
        SKILLS_DECAY_PREDICTIONS.items(),
        key=lambda x: x[1]["half_life_years"]
    )
    return {k: v for k, v in sorted_skills}


def get_reskilling_pathways(from_role: str = None) -> List[Dict[str, Any]]:
    """
    Get reskilling pathways with economics.
    Career transitions with costs, timelines, and ROI.
    """
    pathways = RESKILLING_PATHWAYS
    if from_role:
        pathways = [p for p in pathways if from_role.lower() in p["from_role"].lower()]
    
    # Sort by ROI (salary increase / cost)
    for p in pathways:
        p["roi_score"] = p["salary_increase_pct"] / (p["reskilling_cost_usd"] / 1000)
    
    pathways.sort(key=lambda x: x["roi_score"], reverse=True)
    return pathways


def get_skills_adjacency(skill: str) -> Dict[str, Any]:
    """
    Get skills adjacency graph - what skills transfer.
    """
    if skill in SKILLS_ADJACENCY_GRAPH:
        return {skill: SKILLS_ADJACENCY_GRAPH[skill]}
    return {"error": f"Skill not found. Available: {list(SKILLS_ADJACENCY_GRAPH.keys())}"}


def get_workforce_impact_summary() -> Dict[str, Any]:
    """
    Get aggregate workforce impact data.
    Total jobs at risk, reskilling opportunity size.
    """
    total_jobs_at_risk = sum(
        s["jobs_at_risk_usa"] for s in SKILLS_DECAY_PREDICTIONS.values()
    )
    
    critical_skills = [
        {"skill": k, **v} for k, v in SKILLS_DECAY_PREDICTIONS.items()
        if v["automation_threat_level"] == "CRITICAL"
    ]
    
    best_transitions = sorted(
        RESKILLING_PATHWAYS,
        key=lambda x: x["salary_increase_pct"],
        reverse=True
    )[:5]
    
    avg_reskilling_cost = sum(p["reskilling_cost_usd"] for p in RESKILLING_PATHWAYS) / len(RESKILLING_PATHWAYS)
    
    return {
        "total_jobs_at_risk_usa": total_jobs_at_risk,
        "critical_skills_count": len(critical_skills),
        "critical_skills": critical_skills,
        "average_reskilling_cost_usd": round(avg_reskilling_cost),
        "total_reskilling_market_size_usd": total_jobs_at_risk * avg_reskilling_cost,
        "best_roi_transitions": best_transitions,
    }


# =============================================================================
# 3. REGULATORY FORECAST
# =============================================================================

def get_regulatory_forecast(jurisdiction: str = None) -> Dict[str, Any]:
    """
    Get predicted regulatory changes by jurisdiction.
    """
    if jurisdiction:
        if jurisdiction in REGULATORY_FORECAST:
            return {jurisdiction: REGULATORY_FORECAST[jurisdiction]}
        return {"error": f"Jurisdiction not found. Available: {list(REGULATORY_FORECAST.keys())}"}
    return REGULATORY_FORECAST


def get_compliance_risk_scores(task_type: str = None) -> Dict[str, Any]:
    """
    Get compliance risk scores by task type.
    """
    if task_type:
        if task_type in COMPLIANCE_RISK_SCORES:
            return {task_type: COMPLIANCE_RISK_SCORES[task_type]}
        return {"error": f"Task type not found. Available: {list(COMPLIANCE_RISK_SCORES.keys())}"}
    
    # Sort by current risk score descending
    sorted_risks = sorted(
        COMPLIANCE_RISK_SCORES.items(),
        key=lambda x: x[1]["current_risk_score"],
        reverse=True
    )
    return {k: v for k, v in sorted_risks}


def get_regulatory_timeline() -> List[Dict[str, Any]]:
    """
    Get all predicted regulatory changes sorted by date.
    """
    all_changes = []
    for jurisdiction, data in REGULATORY_FORECAST.items():
        for change in data["predicted_changes"]:
            all_changes.append({
                "jurisdiction": jurisdiction,
                "regulatory_body": data["regulatory_body"],
                **change
            })
    
    # Sort by date
    all_changes.sort(key=lambda x: x["predicted_date"])
    return all_changes


def get_compliance_readiness_checklist(task_type: str, jurisdictions: List[str]) -> Dict[str, Any]:
    """
    Get compliance readiness checklist for specific task and jurisdictions.
    """
    checklist = {
        "task_type": task_type,
        "jurisdictions": jurisdictions,
        "risk_assessment": {},
        "upcoming_requirements": [],
        "action_items": [],
    }
    
    if task_type in COMPLIANCE_RISK_SCORES:
        checklist["risk_assessment"] = COMPLIANCE_RISK_SCORES[task_type]
    
    for jurisdiction in jurisdictions:
        if jurisdiction in REGULATORY_FORECAST:
            for change in REGULATORY_FORECAST[jurisdiction]["predicted_changes"]:
                if any(task_type.lower() in t.lower() for t in change.get("affected_tasks", [])):
                    checklist["upcoming_requirements"].append({
                        "jurisdiction": jurisdiction,
                        **change
                    })
                    checklist["action_items"].append(change["action_required"])
    
    return checklist


# =============================================================================
# 4. LABOR ARBITRAGE INDEX
# =============================================================================

def get_labor_arbitrage_index(occupation: str = None) -> Dict[str, Any]:
    """
    Get labor arbitrage index - wage trends driving automation urgency.
    """
    if occupation:
        if occupation in LABOR_ARBITRAGE_INDEX:
            return {occupation: LABOR_ARBITRAGE_INDEX[occupation]}
        return {"error": f"Occupation not found. Available: {list(LABOR_ARBITRAGE_INDEX.keys())}"}
    
    # Sort by arbitrage score descending
    sorted_index = sorted(
        LABOR_ARBITRAGE_INDEX.items(),
        key=lambda x: x[1]["arbitrage_score"],
        reverse=True
    )
    return {k: v for k, v in sorted_index}


def get_geographic_wage_index(location: str = None) -> Dict[str, Any]:
    """
    Get geographic wage multipliers.
    """
    if location:
        if location in GEOGRAPHIC_WAGE_INDEX:
            return {location: GEOGRAPHIC_WAGE_INDEX[location]}
        return {"error": f"Location not found. Available: {list(GEOGRAPHIC_WAGE_INDEX.keys())}"}
    return GEOGRAPHIC_WAGE_INDEX


def calculate_location_adjusted_roi(
    occupation: str,
    location: str,
    base_implementation_cost: float
) -> Dict[str, Any]:
    """
    Calculate location-adjusted automation ROI.
    """
    if occupation not in LABOR_ARBITRAGE_INDEX:
        return {"error": "Occupation not found"}
    if location not in GEOGRAPHIC_WAGE_INDEX:
        return {"error": "Location not found"}
    
    occ_data = LABOR_ARBITRAGE_INDEX[occupation]
    geo_data = GEOGRAPHIC_WAGE_INDEX[location]
    
    adjusted_wage = occ_data["current_wage_usd"] * geo_data["wage_multiplier"]
    adjusted_arbitrage = occ_data["arbitrage_score"] + geo_data["automation_urgency_boost"]
    
    # Simple ROI calculation
    annual_savings = adjusted_wage * 0.85 * 1.35  # 85% automation, 1.35x fully loaded
    payback_months = (base_implementation_cost / annual_savings) * 12
    
    return {
        "occupation": occupation,
        "location": location,
        "base_wage_usd": occ_data["current_wage_usd"],
        "location_adjusted_wage_usd": round(adjusted_wage),
        "wage_multiplier": geo_data["wage_multiplier"],
        "base_arbitrage_score": occ_data["arbitrage_score"],
        "location_adjusted_arbitrage_score": min(adjusted_arbitrage, 100),
        "urgency": _get_urgency_label(adjusted_arbitrage),
        "estimated_annual_savings_usd": round(annual_savings),
        "estimated_payback_months": round(payback_months, 1),
        "recommendation": f"In {location}, automation ROI is {'higher' if geo_data['wage_multiplier'] > 1 else 'lower'} than national average",
    }


def _get_urgency_label(score: float) -> str:
    if score >= 90:
        return "CRITICAL - Automate immediately"
    elif score >= 75:
        return "HIGH - Automate within 6 months"
    elif score >= 60:
        return "MEDIUM - Plan automation within 12 months"
    elif score >= 40:
        return "LOW - Monitor and plan"
    else:
        return "MINIMAL - Automation not urgent"


def get_automate_now_list() -> List[Dict[str, Any]]:
    """
    Get ranked list of what to automate NOW based on arbitrage.
    """
    automate_now = []
    for occ, data in LABOR_ARBITRAGE_INDEX.items():
        if data["automate_now_urgency"] in ["CRITICAL", "HIGH"]:
            automate_now.append({
                "occupation": occ,
                "arbitrage_score": data["arbitrage_score"],
                "urgency": data["automate_now_urgency"],
                "wage_growth_yoy": f"{data['wage_growth_yoy']*100:.1f}%",
                "automation_cost_trend": data["automation_cost_trend"],
                "breakeven_improving_by": f"{abs(data['breakeven_shift_months'])} months/year",
                "labor_shortage": data["projected_labor_shortage"],
            })
    
    automate_now.sort(key=lambda x: x["arbitrage_score"], reverse=True)
    return automate_now


# =============================================================================
# 5. TOTAL COST OF OWNERSHIP
# =============================================================================

def get_tco_analysis(automation_type: str = None) -> Dict[str, Any]:
    """
    Get total cost of ownership analysis including hidden costs.
    """
    if automation_type:
        if automation_type in TCO_HIDDEN_COSTS:
            return {automation_type: TCO_HIDDEN_COSTS[automation_type]}
        return {"error": f"Type not found. Available: {list(TCO_HIDDEN_COSTS.keys())}"}
    return TCO_HIDDEN_COSTS


def get_hidden_cost_multipliers() -> List[Dict[str, Any]]:
    """
    Get hidden cost multipliers by automation type.
    Shows how much budgets typically underestimate.
    """
    multipliers = []
    for auto_type, data in TCO_HIDDEN_COSTS.items():
        multipliers.append({
            "automation_type": auto_type,
            "hidden_cost_multiplier": data["hidden_cost_multiplier"],
            "total_visible_usd": data["total_visible"],
            "total_hidden_usd": data["total_hidden"],
            "total_tco_year1_usd": data["total_tco_year1"],
            "top_budget_overrun": data["common_budget_overruns"][0],
        })
    
    multipliers.sort(key=lambda x: x["hidden_cost_multiplier"], reverse=True)
    return multipliers


def get_maintenance_burden(automation_category: str = None) -> Dict[str, Any]:
    """
    Get maintenance burden estimates (Year 2-5 costs).
    """
    if automation_category:
        if automation_category in MAINTENANCE_BURDEN:
            return {automation_category: MAINTENANCE_BURDEN[automation_category]}
        return {"error": f"Category not found. Available: {list(MAINTENANCE_BURDEN.keys())}"}
    return MAINTENANCE_BURDEN


def get_vendor_lock_in_risk(vendor: str = None) -> Dict[str, Any]:
    """
    Get vendor lock-in risk assessment.
    """
    if vendor:
        if vendor in VENDOR_LOCK_IN_RISK:
            return {vendor: VENDOR_LOCK_IN_RISK[vendor]}
        return {"error": f"Vendor not found. Available: {list(VENDOR_LOCK_IN_RISK.keys())}"}
    
    # Sort by lock-in score descending
    sorted_vendors = sorted(
        VENDOR_LOCK_IN_RISK.items(),
        key=lambda x: x[1]["lock_in_score"],
        reverse=True
    )
    return {k: v for k, v in sorted_vendors}


def calculate_5_year_tco(
    automation_type: str,
    automation_category: str
) -> Dict[str, Any]:
    """
    Calculate complete 5-year TCO projection.
    """
    if automation_type not in TCO_HIDDEN_COSTS:
        return {"error": "Automation type not found"}
    if automation_category not in MAINTENANCE_BURDEN:
        return {"error": "Automation category not found"}
    
    tco = TCO_HIDDEN_COSTS[automation_type]
    maintenance = MAINTENANCE_BURDEN[automation_category]
    
    year1 = tco["total_tco_year1"]
    year2 = year1 * maintenance["year2_pct"]
    year3 = year1 * maintenance["year3_pct"]
    year4 = year1 * maintenance["year4_pct"]
    year5 = year1 * maintenance["year5_pct"]
    
    total_5yr = year1 + year2 + year3 + year4 + year5
    
    return {
        "automation_type": automation_type,
        "automation_category": automation_category,
        "year_1_tco": round(year1),
        "year_2_tco": round(year2),
        "year_3_tco": round(year3),
        "year_4_tco": round(year4),
        "year_5_tco": round(year5),
        "total_5_year_tco": round(total_5yr),
        "breakdown": {
            "visible_costs": tco["total_visible"],
            "hidden_costs": tco["total_hidden"],
            "hidden_cost_multiplier": tco["hidden_cost_multiplier"],
        },
        "budget_risks": tco["common_budget_overruns"],
        "recommendation": f"Budget {tco['hidden_cost_multiplier']:.0%} more than vendor quotes",
    }


# =============================================================================
# COMPOSITE INTELLIGENCE ENDPOINTS
# =============================================================================

def get_automation_pressure_index(occupation: str) -> Dict[str, Any]:
    """
    THE SIGNATURE METRIC: Automation Pressure Index™
    Combines wage growth + tool capability + competitor adoption + regulatory openness
    """
    if occupation not in LABOR_ARBITRAGE_INDEX:
        return {"error": "Occupation not found"}
    
    labor = LABOR_ARBITRAGE_INDEX[occupation]
    
    # Find related skills decay
    skill_decay = None
    for skill, data in SKILLS_DECAY_PREDICTIONS.items():
        if occupation.lower() in skill.lower() or skill.lower() in occupation.lower():
            skill_decay = data
            break
    
    # Calculate composite index
    wage_pressure = min(labor["wage_growth_yoy"] * 500, 30)  # Max 30 points
    cost_decline = min(abs(labor["automation_cost_change_yoy"]) * 100, 25)  # Max 25 points
    adoption_pressure = labor["arbitrage_score"] * 0.25  # Max 25 points
    
    # Regulatory openness (inverse of risk)
    regulatory_openness = 20  # Default
    for task, risk in COMPLIANCE_RISK_SCORES.items():
        if occupation.lower() in task.lower():
            regulatory_openness = max(0, 20 - (risk["current_risk_score"] / 5))
            break
    
    total_index = wage_pressure + cost_decline + adoption_pressure + regulatory_openness
    
    return {
        "occupation": occupation,
        "automation_pressure_index": round(total_index, 1),
        "max_possible": 100,
        "components": {
            "wage_pressure": round(wage_pressure, 1),
            "automation_cost_decline": round(cost_decline, 1),
            "market_adoption": round(adoption_pressure, 1),
            "regulatory_openness": round(regulatory_openness, 1),
        },
        "labor_arbitrage": labor,
        "skills_decay": skill_decay,
        "interpretation": _interpret_pressure_index(total_index),
        "action": _get_pressure_action(total_index),
    }


def _interpret_pressure_index(index: float) -> str:
    if index >= 80:
        return "EXTREME PRESSURE - Automation is inevitable and imminent"
    elif index >= 65:
        return "HIGH PRESSURE - Strong economic forces driving automation"
    elif index >= 50:
        return "MODERATE PRESSURE - Automation makes sense but not urgent"
    elif index >= 35:
        return "LOW PRESSURE - Limited economic case for automation"
    else:
        return "MINIMAL PRESSURE - Human labor remains cost-effective"


def _get_pressure_action(index: float) -> str:
    if index >= 80:
        return "Automate within 3 months or face competitive disadvantage"
    elif index >= 65:
        return "Begin automation planning immediately, implement within 6 months"
    elif index >= 50:
        return "Evaluate automation options, plan for 12-month implementation"
    elif index >= 35:
        return "Monitor automation developments, no immediate action needed"
    else:
        return "Focus on other optimization opportunities"


def get_executive_dashboard() -> Dict[str, Any]:
    """
    Executive dashboard with all key Tier 1 metrics.
    """
    # Top urgent automations
    automate_now = get_automate_now_list()[:5]
    
    # Closing first-mover windows
    closing_windows = [
        w for w in get_first_mover_windows()
        if w["window_status"] in ["CLOSING", "NARROWING"]
    ][:3]
    
    # Highest risk compliance areas
    high_risk = [
        {"task": k, **v} for k, v in COMPLIANCE_RISK_SCORES.items()
        if v["current_risk_score"] >= 70
    ]
    
    # Workforce impact
    workforce = get_workforce_impact_summary()
    
    # Hidden cost warnings
    hidden_costs = get_hidden_cost_multipliers()[:3]
    
    return {
        "generated_at": "2026-03-10T14:30:00Z",
        "key_metrics": {
            "total_jobs_at_risk_usa": workforce["total_jobs_at_risk_usa"],
            "avg_hidden_cost_multiplier": sum(h["hidden_cost_multiplier"] for h in hidden_costs) / len(hidden_costs),
            "high_risk_compliance_areas": len(high_risk),
        },
        "automate_now": automate_now,
        "closing_windows": closing_windows,
        "compliance_alerts": high_risk,
        "budget_warnings": hidden_costs,
        "reskilling_opportunity": {
            "market_size_usd": workforce["total_reskilling_market_size_usd"],
            "best_roi_pathway": workforce["best_roi_transitions"][0] if workforce["best_roi_transitions"] else None,
        },
    }


# =============================================================================
# 6. EXPANDED INDUSTRY & MATURITY DATA
# =============================================================================

def get_all_industry_maturity() -> Dict[str, Any]:
    """
    Get combined industry automation maturity (base + expanded).
    Total of 20 industries.
    """
    combined = {**INDUSTRY_AUTOMATION_MATURITY, **EXPANDED_INDUSTRY_MATURITY}
    return combined


def get_industry_maturity_rankings() -> List[Dict[str, Any]]:
    """
    Get all industries ranked by automation maturity score.
    """
    combined = get_all_industry_maturity()
    rankings = []
    for industry, data in combined.items():
        rankings.append({
            "industry": industry,
            "maturity_score": data["overall_maturity_score"],
            "avg_time_to_scale_months": data["avg_time_to_scale_months"],
            "leaders": data["leaders"],
            "top_task": data["top_automated_tasks"][0] if data["top_automated_tasks"] else None,
        })
    rankings.sort(key=lambda x: x["maturity_score"], reverse=True)
    return rankings


# =============================================================================
# 7. EXPANDED SKILLS DECAY & RESKILLING
# =============================================================================

def get_all_skills_decay() -> Dict[str, Any]:
    """
    Get combined skills decay predictions (base + expanded).
    Total of 35+ skills.
    """
    combined = {**SKILLS_DECAY_PREDICTIONS, **EXPANDED_SKILLS_DECAY}
    # Sort by half-life ascending (most urgent first)
    sorted_skills = sorted(combined.items(), key=lambda x: x[1]["half_life_years"])
    return {k: v for k, v in sorted_skills}


def get_skills_at_risk_summary() -> Dict[str, Any]:
    """
    Get summary of skills at risk by threat level.
    """
    all_skills = {**SKILLS_DECAY_PREDICTIONS, **EXPANDED_SKILLS_DECAY}
    
    by_threat_level = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": [], "VERY_LOW": []}
    total_jobs = 0
    
    for skill, data in all_skills.items():
        level = data["automation_threat_level"]
        if level in by_threat_level:
            by_threat_level[level].append({
                "skill": skill,
                "half_life_years": data["half_life_years"],
                "jobs_at_risk_usa": data["jobs_at_risk_usa"],
            })
            total_jobs += data["jobs_at_risk_usa"]
    
    return {
        "total_skills_tracked": len(all_skills),
        "total_jobs_at_risk_usa": total_jobs,
        "by_threat_level": by_threat_level,
        "critical_count": len(by_threat_level["CRITICAL"]),
        "high_count": len(by_threat_level["HIGH"]),
    }


def get_all_reskilling_pathways() -> List[Dict[str, Any]]:
    """
    Get combined reskilling pathways (base + expanded).
    Total of 22+ pathways.
    """
    combined = RESKILLING_PATHWAYS + EXPANDED_RESKILLING_PATHWAYS
    # Calculate ROI score for each
    for p in combined:
        p["roi_score"] = p["salary_increase_pct"] / (p["reskilling_cost_usd"] / 1000)
    combined.sort(key=lambda x: x["roi_score"], reverse=True)
    return combined


def get_highest_roi_reskilling(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get the highest ROI reskilling pathways.
    """
    pathways = get_all_reskilling_pathways()
    return pathways[:limit]


# =============================================================================
# 8. EXPANDED REGULATORY PREDICTIONS
# =============================================================================

def get_all_regulatory_forecasts() -> Dict[str, Any]:
    """
    Get combined regulatory forecasts (base + expanded).
    Total of 13+ jurisdictions.
    """
    combined = {**REGULATORY_FORECAST, **EXPANDED_REGULATORY_PREDICTIONS}
    return combined


def get_global_regulatory_timeline() -> List[Dict[str, Any]]:
    """
    Get all predicted regulatory changes globally, sorted by date.
    """
    all_forecasts = get_all_regulatory_forecasts()
    all_changes = []
    
    for jurisdiction, data in all_forecasts.items():
        for change in data.get("predicted_changes", []):
            all_changes.append({
                "jurisdiction": jurisdiction,
                "regulatory_body": data.get("regulatory_body", "Unknown"),
                **change
            })
    
    all_changes.sort(key=lambda x: x["predicted_date"])
    return all_changes


def get_high_probability_regulations(min_probability: float = 0.7) -> List[Dict[str, Any]]:
    """
    Get regulatory changes with high probability of occurring.
    """
    timeline = get_global_regulatory_timeline()
    return [r for r in timeline if r.get("probability", 0) >= min_probability]


# =============================================================================
# 9. EXPANDED LABOR ARBITRAGE
# =============================================================================

def get_all_labor_arbitrage() -> Dict[str, Any]:
    """
    Get combined labor arbitrage index (base + expanded).
    Total of 24+ occupations.
    """
    combined = {**LABOR_ARBITRAGE_INDEX, **EXPANDED_LABOR_ARBITRAGE}
    # Sort by arbitrage score descending
    sorted_index = sorted(combined.items(), key=lambda x: x[1]["arbitrage_score"], reverse=True)
    return {k: v for k, v in sorted_index}


def get_critical_arbitrage_occupations() -> List[Dict[str, Any]]:
    """
    Get occupations with critical automation urgency.
    """
    all_arbitrage = get_all_labor_arbitrage()
    critical = []
    for occ, data in all_arbitrage.items():
        if data["automate_now_urgency"] in ["CRITICAL", "HIGH"]:
            critical.append({
                "occupation": occ,
                "arbitrage_score": data["arbitrage_score"],
                "urgency": data["automate_now_urgency"],
                "current_wage_usd": data["current_wage_usd"],
                "wage_growth_yoy_pct": round(data["wage_growth_yoy"] * 100, 1),
                "labor_shortage": data["projected_labor_shortage"],
            })
    return critical


# =============================================================================
# 10. EXPANDED TCO DATA
# =============================================================================

def get_all_tco_analyses() -> Dict[str, Any]:
    """
    Get combined TCO analyses (base + expanded).
    Total of 15+ automation types.
    """
    combined = {**TCO_HIDDEN_COSTS, **EXPANDED_TCO}
    return combined


def get_highest_hidden_cost_multipliers(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get automation types with highest hidden cost multipliers.
    """
    all_tco = get_all_tco_analyses()
    results = []
    for auto_type, data in all_tco.items():
        results.append({
            "automation_type": auto_type,
            "hidden_cost_multiplier": data["hidden_cost_multiplier"],
            "total_visible_usd": data["total_visible"],
            "total_hidden_usd": data["total_hidden"],
            "total_tco_year1_usd": data["total_tco_year1"],
            "top_overrun_risk": data["common_budget_overruns"][0] if data["common_budget_overruns"] else None,
        })
    results.sort(key=lambda x: x["hidden_cost_multiplier"], reverse=True)
    return results[:limit]


# =============================================================================
# 11. AI CAPABILITY TIMELINE
# =============================================================================

def get_ai_capability_timeline(year: str = None) -> Dict[str, Any]:
    """
    Get AI capability predictions by year.
    """
    if year:
        key = f"{year}_predicted" if year != "2024" else "2024_current"
        if key in AI_CAPABILITY_TIMELINE:
            return {year: AI_CAPABILITY_TIMELINE[key]}
        return {"error": "Year not found. Available: 2024, 2026, 2028, 2030"}
    return AI_CAPABILITY_TIMELINE


def get_task_automation_trajectory(task_category: str) -> Dict[str, Any]:
    """
    Get when a task category will be fully automatable.
    """
    timeline = AI_CAPABILITY_TIMELINE
    result = {
        "task_category": task_category,
        "trajectory": []
    }
    
    for period, data in timeline.items():
        year = period.split("_")[0]
        status = "UNKNOWN"
        if task_category.lower() in str(data.get("tasks_fully_automatable", [])).lower():
            status = "FULLY_AUTOMATABLE"
        elif task_category.lower() in str(data.get("tasks_human_assisted", [])).lower():
            status = "HUMAN_ASSISTED"
        elif task_category.lower() in str(data.get("tasks_human_required", [])).lower():
            status = "HUMAN_REQUIRED"
        
        result["trajectory"].append({"year": year, "status": status})
    
    return result


# =============================================================================
# 12. INDUSTRY DISRUPTION FORECASTS
# =============================================================================

def get_industry_disruption_forecast() -> Dict[str, Any]:
    """
    Get industry disruption predictions 2026-2030.
    """
    return INDUSTRY_DISRUPTION_FORECAST


def get_most_disrupted_industries(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get the industries facing most disruption.
    """
    disrupted = INDUSTRY_DISRUPTION_FORECAST.get("Most Disrupted 2026-2030", [])
    return sorted(disrupted, key=lambda x: x["disruption_score"], reverse=True)[:limit]


def get_safest_industries(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get the industries least disrupted by automation.
    """
    return INDUSTRY_DISRUPTION_FORECAST.get("Least Disrupted 2026-2030", [])[:limit]


# =============================================================================
# 13. VENDOR LANDSCAPE
# =============================================================================

def get_vendor_landscape(category: str = None) -> Dict[str, Any]:
    """
    Get vendor analysis by category.
    """
    if category:
        if category in VENDOR_LANDSCAPE:
            return {category: VENDOR_LANDSCAPE[category]}
        return {"error": f"Category not found. Available: {list(VENDOR_LANDSCAPE.keys())}"}
    return VENDOR_LANDSCAPE


def get_vendor_comparison(category: str) -> List[Dict[str, Any]]:
    """
    Get vendor comparison for a specific category.
    """
    if category not in VENDOR_LANDSCAPE:
        return []
    
    vendors = []
    for name, data in VENDOR_LANDSCAPE[category].items():
        vendors.append({"vendor": name, **data})
    
    # Sort by market share
    vendors.sort(key=lambda x: x.get("market_share_pct", 0), reverse=True)
    return vendors


def get_vendor_recommendations(use_case: str, budget: str = "MEDIUM") -> Dict[str, Any]:
    """
    Get vendor recommendations based on use case and budget.
    """
    recommendations = {
        "use_case": use_case,
        "budget": budget,
        "recommended_vendors": []
    }
    
    use_case_lower = use_case.lower()
    
    # Match use case to vendor categories
    if any(kw in use_case_lower for kw in ["rpa", "automation", "process"]):
        vendors = VENDOR_LANDSCAPE.get("RPA_PLATFORMS", {})
        for name, data in vendors.items():
            if budget == "LOW" and data.get("avg_annual_cost_per_robot", 0) < 5000:
                recommendations["recommended_vendors"].append({"vendor": name, **data})
            elif budget == "MEDIUM" and data.get("avg_annual_cost_per_robot", 0) < 10000:
                recommendations["recommended_vendors"].append({"vendor": name, **data})
            elif budget == "HIGH":
                recommendations["recommended_vendors"].append({"vendor": name, **data})
    
    elif any(kw in use_case_lower for kw in ["llm", "ai", "chat", "text", "gpt"]):
        recommendations["recommended_vendors"] = [
            {"vendor": name, **data} for name, data in VENDOR_LANDSCAPE.get("LLM_PROVIDERS", {}).items()
        ]
    
    elif any(kw in use_case_lower for kw in ["document", "ocr", "invoice", "form"]):
        recommendations["recommended_vendors"] = [
            {"vendor": name, **data} for name, data in VENDOR_LANDSCAPE.get("DOCUMENT_AI", {}).items()
        ]
    
    return recommendations


# =============================================================================
# 14. ROI BENCHMARKS BY COMPANY SIZE
# =============================================================================

def get_roi_benchmarks(company_size: str = None) -> Dict[str, Any]:
    """
    Get ROI benchmarks by company size.
    """
    if company_size:
        if company_size in ROI_BENCHMARKS_BY_SIZE:
            return {company_size: ROI_BENCHMARKS_BY_SIZE[company_size]}
        return {"error": f"Size not found. Available: {list(ROI_BENCHMARKS_BY_SIZE.keys())}"}
    return ROI_BENCHMARKS_BY_SIZE


def get_expected_automation_roi(company_size: str, automation_budget: float) -> Dict[str, Any]:
    """
    Calculate expected ROI based on company size and budget.
    """
    if company_size not in ROI_BENCHMARKS_BY_SIZE:
        return {"error": "Company size not found"}
    
    benchmark = ROI_BENCHMARKS_BY_SIZE[company_size]
    
    # Adjust for actual budget vs typical
    budget_ratio = automation_budget / benchmark["typical_automation_budget_usd"]
    adjusted_fte = benchmark["typical_fte_equivalent_saved"] * min(budget_ratio, 2.0)
    
    # Estimate savings (assuming $60k avg loaded cost)
    annual_savings = adjusted_fte * 60000
    total_cost = automation_budget * benchmark["hidden_cost_multiplier"]
    payback_months = (total_cost / annual_savings) * 12 if annual_savings > 0 else 999
    
    return {
        "company_size": company_size,
        "automation_budget_usd": automation_budget,
        "estimated_total_cost_usd": round(total_cost),
        "hidden_cost_multiplier": benchmark["hidden_cost_multiplier"],
        "estimated_fte_equivalent_saved": round(adjusted_fte, 1),
        "estimated_annual_savings_usd": round(annual_savings),
        "estimated_payback_months": round(payback_months, 1),
        "success_rate_pct": benchmark["success_rate_pct"],
        "recommended_first_automations": benchmark["common_first_automations"],
        "key_risks": benchmark["key_risks"],
    }


# =============================================================================
# 15. AUTOMATION FAILURE ANALYSIS
# =============================================================================

def get_automation_failure_rates(automation_type: str = None) -> Dict[str, Any]:
    """
    Get automation failure rates and reasons.
    """
    if automation_type:
        if automation_type in AUTOMATION_FAILURE_RATES["failure_by_type"]:
            return {automation_type: AUTOMATION_FAILURE_RATES["failure_by_type"][automation_type]}
        return {"error": f"Type not found. Available: {list(AUTOMATION_FAILURE_RATES['failure_by_type'].keys())}"}
    return AUTOMATION_FAILURE_RATES


def get_failure_prevention_guide(automation_type: str) -> Dict[str, Any]:
    """
    Get failure prevention recommendations for a specific automation type.
    """
    if automation_type not in AUTOMATION_FAILURE_RATES["failure_by_type"]:
        return {"error": "Automation type not found"}
    
    data = AUTOMATION_FAILURE_RATES["failure_by_type"][automation_type]
    
    return {
        "automation_type": automation_type,
        "failure_rate": data["failure_rate"],
        "top_failure_reasons": data["top_failure_reasons"][:3],
        "prevention_strategies": [
            f"Address {r['reason']} proactively (causes {r['frequency']*100:.0f}% of failures)"
            for r in data["top_failure_reasons"][:3]
        ],
        "recovery_options": AUTOMATION_FAILURE_RATES["recovery_strategies"],
        "avg_cost_of_failure_usd": data["avg_cost_of_failure"],
    }


# =============================================================================
# 16. OCCUPATION AUTOMATION TIMELINE
# =============================================================================

def get_occupation_automation_timeline(occupation: str = None) -> Dict[str, Any]:
    """
    Get detailed automation timeline for specific occupations.
    """
    if occupation:
        if occupation in OCCUPATION_AUTOMATION_TIMELINE:
            return {occupation: OCCUPATION_AUTOMATION_TIMELINE[occupation]}
        return {"error": f"Occupation not found. Available: {list(OCCUPATION_AUTOMATION_TIMELINE.keys())}"}
    return OCCUPATION_AUTOMATION_TIMELINE


def get_occupations_by_displacement_risk(risk_level: str = None) -> List[Dict[str, Any]]:
    """
    Get occupations filtered by displacement risk level.
    """
    results = []
    for occ, data in OCCUPATION_AUTOMATION_TIMELINE.items():
        if risk_level is None or data["job_displacement_risk"] == risk_level:
            results.append({
                "occupation": occ,
                "current_automation_pct": data["current_automation_level_pct"],
                "inflection_year": data["inflection_year"],
                "displacement_risk": data["job_displacement_risk"],
                "transformation_path": data["transformation_path"],
            })
    
    results.sort(key=lambda x: x["current_automation_pct"], reverse=True)
    return results


# =============================================================================
# 17. COMPETITIVE INTELLIGENCE
# =============================================================================

def get_automation_leaders(sector: str = None) -> Dict[str, Any]:
    """
    Get automation leaders by sector.
    """
    if sector:
        if sector in AUTOMATION_LEADERS:
            return {sector: AUTOMATION_LEADERS[sector]}
        return {"error": f"Sector not found. Available: {list(AUTOMATION_LEADERS.keys())}"}
    return AUTOMATION_LEADERS


def get_automation_gap_analysis(sector: str) -> Dict[str, Any]:
    """
    Get automation gap analysis for a sector.
    """
    if sector not in AUTOMATION_LEADERS:
        return {"error": "Sector not found"}
    
    data = AUTOMATION_LEADERS[sector]
    leader_avg = sum(leader["automation_maturity_score"] for leader in data["leaders"]) / len(data["leaders"])
    
    return {
        "sector": sector,
        "leader_average_score": round(leader_avg, 1),
        "laggard_average_score": data["laggards_avg_score"],
        "automation_gap": data["industry_automation_gap"],
        "leaders": data["leaders"],
        "total_leader_savings_usd": sum(leader["estimated_annual_savings_usd"] for leader in data["leaders"]),
        "competitive_insight": f"Leaders in {sector} save ${sum(leader['estimated_annual_savings_usd'] for leader in data['leaders']):,} annually through automation",
    }


# =============================================================================
# 18. TASK DIFFICULTY SCORES
# =============================================================================

def get_task_automation_difficulty(task: str = None) -> Dict[str, Any]:
    """
    Get automation difficulty scores for tasks.
    """
    if task:
        if task in TASK_AUTOMATION_DIFFICULTY:
            return {task: TASK_AUTOMATION_DIFFICULTY[task]}
        return {"error": f"Task not found. Available: {list(TASK_AUTOMATION_DIFFICULTY.keys())}"}
    return TASK_AUTOMATION_DIFFICULTY


def get_easiest_tasks_to_automate(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get the easiest tasks to automate.
    """
    tasks = []
    for task, data in TASK_AUTOMATION_DIFFICULTY.items():
        tasks.append({"task": task, **data})
    tasks.sort(key=lambda x: x["overall_difficulty_score"])
    return tasks[:limit]


def get_quick_win_tasks(max_weeks: int = 8) -> List[Dict[str, Any]]:
    """
    Get quick win automation opportunities.
    """
    quick_wins = []
    for task, data in TASK_AUTOMATION_DIFFICULTY.items():
        if data["time_to_implement_weeks"] <= max_weeks:
            quick_wins.append({
                "task": task,
                "difficulty_score": data["overall_difficulty_score"],
                "time_to_implement_weeks": data["time_to_implement_weeks"],
                "typical_accuracy": data["typical_accuracy_achievable"],
                "recommended_tools": data["recommended_tools"],
            })
    quick_wins.sort(key=lambda x: x["time_to_implement_weeks"])
    return quick_wins


# =============================================================================
# 19. EMERGING TECHNOLOGY RADAR
# =============================================================================

def get_emerging_tech_radar(quadrant: str = None) -> Dict[str, Any]:
    """
    Get emerging technology radar.
    """
    if quadrant:
        if quadrant in EMERGING_TECH_RADAR:
            return {quadrant: EMERGING_TECH_RADAR[quadrant]}
        return {"error": f"Quadrant not found. Available: {list(EMERGING_TECH_RADAR.keys())}"}
    return EMERGING_TECH_RADAR


def get_tech_to_adopt_now() -> List[Dict[str, Any]]:
    """
    Get technologies that should be adopted now.
    """
    return EMERGING_TECH_RADAR.get("ADOPT_NOW", [])


def get_tech_to_trial() -> List[Dict[str, Any]]:
    """
    Get technologies worth trialing.
    """
    return EMERGING_TECH_RADAR.get("TRIAL", [])


# =============================================================================
# 20. IMPLEMENTATION PLAYBOOKS
# =============================================================================

def get_implementation_playbook(use_case: str = None) -> Dict[str, Any]:
    """
    Get step-by-step implementation playbook.
    """
    if use_case:
        if use_case in IMPLEMENTATION_PLAYBOOKS:
            return {use_case: IMPLEMENTATION_PLAYBOOKS[use_case]}
        return {"error": f"Playbook not found. Available: {list(IMPLEMENTATION_PLAYBOOKS.keys())}"}
    return IMPLEMENTATION_PLAYBOOKS


def get_playbook_summary() -> List[Dict[str, Any]]:
    """
    Get summary of all implementation playbooks.
    """
    summaries = []
    for name, data in IMPLEMENTATION_PLAYBOOKS.items():
        summaries.append({
            "use_case": name,
            "total_duration_weeks": data["total_duration_weeks"],
            "total_cost_estimate_usd": data["total_cost_estimate_usd"],
            "expected_roi_year1": data["expected_roi_year1"],
            "phases_count": len(data["phases"]),
            "risk_factors": data["risk_factors"],
        })
    return summaries


# =============================================================================
# 21. ENHANCED EXECUTIVE DASHBOARD
# =============================================================================

def get_enhanced_executive_dashboard() -> Dict[str, Any]:
    """
    Enhanced executive dashboard with all expanded metrics.
    """
    # Get base dashboard
    base = get_executive_dashboard()
    
    # Add expanded metrics
    all_skills = get_skills_at_risk_summary()
    industry_rankings = get_industry_maturity_rankings()[:5]
    disrupted = get_most_disrupted_industries(3)
    tech_radar = get_tech_to_adopt_now()[:3]
    quick_wins = get_quick_win_tasks(6)[:3]
    failure_data = get_automation_failure_rates()
    
    return {
        **base,
        "expanded_metrics": {
            "total_skills_tracked": all_skills["total_skills_tracked"],
            "critical_skills_at_risk": all_skills["critical_count"],
            "overall_automation_failure_rate": failure_data["overall_failure_rate"],
        },
        "industry_leaders": industry_rankings,
        "most_disrupted_industries": disrupted,
        "technologies_to_adopt": tech_radar,
        "quick_win_automations": quick_wins,
        "data_coverage": {
            "industries": len(get_all_industry_maturity()),
            "skills": len(get_all_skills_decay()),
            "reskilling_pathways": len(get_all_reskilling_pathways()),
            "jurisdictions": len(get_all_regulatory_forecasts()),
            "occupations_tracked": len(get_all_labor_arbitrage()),
            "tco_analyses": len(get_all_tco_analyses()),
        },
    }
