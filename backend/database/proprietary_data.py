"""
PROPRIETARY DATA LAYER - Competitive Moat
Data that no competitor has - makes the platform indispensable.

1. AI Tool-to-Task Mapping: Specific tools/vendors for each task
2. Implementation Complexity: Real-world difficulty scores
3. Task Decomposition: Atomic breakdown of complex tasks
4. Failure Modes: What breaks and mitigation strategies
5. ROI Calculator: Cost-benefit analysis data
6. Integration Patterns: System dependencies and APIs
7. Training Data Requirements: What's needed to train automation
"""
import uuid
from typing import Dict, List, Optional
from enum import Enum


# =============================================================================
# AI TOOL CAPABILITIES DATABASE
# Maps specific AI tools/vendors to task categories they can handle
# =============================================================================

class AIToolCategory(Enum):
    LLM_TEXT = "LLM Text Generation"
    LLM_REASONING = "LLM Reasoning/Analysis"
    LLM_CODE = "LLM Code Generation"
    COMPUTER_VISION = "Computer Vision"
    SPEECH_TO_TEXT = "Speech Recognition"
    TEXT_TO_SPEECH = "Text to Speech"
    RPA_BASIC = "Basic RPA"
    RPA_INTELLIGENT = "Intelligent RPA"
    DOCUMENT_AI = "Document Processing AI"
    CONVERSATIONAL_AI = "Conversational AI"
    PREDICTIVE_AI = "Predictive Analytics"
    AUTONOMOUS_SYSTEMS = "Autonomous Systems"


