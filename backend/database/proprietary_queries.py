"""
Proprietary Data Queries - The Competitive Moat
These queries expose unique data that no competitor has.
"""
from typing import List, Dict, Any, Optional

from .proprietary_data import (
    AI_TOOLS_DATABASE,
    TASK_TOOL_RECOMMENDATIONS,
    IMPLEMENTATION_COMPLEXITY_DATA,
    TASK_DECOMPOSITION,
    FAILURE_MODES,
    SALARY_BENCHMARKS,
    ROI_CALCULATIONS,
    FULLY_LOADED_MULTIPLIER,
)


def get_ai_tools(category: str = None, vendor: str = None) -> List[Dict[str, Any]]:
    """
    Get AI tools database with filtering.
    
    Args:
        category: Filter by tool category (e.g., "LLM_TEXT", "RPA_INTELLIGENT")
        vendor: Filter by vendor name
    
    Returns:
        List of AI tools with capabilities and pricing
    """
    tools = AI_TOOLS_DATABASE
    
    if category:
        tools = [t for t in tools if t["category"] == category]
    
    if vendor:
        tools = [t for t in tools if vendor.lower() in t["vendor"].lower()]
    
    return tools


def get_tool_recommendations(task_id: str = None) -> List[Dict[str, Any]]:
    """
    Get AI tool recommendations for tasks.
    The SECRET SAUCE - specific tool recommendations for each task.
    
    Args:
        task_id: Optional filter by task ID
    
    Returns:
        List of task-to-tool recommendations with architecture patterns
    """
    recommendations = TASK_TOOL_RECOMMENDATIONS
    
    if task_id:
        recommendations = [r for r in recommendations if r["task_id"] == task_id]
    
    # Enrich with full tool details
    result = []
    for rec in recommendations:
        enriched_tools = []
        for tool_rec in rec.get("recommended_tools", []):
            tool_id = tool_rec["tool_id"]
            tool_details = next((t for t in AI_TOOLS_DATABASE if t["tool_id"] == tool_id), None)
            if tool_details:
                enriched_tools.append({
                    **tool_rec,
                    "tool_name": tool_details["tool_name"],
                    "vendor": tool_details["vendor"],
                    "pricing_model": tool_details.get("pricing_model"),
                    "enterprise_ready": tool_details.get("enterprise_ready"),
                    "gdpr_compliant": tool_details.get("gdpr_compliant"),
                })
        
        result.append({
            **rec,
            "recommended_tools": enriched_tools,
        })
    
    return result


def get_implementation_complexity(task_id: str = None, complexity_level: str = None) -> List[Dict[str, Any]]:
    """
    Get implementation complexity data.
    Real-world difficulty scores, costs, and success rates.
    
    Args:
        task_id: Optional filter by task ID
        complexity_level: Optional filter by complexity (TRIVIAL, SIMPLE, MODERATE, COMPLEX, etc.)
    
    Returns:
        List of implementation complexity assessments
    """
    data = IMPLEMENTATION_COMPLEXITY_DATA
    
    if task_id:
        data = [d for d in data if d["task_id"] == task_id]
    
    if complexity_level:
        data = [d for d in data if d["complexity_level"] == complexity_level]
    
    return data


def get_task_decomposition(task_id: str = None) -> List[Dict[str, Any]]:
    """
    Get task decomposition trees.
    Breaks complex tasks into atomic automatable units.
    
    Args:
        task_id: Optional filter by parent task ID
    
    Returns:
        List of task decompositions with subtasks and automation potential
    """
    data = TASK_DECOMPOSITION
    
    if task_id:
        data = [d for d in data if d["parent_task_id"] == task_id]
    
    return data


def get_failure_modes(task_id: str = None) -> List[Dict[str, Any]]:
    """
    Get failure mode analysis.
    What breaks, how to detect it, and how to recover.
    
    Args:
        task_id: Optional filter by task ID
    
    Returns:
        List of failure mode analyses
    """
    data = FAILURE_MODES
    
    if task_id:
        data = [d for d in data if d["task_id"] == task_id]
    
    return data


