"""
TIER 1 DATA: GAME-CHANGING INTELLIGENCE
Data that makes investors say "holy shit"

1. Automation Adoption Intelligence - Who's automating what, when
2. Skills Decay & Reskilling Pathways - Career transition economics
3. Regulatory Forecast Model - Predicted compliance changes
4. Labor Arbitrage Index - Wage trends driving automation urgency
5. Total Cost of Ownership - Hidden costs most miss
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from enum import Enum


# =============================================================================
# 1. AUTOMATION ADOPTION INTELLIGENCE
# Which companies automated what, adoption curves, competitive benchmarks
# =============================================================================

class CompanySize(Enum):
    STARTUP = "Startup (<50)"
    SMB = "SMB (50-500)"
    MID_MARKET = "Mid-Market (500-5000)"
    ENTERPRISE = "Enterprise (5000-50000)"
    MEGA = "Mega Corp (50000+)"


class AdoptionStage(Enum):
    NOT_STARTED = "Not Started"
    PILOTING = "Piloting"
    SCALING = "Scaling"
    MATURE = "Mature"
    OPTIMIZING = "Optimizing"


# Industry automation maturity benchmarks (% of companies at each stage)
INDUSTRY_AUTOMATION_MATURITY = {
    "Financial Services": {
        "overall_maturity_score": 72,
        "adoption_distribution": {
            "NOT_STARTED": 8,
            "PILOTING": 15,
            "SCALING": 25,
            "MATURE": 35,
            "OPTIMIZING": 17,
        },
        "top_automated_tasks": [
            {"task": "Transaction reconciliation", "adoption_rate": 0.85},
            {"task": "Fraud detection", "adoption_rate": 0.78},
            {"task": "Customer onboarding KYC", "adoption_rate": 0.72},
            {"task": "Report generation", "adoption_rate": 0.68},
            {"task": "Loan document processing", "adoption_rate": 0.65},
        ],
        "leaders": ["JPMorgan Chase", "Goldman Sachs", "Capital One"],
        "avg_time_to_scale_months": 14,
    },
    "Healthcare": {
        "overall_maturity_score": 45,
        "adoption_distribution": {
            "NOT_STARTED": 22,
            "PILOTING": 28,
            "SCALING": 25,
            "MATURE": 18,
            "OPTIMIZING": 7,
        },
        "top_automated_tasks": [
            {"task": "Medical coding (ICD-10)", "adoption_rate": 0.62},
            {"task": "Appointment scheduling", "adoption_rate": 0.58},
            {"task": "Insurance verification", "adoption_rate": 0.55},
            {"task": "Patient record updates", "adoption_rate": 0.48},
            {"task": "Prior authorization", "adoption_rate": 0.42},
        ],
        "leaders": ["Kaiser Permanente", "Cleveland Clinic", "Mayo Clinic"],
        "avg_time_to_scale_months": 22,
    },
    "Manufacturing": {
        "overall_maturity_score": 58,
        "adoption_distribution": {
            "NOT_STARTED": 15,
            "PILOTING": 22,
            "SCALING": 28,
            "MATURE": 25,
            "OPTIMIZING": 10,
        },
        "top_automated_tasks": [
            {"task": "Quality inspection (visual)", "adoption_rate": 0.72},
            {"task": "Inventory management", "adoption_rate": 0.68},
            {"task": "Predictive maintenance", "adoption_rate": 0.58},
            {"task": "Production scheduling", "adoption_rate": 0.52},
            {"task": "Supply chain optimization", "adoption_rate": 0.45},
        ],
        "leaders": ["Tesla", "Siemens", "Foxconn"],
        "avg_time_to_scale_months": 18,
    },
    "Retail": {
        "overall_maturity_score": 52,
        "adoption_distribution": {
            "NOT_STARTED": 18,
            "PILOTING": 25,
            "SCALING": 27,
            "MATURE": 22,
            "OPTIMIZING": 8,
        },
        "top_automated_tasks": [
            {"task": "Inventory replenishment", "adoption_rate": 0.75},
            {"task": "Customer service chatbots", "adoption_rate": 0.68},
            {"task": "Price optimization", "adoption_rate": 0.55},
            {"task": "Demand forecasting", "adoption_rate": 0.52},
            {"task": "Returns processing", "adoption_rate": 0.48},
        ],
        "leaders": ["Amazon", "Walmart", "Target"],
        "avg_time_to_scale_months": 12,
    },
    "Technology": {
        "overall_maturity_score": 78,
        "adoption_distribution": {
            "NOT_STARTED": 5,
            "PILOTING": 12,
            "SCALING": 22,
            "MATURE": 38,
            "OPTIMIZING": 23,
        },
        "top_automated_tasks": [
            {"task": "Code review assistance", "adoption_rate": 0.82},
            {"task": "Bug triage and routing", "adoption_rate": 0.78},
            {"task": "Documentation generation", "adoption_rate": 0.75},
            {"task": "Test case generation", "adoption_rate": 0.72},
            {"task": "Customer support (Tier 1)", "adoption_rate": 0.70},
        ],
        "leaders": ["Google", "Microsoft", "Meta"],
        "avg_time_to_scale_months": 8,
    },
    "Legal": {
        "overall_maturity_score": 38,
        "adoption_distribution": {
            "NOT_STARTED": 28,
            "PILOTING": 32,
            "SCALING": 22,
            "MATURE": 13,
            "OPTIMIZING": 5,
        },
        "top_automated_tasks": [
            {"task": "Document review (eDiscovery)", "adoption_rate": 0.65},
            {"task": "Contract analysis", "adoption_rate": 0.52},
            {"task": "Legal research", "adoption_rate": 0.48},
            {"task": "Due diligence", "adoption_rate": 0.38},
            {"task": "Billing and time tracking", "adoption_rate": 0.35},
        ],
        "leaders": ["Latham & Watkins", "Baker McKenzie", "DLA Piper"],
        "avg_time_to_scale_months": 24,
    },
    "Insurance": {
        "overall_maturity_score": 62,
        "adoption_distribution": {
            "NOT_STARTED": 12,
            "PILOTING": 20,
            "SCALING": 28,
            "MATURE": 28,
            "OPTIMIZING": 12,
        },
        "top_automated_tasks": [
            {"task": "Claims processing", "adoption_rate": 0.72},
            {"task": "Underwriting data extraction", "adoption_rate": 0.65},
            {"task": "Policy administration", "adoption_rate": 0.58},
            {"task": "Customer inquiry handling", "adoption_rate": 0.55},
            {"task": "Fraud detection", "adoption_rate": 0.52},
        ],
        "leaders": ["Lemonade", "Progressive", "Allstate"],
        "avg_time_to_scale_months": 16,
    },
    "Transportation & Logistics": {
        "overall_maturity_score": 55,
        "adoption_distribution": {
            "NOT_STARTED": 18,
            "PILOTING": 22,
            "SCALING": 28,
            "MATURE": 22,
            "OPTIMIZING": 10,
        },
        "top_automated_tasks": [
            {"task": "Route optimization", "adoption_rate": 0.78},
            {"task": "Shipment tracking updates", "adoption_rate": 0.72},
            {"task": "Warehouse picking", "adoption_rate": 0.58},
            {"task": "Load planning", "adoption_rate": 0.52},
            {"task": "Driver scheduling", "adoption_rate": 0.45},
        ],
        "leaders": ["UPS", "FedEx", "DHL"],
        "avg_time_to_scale_months": 15,
    },
}

# Time-to-adoption curves by company size (months to reach each stage)
ADOPTION_VELOCITY_BY_SIZE = {
    "STARTUP": {
        "pilot_to_scale_months": 3,
        "scale_to_mature_months": 6,
        "typical_blockers": ["Budget constraints", "Technical expertise gaps"],
        "success_rate": 0.72,
    },
    "SMB": {
        "pilot_to_scale_months": 6,
        "scale_to_mature_months": 12,
        "typical_blockers": ["Change management", "Integration complexity"],
        "success_rate": 0.65,
    },
    "MID_MARKET": {
        "pilot_to_scale_months": 9,
        "scale_to_mature_months": 18,
        "typical_blockers": ["Stakeholder alignment", "Legacy systems"],
        "success_rate": 0.58,
    },
    "ENTERPRISE": {
        "pilot_to_scale_months": 14,
        "scale_to_mature_months": 28,
        "typical_blockers": ["Governance/compliance", "Global rollout complexity"],
        "success_rate": 0.52,
    },
    "MEGA": {
        "pilot_to_scale_months": 20,
        "scale_to_mature_months": 40,
        "typical_blockers": ["Organizational inertia", "Union negotiations"],
        "success_rate": 0.45,
    },
}

# First-mover advantage windows (months until competitive advantage erodes)
FIRST_MOVER_WINDOWS = {
    "Data Entry Automation": {
        "window_months": 6,
        "current_adoption_rate": 0.75,
        "window_status": "CLOSING",
        "recommendation": "Automate immediately or lose competitive advantage",
    },
    "Customer Service AI": {
        "window_months": 18,
        "current_adoption_rate": 0.45,
        "window_status": "OPEN",
        "recommendation": "Strong first-mover opportunity, 18 months to differentiate",
    },
    "Legal Document Review": {
        "window_months": 24,
        "current_adoption_rate": 0.35,
        "window_status": "WIDE_OPEN",
        "recommendation": "Early adopters will gain significant cost advantage",
    },
    "Autonomous Vehicles": {
        "window_months": 60,
        "current_adoption_rate": 0.05,
        "window_status": "EMERGING",
        "recommendation": "Watch and prepare, too early for most companies",
    },
    "Quality Inspection CV": {
        "window_months": 12,
        "current_adoption_rate": 0.55,
        "window_status": "NARROWING",
        "recommendation": "Act within 12 months to maintain parity",
    },
    "Financial Analysis AI": {
        "window_months": 24,
        "current_adoption_rate": 0.30,
        "window_status": "OPEN",
        "recommendation": "Significant opportunity for differentiation",
    },
    "HR Resume Screening": {
        "window_months": 12,
        "current_adoption_rate": 0.48,
        "window_status": "NARROWING",
        "recommendation": "Implement soon, but watch compliance requirements",
    },
    "Predictive Maintenance": {
        "window_months": 18,
        "current_adoption_rate": 0.42,
        "window_status": "OPEN",
        "recommendation": "Good opportunity in manufacturing sector",
    },
}


# =============================================================================
# 2. SKILLS DECAY & RESKILLING PATHWAYS
# Skills half-life, career transitions, reskilling economics
# =============================================================================

SKILLS_DECAY_PREDICTIONS = {
    # Format: skill -> years of remaining market value
    "Data Entry": {
        "half_life_years": 2.3,
        "current_demand_trend": "DECLINING",
        "annual_decline_rate": 0.18,  # 18% YoY decline
        "automation_threat_level": "CRITICAL",
        "jobs_at_risk_usa": 1200000,
    },
    "Basic Bookkeeping": {
        "half_life_years": 3.5,
        "current_demand_trend": "DECLINING",
        "annual_decline_rate": 0.12,
        "automation_threat_level": "HIGH",
        "jobs_at_risk_usa": 850000,
    },
    "Customer Service (Tier 1)": {
        "half_life_years": 4.0,
        "current_demand_trend": "DECLINING",
        "annual_decline_rate": 0.10,
        "automation_threat_level": "HIGH",
        "jobs_at_risk_usa": 2100000,
    },
    "Paralegal Research": {
        "half_life_years": 5.5,
        "current_demand_trend": "STABLE",
        "annual_decline_rate": 0.08,
        "automation_threat_level": "MEDIUM",
        "jobs_at_risk_usa": 180000,
    },
    "Quality Inspection (Visual)": {
        "half_life_years": 4.5,
        "current_demand_trend": "DECLINING",
        "annual_decline_rate": 0.09,
        "automation_threat_level": "HIGH",
        "jobs_at_risk_usa": 420000,
    },
    "Truck Driving (Long-haul)": {
        "half_life_years": 8.0,
        "current_demand_trend": "STABLE",
        "annual_decline_rate": 0.05,
        "automation_threat_level": "MEDIUM",
        "jobs_at_risk_usa": 1800000,
    },
    "Financial Analysis": {
        "half_life_years": 7.0,
        "current_demand_trend": "TRANSFORMING",
        "annual_decline_rate": 0.03,
        "automation_threat_level": "LOW",
        "jobs_at_risk_usa": 95000,
    },
    "Software Development": {
        "half_life_years": 12.0,
        "current_demand_trend": "GROWING",
        "annual_decline_rate": -0.05,  # Growing
        "automation_threat_level": "LOW",
        "jobs_at_risk_usa": 0,  # Net job creation
    },
    "Nursing (Clinical)": {
        "half_life_years": 25.0,
        "current_demand_trend": "GROWING",
        "annual_decline_rate": -0.08,  # Growing
        "automation_threat_level": "VERY_LOW",
        "jobs_at_risk_usa": 0,
    },
    "Cashier": {
        "half_life_years": 3.0,
        "current_demand_trend": "DECLINING",
        "annual_decline_rate": 0.15,
        "automation_threat_level": "CRITICAL",
        "jobs_at_risk_usa": 1500000,
    },
}

# Reskilling pathways with economics
RESKILLING_PATHWAYS = [
    {
        "from_role": "Data Entry Clerk",
        "from_salary_usd": 35000,
        "to_role": "RPA Developer",
        "to_salary_usd": 85000,
        "salary_increase_pct": 143,
        "reskilling_cost_usd": 8000,
        "reskilling_duration_months": 6,
        "success_rate": 0.72,
        "required_training": [
            "UiPath certification ($500)",
            "Basic Python ($1000)",
            "Process analysis ($2000)",
            "Bootcamp/course ($4500)",
        ],
        "skills_to_acquire": ["UiPath Studio", "Python basics", "Process mapping", "SQL"],
        "job_market_demand": "HIGH",
        "roi_years_to_breakeven": 0.4,
    },
    {
        "from_role": "Customer Service Rep",
        "from_salary_usd": 38000,
        "to_role": "Customer Success Manager",
        "to_salary_usd": 72000,
        "salary_increase_pct": 89,
        "reskilling_cost_usd": 5000,
        "reskilling_duration_months": 4,
        "success_rate": 0.68,
        "required_training": [
            "CRM certification - Salesforce ($1500)",
            "Customer success methodology ($1500)",
            "Data analysis basics ($2000)",
        ],
        "skills_to_acquire": ["Salesforce", "Customer health scoring", "Churn analysis", "Account management"],
        "job_market_demand": "HIGH",
        "roi_years_to_breakeven": 0.3,
    },
    {
        "from_role": "Bookkeeper",
        "from_salary_usd": 45000,
        "to_role": "Financial Systems Analyst",
        "to_salary_usd": 78000,
        "salary_increase_pct": 73,
        "reskilling_cost_usd": 12000,
        "reskilling_duration_months": 9,
        "success_rate": 0.65,
        "required_training": [
            "ERP certification - SAP/Oracle ($5000)",
            "SQL and data analysis ($3000)",
            "Business intelligence tools ($2000)",
            "Process improvement ($2000)",
        ],
        "skills_to_acquire": ["SAP/Oracle", "SQL", "Power BI/Tableau", "Process optimization"],
        "job_market_demand": "MEDIUM",
        "roi_years_to_breakeven": 0.6,
    },
    {
        "from_role": "Paralegal",
        "from_salary_usd": 58000,
        "to_role": "Legal Operations Manager",
        "to_salary_usd": 95000,
        "salary_increase_pct": 64,
        "reskilling_cost_usd": 15000,
        "reskilling_duration_months": 12,
        "success_rate": 0.58,
        "required_training": [
            "Legal tech certification ($4000)",
            "Project management - PMP ($3500)",
            "Contract lifecycle management ($3500)",
            "Vendor management ($4000)",
        ],
        "skills_to_acquire": ["Legal tech platforms", "Project management", "CLM systems", "Vendor negotiation"],
        "job_market_demand": "HIGH",
        "roi_years_to_breakeven": 0.8,
    },
    {
        "from_role": "Quality Inspector",
        "from_salary_usd": 42000,
        "to_role": "Computer Vision Engineer",
        "to_salary_usd": 120000,
        "salary_increase_pct": 186,
        "reskilling_cost_usd": 25000,
        "reskilling_duration_months": 18,
        "success_rate": 0.45,
        "required_training": [
            "Python programming ($3000)",
            "Machine learning fundamentals ($5000)",
            "Computer vision specialization ($8000)",
            "Bootcamp/degree program ($9000)",
        ],
        "skills_to_acquire": ["Python", "TensorFlow/PyTorch", "OpenCV", "Deep learning"],
        "job_market_demand": "VERY_HIGH",
        "roi_years_to_breakeven": 0.5,
    },
    {
        "from_role": "Truck Driver",
        "from_salary_usd": 50000,
        "to_role": "Fleet Operations Manager",
        "to_salary_usd": 75000,
        "salary_increase_pct": 50,
        "reskilling_cost_usd": 10000,
        "reskilling_duration_months": 8,
        "success_rate": 0.62,
        "required_training": [
            "Fleet management software ($2500)",
            "Logistics optimization ($3000)",
            "DOT compliance certification ($1500)",
            "Leadership training ($3000)",
        ],
        "skills_to_acquire": ["TMS systems", "Route optimization", "Regulatory compliance", "Team management"],
        "job_market_demand": "MEDIUM",
        "roi_years_to_breakeven": 0.7,
    },
    {
        "from_role": "Cashier",
        "from_salary_usd": 28000,
        "to_role": "E-commerce Specialist",
        "to_salary_usd": 55000,
        "salary_increase_pct": 96,
        "reskilling_cost_usd": 6000,
        "reskilling_duration_months": 5,
        "success_rate": 0.70,
        "required_training": [
            "E-commerce platforms ($1500)",
            "Digital marketing basics ($2000)",
            "Analytics and reporting ($1500)",
            "Customer experience tools ($1000)",
        ],
        "skills_to_acquire": ["Shopify/WooCommerce", "Google Analytics", "Email marketing", "Inventory systems"],
        "job_market_demand": "HIGH",
        "roi_years_to_breakeven": 0.3,
    },
]

# Skills adjacency - what skills transfer and amplify
SKILLS_ADJACENCY_GRAPH = {
    "Data Entry": {
        "transferable_to": ["RPA Development", "Data Quality Analysis", "Process Documentation"],
        "transfer_efficiency": 0.6,
        "amplifying_skills": ["Excel advanced", "SQL basics", "Process thinking"],
    },
    "Customer Service": {
        "transferable_to": ["Sales", "Customer Success", "Training", "UX Research"],
        "transfer_efficiency": 0.7,
        "amplifying_skills": ["CRM tools", "Conflict resolution", "Product knowledge"],
    },
    "Bookkeeping": {
        "transferable_to": ["Financial Analysis", "Audit", "FP&A", "Systems Administration"],
        "transfer_efficiency": 0.75,
        "amplifying_skills": ["ERP systems", "Financial modeling", "Regulatory knowledge"],
    },
    "Quality Inspection": {
        "transferable_to": ["Quality Engineering", "Process Engineering", "Data Analysis"],
        "transfer_efficiency": 0.55,
        "amplifying_skills": ["Statistical analysis", "Root cause analysis", "Technical writing"],
    },
    "Legal Research": {
        "transferable_to": ["Compliance", "Legal Operations", "Contract Management", "Policy Analysis"],
        "transfer_efficiency": 0.8,
        "amplifying_skills": ["Legal tech", "Project management", "Data analysis"],
    },
}


# =============================================================================
# 3. REGULATORY FORECAST MODEL
# Predicted compliance changes by jurisdiction 2026-2030
# =============================================================================

REGULATORY_FORECAST = {
    "EU": {
        "jurisdiction": "European Union",
        "regulatory_body": "EU AI Office",
        "current_framework": "EU AI Act (2024)",
        "predicted_changes": [
            {
                "change_id": "EU-2026-001",
                "predicted_date": "2026-Q2",
                "probability": 0.95,
                "change_type": "ENFORCEMENT",
                "description": "Full enforcement of EU AI Act for high-risk AI systems",
                "affected_tasks": ["Credit scoring", "Recruitment screening", "Educational assessment"],
                "impact": "CRITICAL",
                "action_required": "Implement HITL, audit trails, transparency notices",
            },
            {
                "change_id": "EU-2026-002",
                "predicted_date": "2026-Q4",
                "probability": 0.75,
                "change_type": "EXPANSION",
                "description": "Extension of high-risk category to customer service AI",
                "affected_tasks": ["Customer service chatbots", "Complaint handling"],
                "impact": "HIGH",
                "action_required": "Prepare transparency mechanisms, human oversight protocols",
            },
            {
                "change_id": "EU-2027-001",
                "predicted_date": "2027-Q2",
                "probability": 0.65,
                "change_type": "NEW_REQUIREMENT",
                "description": "Mandatory AI impact assessments for all workplace automation",
                "affected_tasks": ["All workplace automation"],
                "impact": "MEDIUM",
                "action_required": "Document workforce impact, develop mitigation plans",
            },
            {
                "change_id": "EU-2028-001",
                "predicted_date": "2028-Q1",
                "probability": 0.55,
                "change_type": "EXPANSION",
                "description": "General-purpose AI models brought under stricter oversight",
                "affected_tasks": ["LLM-based automation", "Foundation model deployments"],
                "impact": "HIGH",
                "action_required": "Vendor compliance verification, usage documentation",
            },
        ],
        "overall_regulatory_trajectory": "TIGHTENING",
        "compliance_cost_trend": "INCREASING",
    },
    "USA-Federal": {
        "jurisdiction": "United States (Federal)",
        "regulatory_body": "Multiple (FTC, EEOC, CFPB, SEC)",
        "current_framework": "Fragmented sectoral regulation",
        "predicted_changes": [
            {
                "change_id": "US-2026-001",
                "predicted_date": "2026-Q3",
                "probability": 0.70,
                "change_type": "NEW_REQUIREMENT",
                "description": "FTC enforcement action against deceptive AI practices",
                "affected_tasks": ["Customer-facing AI", "Marketing automation"],
                "impact": "MEDIUM",
                "action_required": "Clear AI disclosure, accuracy claims substantiation",
            },
            {
                "change_id": "US-2027-001",
                "predicted_date": "2027-Q1",
                "probability": 0.60,
                "change_type": "NEW_FRAMEWORK",
                "description": "EEOC guidelines on AI in hiring becoming enforceable",
                "affected_tasks": ["Resume screening", "Interview scheduling", "Candidate scoring"],
                "impact": "HIGH",
                "action_required": "Bias testing, adverse impact analysis, human review protocols",
            },
            {
                "change_id": "US-2027-002",
                "predicted_date": "2027-Q3",
                "probability": 0.50,
                "change_type": "LEGISLATION",
                "description": "Federal AI accountability legislation (if passed)",
                "affected_tasks": ["High-stakes decisions", "Critical infrastructure"],
                "impact": "HIGH",
                "action_required": "Monitor legislative progress, prepare compliance program",
            },
        ],
        "overall_regulatory_trajectory": "GRADUALLY_TIGHTENING",
        "compliance_cost_trend": "STABLE_TO_INCREASING",
    },
    "Canada-Federal": {
        "jurisdiction": "Canada (Federal)",
        "regulatory_body": "ISED, Privacy Commissioner",
        "current_framework": "AIDA (proposed), PIPEDA",
        "predicted_changes": [
            {
                "change_id": "CA-2026-001",
                "predicted_date": "2026-Q2",
                "probability": 0.80,
                "change_type": "NEW_FRAMEWORK",
                "description": "Artificial Intelligence and Data Act (AIDA) passage",
                "affected_tasks": ["High-impact AI systems", "Automated decision-making"],
                "impact": "HIGH",
                "action_required": "Impact assessments, transparency requirements, human oversight",
            },
            {
                "change_id": "CA-2027-001",
                "predicted_date": "2027-Q1",
                "probability": 0.65,
                "change_type": "ENFORCEMENT",
                "description": "First AIDA enforcement actions",
                "affected_tasks": ["Consumer-facing AI", "Employment decisions"],
                "impact": "MEDIUM",
                "action_required": "Compliance audit, documentation review",
            },
        ],
        "overall_regulatory_trajectory": "TIGHTENING",
        "compliance_cost_trend": "INCREASING",
    },
    "Quebec": {
        "jurisdiction": "Quebec, Canada",
        "regulatory_body": "CAI, OIQ, Professional Orders",
        "current_framework": "Law 25 (2023), Professional Acts",
        "predicted_changes": [
            {
                "change_id": "QC-2026-001",
                "predicted_date": "2026-Q1",
                "probability": 0.90,
                "change_type": "ENFORCEMENT",
                "description": "Full Law 25 enforcement with penalties",
                "affected_tasks": ["Any AI processing personal information"],
                "impact": "HIGH",
                "action_required": "Privacy impact assessments, consent mechanisms, transparency",
            },
            {
                "change_id": "QC-2026-002",
                "predicted_date": "2026-Q3",
                "probability": 0.70,
                "change_type": "NEW_REQUIREMENT",
                "description": "OIQ guidelines on AI in engineering decisions",
                "affected_tasks": ["Engineering automation", "Safety-critical systems"],
                "impact": "CRITICAL",
                "action_required": "P.Eng oversight requirements, documentation standards",
            },
            {
                "change_id": "QC-2027-001",
                "predicted_date": "2027-Q2",
                "probability": 0.60,
                "change_type": "EXPANSION",
                "description": "Extended automated decision-making disclosure requirements",
                "affected_tasks": ["HR decisions", "Credit decisions", "Insurance underwriting"],
                "impact": "MEDIUM",
                "action_required": "Explainability mechanisms, appeal processes",
            },
        ],
        "overall_regulatory_trajectory": "STRICT",
        "compliance_cost_trend": "HIGH",
    },
    "UK": {
        "jurisdiction": "United Kingdom",
        "regulatory_body": "ICO, FCA, sector regulators",
        "current_framework": "Pro-innovation, principles-based",
        "predicted_changes": [
            {
                "change_id": "UK-2026-001",
                "predicted_date": "2026-Q4",
                "probability": 0.65,
                "change_type": "NEW_FRAMEWORK",
                "description": "AI Safety Institute enforcement powers",
                "affected_tasks": ["Frontier AI models", "Critical infrastructure AI"],
                "impact": "MEDIUM",
                "action_required": "Safety testing, incident reporting",
            },
        ],
        "overall_regulatory_trajectory": "MODERATE",
        "compliance_cost_trend": "STABLE",
    },
}

# Compliance risk score by task type
COMPLIANCE_RISK_SCORES = {
    "Resume Screening": {
        "current_risk_score": 78,
        "predicted_2027_score": 92,
        "risk_trend": "INCREASING",
        "key_risks": ["Bias/discrimination", "EEOC scrutiny", "EU AI Act High-Risk"],
        "mitigation_cost_usd": 50000,
    },
    "Credit Scoring": {
        "current_risk_score": 85,
        "predicted_2027_score": 95,
        "risk_trend": "INCREASING",
        "key_risks": ["Fair lending laws", "EU AI Act High-Risk", "Explainability requirements"],
        "mitigation_cost_usd": 150000,
    },
    "Customer Service Chatbot": {
        "current_risk_score": 45,
        "predicted_2027_score": 65,
        "risk_trend": "INCREASING",
        "key_risks": ["Transparency disclosure", "Misinformation liability", "Consumer protection"],
        "mitigation_cost_usd": 25000,
    },
    "Data Entry Automation": {
        "current_risk_score": 15,
        "predicted_2027_score": 20,
        "risk_trend": "STABLE",
        "key_risks": ["Data accuracy", "Privacy (if PII)"],
        "mitigation_cost_usd": 5000,
    },
    "Quality Inspection": {
        "current_risk_score": 35,
        "predicted_2027_score": 45,
        "risk_trend": "SLIGHTLY_INCREASING",
        "key_risks": ["Product liability", "Safety certifications"],
        "mitigation_cost_usd": 30000,
    },
    "Medical Diagnosis Support": {
        "current_risk_score": 90,
        "predicted_2027_score": 95,
        "risk_trend": "STABLE_HIGH",
        "key_risks": ["FDA regulation", "Malpractice liability", "HIPAA"],
        "mitigation_cost_usd": 500000,
    },
    "Autonomous Vehicles": {
        "current_risk_score": 95,
        "predicted_2027_score": 85,
        "risk_trend": "DECREASING",
        "key_risks": ["Safety certification", "Liability frameworks", "Insurance"],
        "mitigation_cost_usd": 10000000,
    },
}


# =============================================================================
# 4. LABOR ARBITRAGE INDEX
# Real-time wage trends driving automation urgency
# =============================================================================

LABOR_ARBITRAGE_INDEX = {
    # Tracks wage inflation and automation ROI changes
    "Data Entry Clerk": {
        "current_wage_usd": 35000,
        "wage_growth_yoy": 0.04,  # 4% annual growth
        "wage_growth_5yr_cagr": 0.035,
        "automation_cost_trend": "DECREASING",
        "automation_cost_change_yoy": -0.15,  # 15% cheaper each year
        "arbitrage_score": 92,  # 0-100, higher = more urgent to automate
        "arbitrage_trend": "WIDENING",
        "breakeven_shift_months": -8,  # ROI breakeven getting 8 months faster per year
        "automate_now_urgency": "CRITICAL",
        "projected_labor_shortage": True,
    },
    "Customer Service Rep": {
        "current_wage_usd": 42000,
        "wage_growth_yoy": 0.05,
        "wage_growth_5yr_cagr": 0.045,
        "automation_cost_trend": "DECREASING",
        "automation_cost_change_yoy": -0.20,
        "arbitrage_score": 85,
        "arbitrage_trend": "WIDENING",
        "breakeven_shift_months": -6,
        "automate_now_urgency": "HIGH",
        "projected_labor_shortage": True,
    },
    "Truck Driver": {
        "current_wage_usd": 55000,
        "wage_growth_yoy": 0.08,  # High due to shortage
        "wage_growth_5yr_cagr": 0.07,
        "automation_cost_trend": "DECREASING",
        "automation_cost_change_yoy": -0.10,
        "arbitrage_score": 78,
        "arbitrage_trend": "WIDENING",
        "breakeven_shift_months": -4,
        "automate_now_urgency": "MEDIUM",
        "projected_labor_shortage": True,
    },
    "Registered Nurse": {
        "current_wage_usd": 85000,
        "wage_growth_yoy": 0.06,
        "wage_growth_5yr_cagr": 0.055,
        "automation_cost_trend": "STABLE",
        "automation_cost_change_yoy": -0.05,
        "arbitrage_score": 25,
        "arbitrage_trend": "STABLE",
        "breakeven_shift_months": -1,
        "automate_now_urgency": "LOW",
        "projected_labor_shortage": True,
    },
    "Software Developer": {
        "current_wage_usd": 125000,
        "wage_growth_yoy": 0.03,
        "wage_growth_5yr_cagr": 0.04,
        "automation_cost_trend": "DECREASING",
        "automation_cost_change_yoy": -0.25,
        "arbitrage_score": 55,
        "arbitrage_trend": "WIDENING",
        "breakeven_shift_months": -3,
        "automate_now_urgency": "MEDIUM",
        "projected_labor_shortage": False,
    },
    "Financial Analyst": {
        "current_wage_usd": 95000,
        "wage_growth_yoy": 0.04,
        "wage_growth_5yr_cagr": 0.038,
        "automation_cost_trend": "DECREASING",
        "automation_cost_change_yoy": -0.18,
        "arbitrage_score": 68,
        "arbitrage_trend": "WIDENING",
        "breakeven_shift_months": -5,
        "automate_now_urgency": "MEDIUM",
        "projected_labor_shortage": False,
    },
    "Paralegal": {
        "current_wage_usd": 60000,
        "wage_growth_yoy": 0.03,
        "wage_growth_5yr_cagr": 0.028,
        "automation_cost_trend": "DECREASING",
        "automation_cost_change_yoy": -0.22,
        "arbitrage_score": 75,
        "arbitrage_trend": "WIDENING",
        "breakeven_shift_months": -7,
        "automate_now_urgency": "HIGH",
        "projected_labor_shortage": False,
    },
    "Quality Inspector": {
        "current_wage_usd": 45000,
        "wage_growth_yoy": 0.04,
        "wage_growth_5yr_cagr": 0.035,
        "automation_cost_trend": "DECREASING",
        "automation_cost_change_yoy": -0.12,
        "arbitrage_score": 72,
        "arbitrage_trend": "WIDENING",
        "breakeven_shift_months": -4,
        "automate_now_urgency": "MEDIUM",
        "projected_labor_shortage": True,
    },
    "Bookkeeper": {
        "current_wage_usd": 48000,
        "wage_growth_yoy": 0.03,
        "wage_growth_5yr_cagr": 0.025,
        "automation_cost_trend": "DECREASING",
        "automation_cost_change_yoy": -0.18,
        "arbitrage_score": 88,
        "arbitrage_trend": "WIDENING",
        "breakeven_shift_months": -9,
        "automate_now_urgency": "CRITICAL",
        "projected_labor_shortage": False,
    },
}

# Geographic wage differentials (automation ROI varies by location)
GEOGRAPHIC_WAGE_INDEX = {
    "San Francisco": {"wage_multiplier": 1.45, "automation_urgency_boost": 15},
    "New York": {"wage_multiplier": 1.35, "automation_urgency_boost": 12},
    "Seattle": {"wage_multiplier": 1.30, "automation_urgency_boost": 10},
    "Boston": {"wage_multiplier": 1.25, "automation_urgency_boost": 8},
    "Austin": {"wage_multiplier": 1.10, "automation_urgency_boost": 5},
    "Denver": {"wage_multiplier": 1.08, "automation_urgency_boost": 4},
    "Chicago": {"wage_multiplier": 1.05, "automation_urgency_boost": 3},
    "Dallas": {"wage_multiplier": 1.00, "automation_urgency_boost": 0},
    "Phoenix": {"wage_multiplier": 0.95, "automation_urgency_boost": -2},
    "Detroit": {"wage_multiplier": 0.90, "automation_urgency_boost": -5},
    "Rural Midwest": {"wage_multiplier": 0.75, "automation_urgency_boost": -10},
    # International
    "Toronto": {"wage_multiplier": 1.15, "automation_urgency_boost": 6},
    "Vancouver": {"wage_multiplier": 1.20, "automation_urgency_boost": 8},
    "London": {"wage_multiplier": 1.40, "automation_urgency_boost": 14},
    "Frankfurt": {"wage_multiplier": 1.25, "automation_urgency_boost": 8},
    "Singapore": {"wage_multiplier": 1.30, "automation_urgency_boost": 10},
}


# =============================================================================
# 5. TOTAL COST OF OWNERSHIP (TCO) DATABASE
# Hidden costs most companies miss
# =============================================================================

TCO_HIDDEN_COSTS = {
    "Data Entry Automation": {
        "visible_costs": {
            "software_licensing": 15000,
            "implementation_services": 25000,
            "hardware": 0,
        },
        "hidden_costs": {
            "data_preparation_cleanup": 8000,
            "exception_handling_design": 12000,
            "user_training": 5000,
            "change_management": 8000,
            "parallel_running_period": 6000,
            "documentation": 3000,
            "security_review": 4000,
            "ongoing_maintenance_year1": 8000,
            "model_drift_retraining": 0,
        },
        "total_visible": 40000,
        "total_hidden": 54000,
        "hidden_cost_multiplier": 1.35,
        "total_tco_year1": 94000,
        "common_budget_overruns": [
            {"item": "Data quality issues", "typical_overrun_pct": 40},
            {"item": "Edge case handling", "typical_overrun_pct": 25},
            {"item": "Integration complexity", "typical_overrun_pct": 30},
        ],
    },
    "Customer Service AI": {
        "visible_costs": {
            "software_licensing": 48000,
            "implementation_services": 75000,
            "hardware": 0,
        },
        "hidden_costs": {
            "knowledge_base_creation": 35000,
            "intent_training_data": 20000,
            "conversation_design": 25000,
            "user_training": 10000,
            "change_management": 15000,
            "parallel_running_period": 20000,
            "documentation": 8000,
            "security_review": 6000,
            "ongoing_maintenance_year1": 24000,
            "model_drift_retraining": 15000,
        },
        "total_visible": 123000,
        "total_hidden": 178000,
        "hidden_cost_multiplier": 1.45,
        "total_tco_year1": 301000,
        "common_budget_overruns": [
            {"item": "Knowledge base gaps", "typical_overrun_pct": 50},
            {"item": "Edge case explosion", "typical_overrun_pct": 60},
            {"item": "Customer acceptance testing", "typical_overrun_pct": 35},
        ],
    },
    "Quality Inspection CV": {
        "visible_costs": {
            "software_licensing": 35000,
            "implementation_services": 120000,
            "hardware": 45000,
        },
        "hidden_costs": {
            "training_data_labeling": 40000,
            "camera_lighting_setup": 25000,
            "production_line_integration": 35000,
            "user_training": 15000,
            "change_management": 20000,
            "parallel_running_period": 30000,
            "documentation": 10000,
            "security_review": 8000,
            "ongoing_maintenance_year1": 25000,
            "model_drift_retraining": 20000,
        },
        "total_visible": 200000,
        "total_hidden": 228000,
        "hidden_cost_multiplier": 1.14,
        "total_tco_year1": 428000,
        "common_budget_overruns": [
            {"item": "Defect variety underestimated", "typical_overrun_pct": 45},
            {"item": "Environmental variation", "typical_overrun_pct": 35},
            {"item": "Production speed requirements", "typical_overrun_pct": 25},
        ],
    },
    "Legal Document Review": {
        "visible_costs": {
            "software_licensing": 60000,
            "implementation_services": 80000,
            "hardware": 0,
        },
        "hidden_costs": {
            "training_data_preparation": 45000,
            "legal_sme_time": 50000,
            "validation_sampling": 25000,
            "user_training": 20000,
            "change_management": 30000,
            "parallel_running_period": 40000,
            "documentation": 15000,
            "security_review": 12000,
            "ongoing_maintenance_year1": 30000,
            "model_drift_retraining": 25000,
        },
        "total_visible": 140000,
        "total_hidden": 292000,
        "hidden_cost_multiplier": 2.09,
        "total_tco_year1": 432000,
        "common_budget_overruns": [
            {"item": "Legal nuance handling", "typical_overrun_pct": 55},
            {"item": "Jurisdiction variations", "typical_overrun_pct": 40},
            {"item": "Partner firm integration", "typical_overrun_pct": 30},
        ],
    },
    "HR Resume Screening": {
        "visible_costs": {
            "software_licensing": 25000,
            "implementation_services": 40000,
            "hardware": 0,
        },
        "hidden_costs": {
            "bias_testing_mitigation": 35000,
            "compliance_documentation": 20000,
            "ats_integration": 15000,
            "user_training": 8000,
            "change_management": 12000,
            "parallel_running_period": 15000,
            "documentation": 8000,
            "security_review": 6000,
            "ongoing_maintenance_year1": 15000,
            "model_drift_retraining": 10000,
        },
        "total_visible": 65000,
        "total_hidden": 144000,
        "hidden_cost_multiplier": 2.22,
        "total_tco_year1": 209000,
        "common_budget_overruns": [
            {"item": "Bias detection/mitigation", "typical_overrun_pct": 70},
            {"item": "Regulatory compliance", "typical_overrun_pct": 50},
            {"item": "Candidate experience issues", "typical_overrun_pct": 35},
        ],
    },
}

# Maintenance burden estimates (Year 2-5 costs as % of Year 1)
MAINTENANCE_BURDEN = {
    "RPA_BASIC": {"year2_pct": 0.15, "year3_pct": 0.12, "year4_pct": 0.10, "year5_pct": 0.10},
    "RPA_INTELLIGENT": {"year2_pct": 0.20, "year3_pct": 0.18, "year4_pct": 0.15, "year5_pct": 0.15},
    "LLM_BASED": {"year2_pct": 0.25, "year3_pct": 0.22, "year4_pct": 0.20, "year5_pct": 0.18},
    "COMPUTER_VISION": {"year2_pct": 0.22, "year3_pct": 0.20, "year4_pct": 0.18, "year5_pct": 0.15},
    "AUTONOMOUS": {"year2_pct": 0.30, "year3_pct": 0.28, "year4_pct": 0.25, "year5_pct": 0.22},
}

# Vendor lock-in risk and switching costs
VENDOR_LOCK_IN_RISK = {
    "UiPath": {
        "lock_in_score": 65,
        "switching_cost_pct": 0.40,  # 40% of implementation cost to switch
        "data_portability": "MEDIUM",
        "alternative_vendors": ["Automation Anywhere", "Blue Prism", "Power Automate"],
    },
    "OpenAI": {
        "lock_in_score": 45,
        "switching_cost_pct": 0.25,
        "data_portability": "HIGH",
        "alternative_vendors": ["Anthropic", "Google", "Cohere"],
    },
    "Salesforce": {
        "lock_in_score": 85,
        "switching_cost_pct": 0.70,
        "data_portability": "LOW",
        "alternative_vendors": ["HubSpot", "Microsoft Dynamics", "Zoho"],
    },
    "SAP": {
        "lock_in_score": 90,
        "switching_cost_pct": 0.85,
        "data_portability": "VERY_LOW",
        "alternative_vendors": ["Oracle", "Microsoft Dynamics", "Workday"],
    },
    "AWS": {
        "lock_in_score": 70,
        "switching_cost_pct": 0.50,
        "data_portability": "MEDIUM",
        "alternative_vendors": ["Google Cloud", "Azure", "On-premise"],
    },
}