AI_TOOLS_DATABASE = [
    # LLM TEXT GENERATION
    {
        "tool_id": "tool-001",
        "tool_name": "OpenAI GPT-5.2",
        "vendor": "OpenAI",
        "category": "LLM_TEXT",
        "capabilities": ["text_generation", "summarization", "translation", "content_creation", "email_drafting"],
        "task_categories_supported": ["Documentation", "Reporting", "Communication", "Content Creation"],
        "api_endpoint": "api.openai.com/v1/chat/completions",
        "pricing_model": "per_token",
        "price_per_1k_tokens_input": 0.01,
        "price_per_1k_tokens_output": 0.03,
        "latency_ms_avg": 500,
        "accuracy_benchmark": 0.94,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": False,
    },
    {
        "tool_id": "tool-002",
        "tool_name": "Anthropic Claude Sonnet 4.5",
        "vendor": "Anthropic",
        "category": "LLM_REASONING",
        "capabilities": ["complex_reasoning", "legal_analysis", "financial_analysis", "research", "coding"],
        "task_categories_supported": ["Analysis", "Legal Analysis", "Research", "Quality Assurance"],
        "api_endpoint": "api.anthropic.com/v1/messages",
        "pricing_model": "per_token",
        "price_per_1k_tokens_input": 0.003,
        "price_per_1k_tokens_output": 0.015,
        "latency_ms_avg": 800,
        "accuracy_benchmark": 0.96,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": False,
    },
    {
        "tool_id": "tool-003",
        "tool_name": "Google Gemini 3 Pro",
        "vendor": "Google",
        "category": "LLM_TEXT",
        "capabilities": ["multimodal", "text_generation", "image_understanding", "data_analysis"],
        "task_categories_supported": ["Data Analysis", "Reporting", "Documentation", "Inspection"],
        "api_endpoint": "generativelanguage.googleapis.com/v1",
        "pricing_model": "per_token",
        "price_per_1k_tokens_input": 0.00125,
        "price_per_1k_tokens_output": 0.005,
        "latency_ms_avg": 600,
        "accuracy_benchmark": 0.93,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": True,
    },
    # RPA TOOLS
    {
        "tool_id": "tool-004",
        "tool_name": "UiPath Enterprise",
        "vendor": "UiPath",
        "category": "RPA_INTELLIGENT",
        "capabilities": ["screen_scraping", "data_entry", "form_filling", "file_management", "email_automation"],
        "task_categories_supported": ["Data Processing", "Data Entry", "Reconciliation", "Administration"],
        "api_endpoint": "cloud.uipath.com/api",
        "pricing_model": "per_robot_per_month",
        "price_per_robot_month": 420,
        "latency_ms_avg": 100,
        "accuracy_benchmark": 0.99,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": True,
    },
    {
        "tool_id": "tool-005",
        "tool_name": "Automation Anywhere A360",
        "vendor": "Automation Anywhere",
        "category": "RPA_INTELLIGENT",
        "capabilities": ["cognitive_automation", "document_processing", "workflow_automation"],
        "task_categories_supported": ["Data Processing", "Documentation", "Transaction Processing"],
        "api_endpoint": "community.cloud.automationanywhere.com",
        "pricing_model": "per_bot_hour",
        "price_per_bot_hour": 0.50,
        "latency_ms_avg": 150,
        "accuracy_benchmark": 0.98,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": True,
    },
    {
        "tool_id": "tool-006",
        "tool_name": "Microsoft Power Automate",
        "vendor": "Microsoft",
        "category": "RPA_BASIC",
        "capabilities": ["flow_automation", "connector_integrations", "approval_workflows"],
        "task_categories_supported": ["Administration", "Communication", "Data Entry"],
        "api_endpoint": "flow.microsoft.com/api",
        "pricing_model": "per_user_per_month",
        "price_per_user_month": 15,
        "latency_ms_avg": 200,
        "accuracy_benchmark": 0.97,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": True,
    },
    # DOCUMENT AI
    {
        "tool_id": "tool-007",
        "tool_name": "AWS Textract",
        "vendor": "Amazon",
        "category": "DOCUMENT_AI",
        "capabilities": ["ocr", "table_extraction", "form_extraction", "handwriting_recognition"],
        "task_categories_supported": ["Records Management", "Data Entry", "Documentation"],
        "api_endpoint": "textract.amazonaws.com",
        "pricing_model": "per_page",
        "price_per_page": 0.015,
        "latency_ms_avg": 2000,
        "accuracy_benchmark": 0.95,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": False,
    },
    {
        "tool_id": "tool-008",
        "tool_name": "Google Document AI",
        "vendor": "Google",
        "category": "DOCUMENT_AI",
        "capabilities": ["invoice_parsing", "receipt_parsing", "contract_analysis", "form_parsing"],
        "task_categories_supported": ["Medical Coding", "Reconciliation", "Data Entry"],
        "api_endpoint": "documentai.googleapis.com",
        "pricing_model": "per_page",
        "price_per_page": 0.01,
        "latency_ms_avg": 1500,
        "accuracy_benchmark": 0.96,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": True,
    },
    # CONVERSATIONAL AI
    {
        "tool_id": "tool-009",
        "tool_name": "Amazon Lex + Connect",
        "vendor": "Amazon",
        "category": "CONVERSATIONAL_AI",
        "capabilities": ["voice_bots", "chat_bots", "intent_recognition", "slot_filling"],
        "task_categories_supported": ["Communication", "Customer Service", "Interview"],
        "api_endpoint": "lex.amazonaws.com",
        "pricing_model": "per_request",
        "price_per_1k_requests": 0.75,
        "latency_ms_avg": 300,
        "accuracy_benchmark": 0.91,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": False,
    },
    {
        "tool_id": "tool-010",
        "tool_name": "Intercom Fin AI",
        "vendor": "Intercom",
        "category": "CONVERSATIONAL_AI",
        "capabilities": ["customer_support", "ticket_routing", "knowledge_base_qa"],
        "task_categories_supported": ["Communication", "Problem Resolution", "Customer Service"],
        "api_endpoint": "api.intercom.io",
        "pricing_model": "per_resolution",
        "price_per_resolution": 0.99,
        "latency_ms_avg": 400,
        "accuracy_benchmark": 0.88,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": False,
    },
    # COMPUTER VISION
    {
        "tool_id": "tool-011",
        "tool_name": "Landing AI Visual Inspection",
        "vendor": "Landing AI",
        "category": "COMPUTER_VISION",
        "capabilities": ["defect_detection", "quality_inspection", "anomaly_detection"],
        "task_categories_supported": ["Inspection", "Quality Assurance"],
        "api_endpoint": "api.landing.ai",
        "pricing_model": "per_image",
        "price_per_image": 0.005,
        "latency_ms_avg": 100,
        "accuracy_benchmark": 0.97,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": True,
    },
    {
        "tool_id": "tool-012",
        "tool_name": "Cognex ViDi",
        "vendor": "Cognex",
        "category": "COMPUTER_VISION",
        "capabilities": ["part_location", "assembly_verification", "character_recognition"],
        "task_categories_supported": ["Inspection", "Quality Assurance", "Manufacturing"],
        "api_endpoint": "on_premise_only",
        "pricing_model": "perpetual_license",
        "price_perpetual": 25000,
        "latency_ms_avg": 50,
        "accuracy_benchmark": 0.99,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": True,
    },
    # AUTONOMOUS SYSTEMS
    {
        "tool_id": "tool-013",
        "tool_name": "Waymo Driver",
        "vendor": "Waymo",
        "category": "AUTONOMOUS_SYSTEMS",
        "capabilities": ["autonomous_driving", "route_planning", "obstacle_avoidance"],
        "task_categories_supported": ["Vehicle Operation"],
        "api_endpoint": "partner_api_only",
        "pricing_model": "per_mile",
        "price_per_mile": 0.50,
        "latency_ms_avg": 10,
        "accuracy_benchmark": 0.9999,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": False,
    },
    {
        "tool_id": "tool-014",
        "tool_name": "TuSimple Autonomous Trucking",
        "vendor": "TuSimple",
        "category": "AUTONOMOUS_SYSTEMS",
        "capabilities": ["highway_driving", "platooning", "fuel_optimization"],
        "task_categories_supported": ["Vehicle Operation", "Transportation"],
        "api_endpoint": "partner_api_only",
        "pricing_model": "per_mile",
        "price_per_mile": 0.35,
        "latency_ms_avg": 10,
        "accuracy_benchmark": 0.999,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": False,
    },
    # PREDICTIVE AI
    {
        "tool_id": "tool-015",
        "tool_name": "DataRobot AutoML",
        "vendor": "DataRobot",
        "category": "PREDICTIVE_AI",
        "capabilities": ["time_series_forecasting", "classification", "regression", "anomaly_detection"],
        "task_categories_supported": ["Analysis", "Data Analysis", "Evaluation"],
        "api_endpoint": "app.datarobot.com/api/v2",
        "pricing_model": "per_prediction",
        "price_per_1k_predictions": 0.10,
        "latency_ms_avg": 50,
        "accuracy_benchmark": 0.92,
        "enterprise_ready": True,
        "soc2_compliant": True,
        "gdpr_compliant": True,
        "on_premise_available": True,
    },
]