def get_salary_benchmarks(region: str = "USA", occupation: str = None) -> Dict[str, Any]:
    """
    Get salary benchmarks by region and occupation.
    Essential for ROI calculations.
    
    Args:
        region: USA, Canada, or EU
        occupation: Optional filter by occupation title
    
    Returns:
        Salary data with fully-loaded cost multiplier
    """
    if region not in SALARY_BENCHMARKS:
        return {"error": f"Region not found. Available: {list(SALARY_BENCHMARKS.keys())}"}
    
    salaries = SALARY_BENCHMARKS[region]
    
    if occupation:
        if occupation in salaries:
            salary = salaries[occupation]
            return {
                "occupation": occupation,
                "region": region,
                "annual_salary": salary,
                "fully_loaded_cost": round(salary * FULLY_LOADED_MULTIPLIER),
                "multiplier": FULLY_LOADED_MULTIPLIER,
            }
        else:
            return {"error": f"Occupation not found in {region}"}
    
    # Return all with fully-loaded costs
    return {
        "region": region,
        "multiplier": FULLY_LOADED_MULTIPLIER,
        "salaries": [
            {
                "occupation": occ,
                "annual_salary": sal,
                "fully_loaded_cost": round(sal * FULLY_LOADED_MULTIPLIER),
            }
            for occ, sal in salaries.items()
        ]
    }


def get_roi_analysis(task_id: str = None, region: str = None) -> List[Dict[str, Any]]:
    """
    Get ROI analysis for automation investments.
    Complete business case with payback period and multi-year ROI.
    
    Args:
        task_id: Optional filter by task ID
        region: Optional filter by region
    
    Returns:
        List of ROI analyses
    """
    data = ROI_CALCULATIONS
    
    if task_id:
        data = [d for d in data if d["task_id"] == task_id]
    
    if region:
        data = [d for d in data if d["region"] == region]
    
    return data


def calculate_custom_roi(
    annual_salary: float,
    automation_percentage: float,
    implementation_cost: float,
    ongoing_annual_cost: float,
    region: str = "USA"
) -> Dict[str, Any]:
    """
    Calculate custom ROI for any automation scenario.
    
    Args:
        annual_salary: Base salary of role being automated
        automation_percentage: Percentage of role that can be automated (0.0-1.0)
        implementation_cost: One-time implementation cost
        ongoing_annual_cost: Annual licensing/maintenance cost
        region: Region for context
    
    Returns:
        Complete ROI analysis
    """
    fully_loaded = annual_salary * FULLY_LOADED_MULTIPLIER
    annual_savings = fully_loaded * automation_percentage
    net_savings_year1 = annual_savings - implementation_cost - ongoing_annual_cost
    net_savings_year2_plus = annual_savings - ongoing_annual_cost
    
    # Payback period
    if annual_savings - ongoing_annual_cost > 0:
        payback_months = implementation_cost / ((annual_savings - ongoing_annual_cost) / 12)
    else:
        payback_months = float('inf')
    
    # ROI calculations
    year_1_investment = implementation_cost + ongoing_annual_cost
    year_1_roi = ((annual_savings - year_1_investment) / year_1_investment) * 100 if year_1_investment > 0 else 0
    
    total_investment_3yr = implementation_cost + (ongoing_annual_cost * 3)
    total_savings_3yr = annual_savings * 3
    year_3_roi = ((total_savings_3yr - total_investment_3yr) / total_investment_3yr) * 100 if total_investment_3yr > 0 else 0
    
    return {
        "input": {
            "annual_salary": annual_salary,
            "automation_percentage": automation_percentage,
            "implementation_cost": implementation_cost,
            "ongoing_annual_cost": ongoing_annual_cost,
            "region": region,
        },
        "analysis": {
            "fully_loaded_cost": round(fully_loaded),
            "annual_labor_savings": round(annual_savings),
            "fte_equivalent_automated": automation_percentage,
            "payback_months": round(payback_months, 1) if payback_months != float('inf') else "Never",
            "net_savings_year_1": round(net_savings_year1),
            "net_savings_year_2": round(net_savings_year2_plus),
            "net_savings_year_3": round(net_savings_year2_plus),
            "cumulative_savings_3yr": round(net_savings_year1 + net_savings_year2_plus * 2),
            "year_1_roi_percentage": round(year_1_roi, 1),
            "year_3_roi_percentage": round(year_3_roi, 1),
        },
        "recommendation": _get_roi_recommendation(year_1_roi, payback_months),
    }


def _get_roi_recommendation(year_1_roi: float, payback_months: float) -> str:
    """Generate recommendation based on ROI metrics."""
    if payback_months == float('inf'):
        return "NOT RECOMMENDED - Automation costs exceed savings"
    elif payback_months <= 6:
        return "STRONGLY RECOMMENDED - Excellent ROI, quick payback"
    elif payback_months <= 12:
        return "RECOMMENDED - Good ROI, reasonable payback period"
    elif payback_months <= 24:
        return "CONSIDER - Moderate ROI, longer payback; evaluate strategic value"
    else:
        return "CAUTION - Long payback period; ensure strategic alignment"