# =============================================================================
# TASK-TO-TOOL MAPPING (The Secret Sauce)
# Specific recommendations for which tools work for which tasks
# =============================================================================

TASK_TOOL_RECOMMENDATIONS = [
    # DATA ENTRY TASKS -> RPA + Document AI
    {
        "task_id": "task-005",  # Enter data from source documents
        "task_description": "Enter data from source documents into computer database",
        "recommended_tools": [
            {
                "tool_id": "tool-004",  # UiPath
                "fit_score": 0.95,
                "use_case": "Automated keystroke and form filling",
                "estimated_accuracy": 0.99,
                "setup_hours": 40,
            },
            {
                "tool_id": "tool-007",  # AWS Textract
                "fit_score": 0.90,
                "use_case": "OCR for source document digitization",
                "estimated_accuracy": 0.95,
                "setup_hours": 20,
            },
        ],
        "recommended_architecture": "Textract for OCR -> UiPath for data entry -> Human review for exceptions",
        "automation_confidence": 0.95,
    },
    # CUSTOMER SERVICE -> Conversational AI + LLM
    {
        "task_id": "task-014",  # Answer customer inquiries
        "task_description": "Answer customer inquiries via phone, email, or chat",
        "recommended_tools": [
            {
                "tool_id": "tool-010",  # Intercom Fin
                "fit_score": 0.92,
                "use_case": "Tier 1 support automation",
                "estimated_accuracy": 0.88,
                "setup_hours": 80,
            },
            {
                "tool_id": "tool-001",  # GPT-5.2
                "fit_score": 0.88,
                "use_case": "Complex query resolution and email drafting",
                "estimated_accuracy": 0.90,
                "setup_hours": 60,
            },
        ],
        "recommended_architecture": "Intercom for routing + GPT-5.2 for complex queries -> Human escalation for edge cases",
        "automation_confidence": 0.85,
    },
    # LEGAL RESEARCH -> LLM
    {
        "task_id": "task-021",  # Legal research
        "task_description": "Conduct legal research using databases and case law",
        "recommended_tools": [
            {
                "tool_id": "tool-002",  # Claude Sonnet
                "fit_score": 0.94,
                "use_case": "Case law analysis and citation finding",
                "estimated_accuracy": 0.92,
                "setup_hours": 100,
            },
        ],
        "recommended_architecture": "Claude for research synthesis -> Human lawyer for verification and strategy",
        "automation_confidence": 0.80,
    },
    # QC INSPECTION -> Computer Vision
    {
        "task_id": "task-025",  # Visual inspection
        "task_description": "Visually inspect products for defects and quality standards",
        "recommended_tools": [
            {
                "tool_id": "tool-011",  # Landing AI
                "fit_score": 0.96,
                "use_case": "Automated defect detection on production line",
                "estimated_accuracy": 0.97,
                "setup_hours": 200,
            },
            {
                "tool_id": "tool-012",  # Cognex ViDi
                "fit_score": 0.98,
                "use_case": "High-speed inline inspection",
                "estimated_accuracy": 0.99,
                "setup_hours": 300,
            },
        ],
        "recommended_architecture": "CV model for primary inspection -> Human review for flagged items -> Continuous model retraining",
        "automation_confidence": 0.90,
    },
    # TRUCK DRIVING -> Autonomous Systems
    {
        "task_id": "task-027",  # Operate heavy vehicle
        "task_description": "Operate heavy commercial vehicle safely on highways",
        "recommended_tools": [
            {
                "tool_id": "tool-014",  # TuSimple
                "fit_score": 0.85,
                "use_case": "Highway autonomous trucking",
                "estimated_accuracy": 0.999,
                "setup_hours": 1000,
            },
        ],
        "recommended_architecture": "Autonomous for highway segments -> Human driver for first/last mile -> Remote monitoring",
        "automation_confidence": 0.70,
    },
    # FINANCIAL ANALYSIS -> LLM + Predictive
    {
        "task_id": "task-010",  # Analyze financial data
        "task_description": "Analyze financial data and market trends",
        "recommended_tools": [
            {
                "tool_id": "tool-002",  # Claude
                "fit_score": 0.90,
                "use_case": "Qualitative analysis and report generation",
                "estimated_accuracy": 0.88,
                "setup_hours": 80,
            },
            {
                "tool_id": "tool-015",  # DataRobot
                "fit_score": 0.92,
                "use_case": "Quantitative forecasting and trend analysis",
                "estimated_accuracy": 0.85,
                "setup_hours": 120,
            },
        ],
        "recommended_architecture": "DataRobot for quant models -> Claude for narrative insights -> Human analyst for judgment calls",
        "automation_confidence": 0.75,
    },
    # BOOKKEEPING -> RPA + Document AI
    {
        "task_id": "task-034",  # Record financial transactions
        "task_description": "Record financial transactions in accounting software",
        "recommended_tools": [
            {
                "tool_id": "tool-004",  # UiPath
                "fit_score": 0.98,
                "use_case": "Automated journal entry posting",
                "estimated_accuracy": 0.99,
                "setup_hours": 60,
            },
            {
                "tool_id": "tool-008",  # Google Document AI
                "fit_score": 0.95,
                "use_case": "Invoice and receipt parsing",
                "estimated_accuracy": 0.96,
                "setup_hours": 40,
            },
        ],
        "recommended_architecture": "Document AI for data extraction -> UiPath for ERP posting -> Monthly human reconciliation",
        "automation_confidence": 0.95,
    },
    # RESUME SCREENING -> LLM (with compliance warnings)
    {
        "task_id": "task-036",  # Screen resumes
        "task_description": "Screen resumes and applications for job requirements",
        "recommended_tools": [
            {
                "tool_id": "tool-001",  # GPT-5.2
                "fit_score": 0.85,
                "use_case": "Initial screening against job requirements",
                "estimated_accuracy": 0.82,
                "setup_hours": 60,
                "compliance_warning": "EU AI Act High-Risk - HITL mandatory, audit trail required",
            },
        ],
        "recommended_architecture": "LLM for initial scoring -> Human recruiter reviews all candidates -> Bias testing required",
        "automation_confidence": 0.50,  # Lower due to compliance
    },
    # GRADING -> LLM (with compliance warnings)
    {
        "task_id": "task-031",  # Grade assignments
        "task_description": "Grade student assignments and provide feedback",
        "recommended_tools": [
            {
                "tool_id": "tool-002",  # Claude
                "fit_score": 0.88,
                "use_case": "Essay scoring and feedback generation",
                "estimated_accuracy": 0.85,
                "setup_hours": 100,
                "compliance_warning": "EU AI Act High-Risk for educational outcomes - transparency required",
            },
        ],
        "recommended_architecture": "LLM for initial grading -> Teacher reviews flagged assignments -> Student appeal process",
        "automation_confidence": 0.60,
    },
]