def get_automation_blueprint(task_id: str) -> Dict[str, Any]:
    """
    Get complete automation blueprint for a task.
    Combines all proprietary data into actionable implementation plan.
    
    Args:
        task_id: Task ID to generate blueprint for
    
    Returns:
        Complete automation blueprint with tools, complexity, failure modes, and ROI
    """
    # Get all relevant data
    tool_recs = get_tool_recommendations(task_id)
    complexity = get_implementation_complexity(task_id)
    decomposition = get_task_decomposition(task_id)
    failures = get_failure_modes(task_id)
    roi = get_roi_analysis(task_id)
    
    if not tool_recs:
        return {"error": "No automation blueprint available for this task"}
    
    blueprint = {
        "task_id": task_id,
        "task_description": tool_recs[0].get("task_description", ""),
        "sections": {}
    }
    
    # Tool recommendations
    if tool_recs:
        blueprint["sections"]["recommended_tools"] = {
            "primary_tools": tool_recs[0].get("recommended_tools", []),
            "recommended_architecture": tool_recs[0].get("recommended_architecture"),
            "automation_confidence": tool_recs[0].get("automation_confidence"),
        }
    
    # Implementation complexity
    if complexity:
        blueprint["sections"]["implementation"] = {
            "complexity_level": complexity[0].get("complexity_level"),
            "estimated_weeks": complexity[0].get("estimated_implementation_weeks"),
            "estimated_cost_usd": complexity[0].get("estimated_cost_usd"),
            "required_roles": complexity[0].get("required_roles"),
            "technical_requirements": complexity[0].get("technical_requirements"),
            "common_blockers": complexity[0].get("common_blockers"),
            "industry_success_rate": complexity[0].get("success_rate_industry"),
        }
    
    # Task decomposition
    if decomposition:
        blueprint["sections"]["task_breakdown"] = {
            "atomic_subtasks": decomposition[0].get("atomic_subtasks"),
            "total_human_time_minutes": decomposition[0].get("total_human_time_minutes"),
            "total_automated_time_minutes": decomposition[0].get("total_automated_time_minutes"),
            "time_savings_percentage": decomposition[0].get("time_savings_percentage"),
            "bottleneck": decomposition[0].get("bottleneck_subtask"),
            "full_automation_blocker": decomposition[0].get("full_automation_blocker"),
        }
    
    # Failure modes
    if failures:
        blueprint["sections"]["risk_analysis"] = {
            "failure_modes": failures[0].get("failure_modes"),
            "overall_failure_rate": failures[0].get("overall_failure_rate"),
            "mean_time_to_recovery": failures[0].get("mean_time_to_recovery_minutes"),
            "recommended_sla": failures[0].get("recommended_sla"),
        }
    
    # ROI analysis
    if roi:
        blueprint["sections"]["business_case"] = {
            "annual_savings_usd": roi[0].get("annual_savings_usd"),
            "implementation_cost_usd": roi[0].get("implementation_cost_usd"),
            "ongoing_cost_annual_usd": roi[0].get("ongoing_cost_annual_usd"),
            "payback_months": roi[0].get("payback_months"),
            "year_1_roi_percentage": roi[0].get("year_1_roi"),
            "year_3_roi_percentage": roi[0].get("year_3_roi"),
        }
    
    return blueprint


def get_quick_wins(min_roi: float = 100, max_payback_months: float = 12) -> List[Dict[str, Any]]:
    """
    Get quick win automation opportunities.
    Tasks with high ROI and fast payback.
    
    Args:
        min_roi: Minimum Year 1 ROI percentage
        max_payback_months: Maximum payback period in months
    
    Returns:
        List of quick win opportunities ranked by ROI
    """
    quick_wins = []
    
    for roi in ROI_CALCULATIONS:
        if roi["year_1_roi"] >= min_roi and roi["payback_months"] <= max_payback_months:
            # Get tool recommendations
            tool_recs = get_tool_recommendations(roi["task_id"])
            
            quick_wins.append({
                "task_id": roi["task_id"],
                "task_description": roi["task_description"],
                "occupation": roi["occupation"],
                "payback_months": roi["payback_months"],
                "year_1_roi_percentage": roi["year_1_roi"],
                "annual_savings_usd": roi["annual_savings_usd"],
                "implementation_cost_usd": roi["implementation_cost_usd"],
                "recommended_tools": [t["tool_name"] for t in tool_recs[0]["recommended_tools"]] if tool_recs else [],
            })
    
    # Sort by ROI descending
    quick_wins.sort(key=lambda x: x["year_1_roi_percentage"], reverse=True)
    
    return quick_wins