# =============================================================================
# IMPLEMENTATION COMPLEXITY SCORES
# Real-world difficulty to actually implement automation
# =============================================================================

class ImplementationComplexity(Enum):
    TRIVIAL = "Trivial"           # < 1 week, < $5K
    SIMPLE = "Simple"             # 1-4 weeks, $5-25K
    MODERATE = "Moderate"         # 1-3 months, $25-100K
    COMPLEX = "Complex"           # 3-6 months, $100-500K
    VERY_COMPLEX = "Very Complex" # 6-12 months, $500K-2M
    TRANSFORMATIONAL = "Transformational"  # 12+ months, $2M+


IMPLEMENTATION_COMPLEXITY_DATA = [
    {
        "task_id": "task-005",  # Data entry
        "task_description": "Enter data from source documents into computer database",
        "complexity_level": "SIMPLE",
        "estimated_implementation_weeks": 3,
        "estimated_cost_usd": 15000,
        "required_roles": ["RPA Developer", "Business Analyst"],
        "technical_requirements": [
            "Source document standardization",
            "Target system API access",
            "Exception handling workflow",
        ],
        "common_blockers": [
            "Inconsistent source document formats",
            "Legacy system integration",
            "Change management resistance",
        ],
        "success_rate_industry": 0.85,
    },
    {
        "task_id": "task-014",  # Customer service
        "task_description": "Answer customer inquiries via phone, email, or chat",
        "complexity_level": "MODERATE",
        "estimated_implementation_weeks": 10,
        "estimated_cost_usd": 75000,
        "required_roles": ["ML Engineer", "Conversation Designer", "CX Analyst"],
        "technical_requirements": [
            "Knowledge base creation",
            "Intent classification training",
            "Integration with ticketing system",
            "Escalation routing logic",
        ],
        "common_blockers": [
            "Insufficient training data",
            "Edge case explosion",
            "Customer acceptance of AI",
        ],
        "success_rate_industry": 0.70,
    },
    {
        "task_id": "task-025",  # QC Inspection
        "task_description": "Visually inspect products for defects and quality standards",
        "complexity_level": "COMPLEX",
        "estimated_implementation_weeks": 20,
        "estimated_cost_usd": 250000,
        "required_roles": ["CV Engineer", "Manufacturing Engineer", "Data Scientist"],
        "technical_requirements": [
            "Labeled defect image dataset (10K+ images)",
            "Camera/lighting infrastructure",
            "Integration with PLC/SCADA",
            "Real-time inference pipeline",
        ],
        "common_blockers": [
            "Rare defect types (class imbalance)",
            "Environmental variation (lighting, position)",
            "Production line speed requirements",
        ],
        "success_rate_industry": 0.65,
    },
    {
        "task_id": "task-027",  # Truck driving
        "task_description": "Operate heavy commercial vehicle safely on highways",
        "complexity_level": "TRANSFORMATIONAL",
        "estimated_implementation_weeks": 104,  # 2 years
        "estimated_cost_usd": 5000000,
        "required_roles": ["Autonomous Systems Team", "Safety Engineers", "Fleet Management"],
        "technical_requirements": [
            "Vehicle retrofit or new fleet",
            "Regulatory approval per state/province",
            "Remote monitoring infrastructure",
            "Insurance and liability framework",
        ],
        "common_blockers": [
            "Regulatory uncertainty",
            "Public acceptance",
            "Edge case safety validation",
            "Weather/road condition limitations",
        ],
        "success_rate_industry": 0.30,
    },
    {
        "task_id": "task-034",  # Bookkeeping
        "task_description": "Record financial transactions in accounting software",
        "complexity_level": "SIMPLE",
        "estimated_implementation_weeks": 4,
        "estimated_cost_usd": 20000,
        "required_roles": ["RPA Developer", "Accountant (SME)"],
        "technical_requirements": [
            "ERP/accounting system API or UI automation",
            "Chart of accounts mapping",
            "Approval workflow integration",
        ],
        "common_blockers": [
            "Multi-currency complexity",
            "Audit trail requirements",
            "Exception handling volume",
        ],
        "success_rate_industry": 0.90,
    },
    {
        "task_id": "task-036",  # Resume screening
        "task_description": "Screen resumes and applications for job requirements",
        "complexity_level": "MODERATE",
        "estimated_implementation_weeks": 8,
        "estimated_cost_usd": 50000,
        "required_roles": ["ML Engineer", "HR Analyst", "Compliance Officer"],
        "technical_requirements": [
            "ATS integration",
            "Bias detection and mitigation",
            "Explainability for rejected candidates",
            "Audit logging for compliance",
        ],
        "common_blockers": [
            "Bias in training data",
            "EU AI Act compliance burden",
            "Candidate experience concerns",
        ],
        "success_rate_industry": 0.55,
    },
]


# =============================================================================
# TASK DECOMPOSITION TREES
# Breaking complex tasks into atomic automatable units
# =============================================================================

TASK_DECOMPOSITION = [
    {
        "parent_task_id": "task-010",  # Analyze financial data
        "parent_task_description": "Analyze financial data and market trends",
        "atomic_subtasks": [
            {
                "subtask_id": "task-010-a",
                "description": "Extract data from financial databases/APIs",
                "automation_potential": 0.98,
                "recommended_tool": "RPA + API connectors",
                "human_time_minutes": 30,
                "automated_time_minutes": 2,
            },
            {
                "subtask_id": "task-010-b",
                "description": "Clean and normalize financial data",
                "automation_potential": 0.95,
                "recommended_tool": "Python/Pandas scripts",
                "human_time_minutes": 60,
                "automated_time_minutes": 5,
            },
            {
                "subtask_id": "task-010-c",
                "description": "Calculate financial ratios and metrics",
                "automation_potential": 0.99,
                "recommended_tool": "Excel macros / Python",
                "human_time_minutes": 45,
                "automated_time_minutes": 1,
            },
            {
                "subtask_id": "task-010-d",
                "description": "Identify trends and anomalies",
                "automation_potential": 0.80,
                "recommended_tool": "DataRobot / Time-series models",
                "human_time_minutes": 90,
                "automated_time_minutes": 10,
            },
            {
                "subtask_id": "task-010-e",
                "description": "Generate narrative insights and recommendations",
                "automation_potential": 0.70,
                "recommended_tool": "Claude / GPT-5.2",
                "human_time_minutes": 120,
                "automated_time_minutes": 15,
            },
            {
                "subtask_id": "task-010-f",
                "description": "Validate conclusions and apply judgment",
                "automation_potential": 0.20,
                "recommended_tool": "Human analyst required",
                "human_time_minutes": 60,
                "automated_time_minutes": 60,  # Still needs human
            },
        ],
        "total_human_time_minutes": 405,
        "total_automated_time_minutes": 93,
        "time_savings_percentage": 77,
        "bottleneck_subtask": "task-010-f",
        "full_automation_blocker": "Judgment and accountability requirements",
    },
    {
        "parent_task_id": "task-014",  # Customer service
        "parent_task_description": "Answer customer inquiries via phone, email, or chat",
        "atomic_subtasks": [
            {
                "subtask_id": "task-014-a",
                "description": "Receive and route incoming inquiry",
                "automation_potential": 0.95,
                "recommended_tool": "IVR / Chatbot routing",
                "human_time_minutes": 2,
                "automated_time_minutes": 0.1,
            },
            {
                "subtask_id": "task-014-b",
                "description": "Identify customer and retrieve account info",
                "automation_potential": 0.98,
                "recommended_tool": "CRM API lookup",
                "human_time_minutes": 3,
                "automated_time_minutes": 0.5,
            },
            {
                "subtask_id": "task-014-c",
                "description": "Classify inquiry intent",
                "automation_potential": 0.90,
                "recommended_tool": "NLU intent classification",
                "human_time_minutes": 1,
                "automated_time_minutes": 0.2,
            },
            {
                "subtask_id": "task-014-d",
                "description": "Retrieve relevant knowledge base articles",
                "automation_potential": 0.92,
                "recommended_tool": "Semantic search / RAG",
                "human_time_minutes": 2,
                "automated_time_minutes": 0.5,
            },
            {
                "subtask_id": "task-014-e",
                "description": "Generate response to customer",
                "automation_potential": 0.85,
                "recommended_tool": "GPT-5.2 / Claude",
                "human_time_minutes": 5,
                "automated_time_minutes": 1,
            },
            {
                "subtask_id": "task-014-f",
                "description": "Handle complex/emotional situations",
                "automation_potential": 0.30,
                "recommended_tool": "Human agent required",
                "human_time_minutes": 10,
                "automated_time_minutes": 10,
            },
            {
                "subtask_id": "task-014-g",
                "description": "Log interaction and update CRM",
                "automation_potential": 0.98,
                "recommended_tool": "RPA / API integration",
                "human_time_minutes": 2,
                "automated_time_minutes": 0.1,
            },
        ],
        "total_human_time_minutes": 25,
        "total_automated_time_minutes": 12.4,
        "time_savings_percentage": 50,
        "bottleneck_subtask": "task-014-f",
        "full_automation_blocker": "Empathy and complex judgment in edge cases",
    },
    {
        "parent_task_id": "task-036",  # Resume screening
        "parent_task_description": "Screen resumes and applications for job requirements",
        "atomic_subtasks": [
            {
                "subtask_id": "task-036-a",
                "description": "Parse resume text and structure",
                "automation_potential": 0.95,
                "recommended_tool": "Document AI / Resume parsers",
                "human_time_minutes": 5,
                "automated_time_minutes": 0.2,
            },
            {
                "subtask_id": "task-036-b",
                "description": "Extract skills, experience, education",
                "automation_potential": 0.90,
                "recommended_tool": "NER models / LLM",
                "human_time_minutes": 10,
                "automated_time_minutes": 0.5,
            },
            {
                "subtask_id": "task-036-c",
                "description": "Match against job requirements",
                "automation_potential": 0.85,
                "recommended_tool": "Semantic matching / LLM",
                "human_time_minutes": 8,
                "automated_time_minutes": 1,
            },
            {
                "subtask_id": "task-036-d",
                "description": "Score and rank candidates",
                "automation_potential": 0.80,
                "recommended_tool": "ML ranking model",
                "human_time_minutes": 5,
                "automated_time_minutes": 0.3,
            },
            {
                "subtask_id": "task-036-e",
                "description": "Check for bias indicators",
                "automation_potential": 0.70,
                "recommended_tool": "Bias detection models",
                "human_time_minutes": 3,
                "automated_time_minutes": 0.5,
            },
            {
                "subtask_id": "task-036-f",
                "description": "Human review of borderline candidates",
                "automation_potential": 0.10,
                "recommended_tool": "Human recruiter (HITL)",
                "human_time_minutes": 15,
                "automated_time_minutes": 15,
                "compliance_note": "EU AI Act mandates human review for employment decisions",
            },
        ],
        "total_human_time_minutes": 46,
        "total_automated_time_minutes": 17.5,
        "time_savings_percentage": 62,
        "bottleneck_subtask": "task-036-f",
        "full_automation_blocker": "EU AI Act High-Risk classification requires HITL",
    },
]


# =============================================================================
# FAILURE MODE ANALYSIS
# What breaks and how to recover
# =============================================================================

FAILURE_MODES = [
    {
        "task_id": "task-005",  # Data entry
        "task_description": "Enter data from source documents into computer database",
        "failure_modes": [
            {
                "failure_type": "OCR_ERROR",
                "description": "Document AI fails to read handwritten or low-quality scans",
                "probability": 0.08,
                "impact_severity": "MEDIUM",
                "detection_method": "Confidence score threshold < 0.85",
                "mitigation": "Route to human review queue",
                "recovery_time_minutes": 5,
                "cost_per_failure_usd": 2.50,
            },
            {
                "failure_type": "SCHEMA_MISMATCH",
                "description": "Extracted fields don't map to target system schema",
                "probability": 0.05,
                "impact_severity": "HIGH",
                "detection_method": "Validation rule failures",
                "mitigation": "Exception workflow with field mapping UI",
                "recovery_time_minutes": 10,
                "cost_per_failure_usd": 8.00,
            },
            {
                "failure_type": "TARGET_SYSTEM_DOWN",
                "description": "ERP or target database unavailable",
                "probability": 0.02,
                "impact_severity": "CRITICAL",
                "detection_method": "API timeout or error response",
                "mitigation": "Queue entries for retry, alert operations",
                "recovery_time_minutes": 60,
                "cost_per_failure_usd": 50.00,
            },
        ],
        "overall_failure_rate": 0.15,
        "mean_time_to_recovery_minutes": 15,
        "recommended_sla": "99.5% success rate, 30-minute exception SLA",
    },
    {
        "task_id": "task-014",  # Customer service
        "task_description": "Answer customer inquiries via phone, email, or chat",
        "failure_modes": [
            {
                "failure_type": "INTENT_MISCLASSIFICATION",
                "description": "AI misunderstands customer intent",
                "probability": 0.12,
                "impact_severity": "MEDIUM",
                "detection_method": "Customer feedback, escalation rate",
                "mitigation": "Offer escalation to human agent",
                "recovery_time_minutes": 3,
                "cost_per_failure_usd": 5.00,
            },
            {
                "failure_type": "HALLUCINATION",
                "description": "AI provides incorrect information",
                "probability": 0.05,
                "impact_severity": "HIGH",
                "detection_method": "Grounding checks against knowledge base",
                "mitigation": "Restrict responses to verified KB content",
                "recovery_time_minutes": 5,
                "cost_per_failure_usd": 15.00,
            },
            {
                "failure_type": "EMOTIONAL_ESCALATION",
                "description": "Customer becomes frustrated with AI",
                "probability": 0.08,
                "impact_severity": "HIGH",
                "detection_method": "Sentiment analysis, repeated queries",
                "mitigation": "Immediate escalation to human with context",
                "recovery_time_minutes": 2,
                "cost_per_failure_usd": 10.00,
            },
        ],
        "overall_failure_rate": 0.25,
        "mean_time_to_recovery_minutes": 5,
        "recommended_sla": "85% first-contact resolution, <5 min escalation time",
    },
    {
        "task_id": "task-025",  # QC Inspection
        "task_description": "Visually inspect products for defects and quality standards",
        "failure_modes": [
            {
                "failure_type": "FALSE_NEGATIVE",
                "description": "Defective product passes inspection (CRITICAL)",
                "probability": 0.01,
                "impact_severity": "CRITICAL",
                "detection_method": "Downstream QC, customer complaints",
                "mitigation": "Lower confidence threshold, add human spot-checks",
                "recovery_time_minutes": 0,  # Product already shipped
                "cost_per_failure_usd": 5000.00,  # Recall/liability
            },
            {
                "failure_type": "FALSE_POSITIVE",
                "description": "Good product flagged as defective",
                "probability": 0.05,
                "impact_severity": "LOW",
                "detection_method": "Human review of rejects",
                "mitigation": "Second-pass human verification of rejects",
                "recovery_time_minutes": 2,
                "cost_per_failure_usd": 3.00,
            },
            {
                "failure_type": "ENVIRONMENTAL_DRIFT",
                "description": "Lighting/camera changes degrade accuracy",
                "probability": 0.03,
                "impact_severity": "MEDIUM",
                "detection_method": "Model confidence drift monitoring",
                "mitigation": "Automated recalibration, alert maintenance",
                "recovery_time_minutes": 30,
                "cost_per_failure_usd": 100.00,
            },
        ],
        "overall_failure_rate": 0.09,
        "mean_time_to_recovery_minutes": 10,
        "recommended_sla": "99.9% defect detection rate, <3% false positive rate",
    },
]


# =============================================================================
# ROI CALCULATOR DATA
# Salary benchmarks + implementation costs = business case
# =============================================================================

SALARY_BENCHMARKS = {
    # US annual salaries (median)
    "USA": {
        "Data Entry Keyer": 35000,
        "Customer Service Representative": 38000,
        "Bookkeeping Clerk": 45000,
        "Paralegal": 58000,
        "Quality Control Inspector": 42000,
        "Financial Analyst": 95000,
        "Software Developer": 120000,
        "Registered Nurse": 82000,
        "Loan Officer": 65000,
        "Heavy Truck Driver": 50000,
        "Cashier": 28000,
        "Recruiter": 55000,
        "Elementary School Teacher": 62000,
        "Lawyer": 145000,
        "Marketing Manager": 135000,
    },
    # Canada annual salaries (CAD)
    "Canada": {
        "Data Entry Keyer": 38000,
        "Customer Service Representative": 42000,
        "Bookkeeping Clerk": 48000,
        "Paralegal": 55000,
        "Quality Control Inspector": 45000,
        "Financial Analyst": 85000,
        "Software Developer": 95000,
        "Registered Nurse": 85000,
        "Loan Officer": 60000,
        "Heavy Truck Driver": 55000,
        "Cashier": 32000,
        "Recruiter": 58000,
        "Elementary School Teacher": 70000,
        "Lawyer": 130000,
        "Marketing Manager": 110000,
    },
    # EU annual salaries (EUR, average)
    "EU": {
        "Data Entry Keyer": 28000,
        "Customer Service Representative": 32000,
        "Bookkeeping Clerk": 38000,
        "Paralegal": 42000,
        "Quality Control Inspector": 35000,
        "Financial Analyst": 65000,
        "Software Developer": 70000,
        "Registered Nurse": 45000,
        "Loan Officer": 48000,
        "Heavy Truck Driver": 38000,
        "Cashier": 24000,
        "Recruiter": 45000,
        "Elementary School Teacher": 42000,
        "Lawyer": 95000,
        "Marketing Manager": 85000,
    },
}

# Fully-loaded cost multiplier (benefits, overhead, etc.)
FULLY_LOADED_MULTIPLIER = 1.35

ROI_CALCULATIONS = [
    {
        "task_id": "task-005",
        "task_description": "Data entry automation",
        "occupation": "Data Entry Keyer",
        "region": "USA",
        "annual_salary": 35000,
        "fully_loaded_cost": 47250,
        "automation_percentage": 0.85,  # 85% of task can be automated
        "fte_equivalent_automated": 0.85,
        "annual_savings_usd": 40163,
        "implementation_cost_usd": 15000,
        "ongoing_cost_annual_usd": 5000,  # Licensing + maintenance
        "payback_months": 4.5,
        "year_1_roi": 167,  # Percentage
        "year_3_roi": 445,
    },
    {
        "task_id": "task-014",
        "task_description": "Customer service automation",
        "occupation": "Customer Service Representative",
        "region": "USA",
        "annual_salary": 38000,
        "fully_loaded_cost": 51300,
        "automation_percentage": 0.50,  # 50% of inquiries handled by AI
        "fte_equivalent_automated": 0.50,
        "annual_savings_usd": 25650,
        "implementation_cost_usd": 75000,
        "ongoing_cost_annual_usd": 24000,  # AI tool licensing
        "payback_months": 46,
        "year_1_roi": -97,  # Negative first year
        "year_3_roi": 32,
    },
    {
        "task_id": "task-034",
        "task_description": "Bookkeeping automation",
        "occupation": "Bookkeeping Clerk",
        "region": "USA",
        "annual_salary": 45000,
        "fully_loaded_cost": 60750,
        "automation_percentage": 0.90,
        "fte_equivalent_automated": 0.90,
        "annual_savings_usd": 54675,
        "implementation_cost_usd": 20000,
        "ongoing_cost_annual_usd": 8000,
        "payback_months": 4.4,
        "year_1_roi": 133,
        "year_3_roi": 398,
    },
]
