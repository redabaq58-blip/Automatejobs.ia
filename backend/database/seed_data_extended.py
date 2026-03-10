"""
Extended seed data - Part 2
Additional occupations, tasks, compliance rules, and Frey-Osborne automation baselines.
Covers: Legal, Manufacturing, Education, Retail, Transportation sectors.
"""
import uuid

# =============================================================================
# FREY-OSBORNE AUTOMATION PROBABILITIES (2013 Study + Updates)
# Source: "The Future of Employment" - Oxford Martin School
# =============================================================================

FREY_OSBORNE_BASELINES = {
    # Format: "onet_code": probability (0.0-1.0)
    # Tech - Generally lower automation risk
    "15-1252.00": 0.042,   # Software Developer - 4.2%
    "15-2051.00": 0.015,   # Data Scientist - 1.5%
    "15-1242.00": 0.033,   # Database Administrator - 3.3%
    "15-1212.00": 0.021,   # Cybersecurity Analyst - 2.1%
    
    # Healthcare - Mixed
    "29-1141.00": 0.009,   # Registered Nurse - 0.9%
    "29-2072.00": 0.918,   # Medical Records Specialist - 91.8%
    "29-1051.00": 0.012,   # Pharmacist - 1.2%
    "29-2061.00": 0.081,   # Licensed Practical Nurse - 8.1%
    "31-9092.00": 0.803,   # Medical Assistants - 80.3%
    
    # Finance - High automation in routine tasks
    "13-2051.00": 0.230,   # Financial Analyst - 23%
    "13-2011.00": 0.940,   # Accountant (routine) - 94%
    "13-2072.00": 0.980,   # Loan Officer - 98%
    "43-3031.00": 0.976,   # Bookkeeping Clerk - 97.6%
    "13-2052.00": 0.058,   # Personal Financial Advisor - 5.8%
    
    # Administrative - Highest automation risk
    "43-9021.00": 0.990,   # Data Entry Keyer - 99%
    "43-4051.00": 0.550,   # Customer Service Rep - 55%
    "43-6014.00": 0.962,   # Secretary/Admin Assistant - 96.2%
    "43-4171.00": 0.946,   # Receptionist - 94.6%
    
    # Legal
    "23-1011.00": 0.035,   # Lawyer - 3.5%
    "23-2011.00": 0.940,   # Paralegal - 94%
    "23-2093.00": 0.660,   # Legal Support Worker - 66%
    
    # Manufacturing
    "51-2092.00": 0.973,   # Team Assembler - 97.3%
    "51-4041.00": 0.865,   # Machinist - 86.5%
    "51-9061.00": 0.980,   # Inspector/Tester - 98%
    "17-2112.00": 0.018,   # Industrial Engineer - 1.8%
    
    # Transportation
    "53-3032.00": 0.790,   # Heavy Truck Driver - 79%
    "53-3033.00": 0.890,   # Light Truck Driver - 89%
    "53-6021.00": 0.810,   # Parking Attendant - 81%
    
    # Education - Low automation risk
    "25-2021.00": 0.007,   # Elementary Teacher - 0.7%
    "25-1011.00": 0.032,   # Business Professor - 3.2%
    "25-9041.00": 0.560,   # Teacher Assistant - 56%
    
    # Retail
    "41-2031.00": 0.920,   # Retail Salesperson - 92%
    "41-2011.00": 0.970,   # Cashier - 97%
    "41-1011.00": 0.016,   # Retail Supervisor - 1.6%
}

# =============================================================================
# EXTENDED OCCUPATIONS
# =============================================================================

EXTENDED_OCCUPATIONS = [
    # LEGAL SECTOR
    {
        "occupation_id": "occ-013",
        "standard_title": "Lawyer",
        "onet_code": "23-1011.00",
        "onet_description": "Represent clients in criminal and civil litigation and other legal proceedings.",
        "noc_2026_code": "41101",
        "noc_teer_category": 0,
        "noc_description": "Lawyers advise clients on legal matters, represent clients before courts.",
        "esco_uri": "http://data.europa.eu/esco/occupation/legal-001",
        "esco_description": "Lawyers represent and advise clients on legal matters.",
        "industry_sector": "Legal",
        "frey_osborne_probability": 0.035,
    },
    {
        "occupation_id": "occ-014",
        "standard_title": "Paralegal",
        "onet_code": "23-2011.00",
        "onet_description": "Assist lawyers by investigating facts, preparing legal documents.",
        "noc_2026_code": "42100",
        "noc_teer_category": 2,
        "noc_description": "Paralegal assistants and legal assistants prepare legal documents.",
        "esco_uri": "http://data.europa.eu/esco/occupation/legal-002",
        "esco_description": "Paralegals assist lawyers with research and document preparation.",
        "industry_sector": "Legal",
        "frey_osborne_probability": 0.940,
    },
    # MANUFACTURING SECTOR
    {
        "occupation_id": "occ-015",
        "standard_title": "Industrial Engineer",
        "onet_code": "17-2112.00",
        "onet_description": "Design, develop, test, and evaluate integrated systems for managing industrial production.",
        "noc_2026_code": "21321",
        "noc_teer_category": 0,
        "noc_description": "Industrial and manufacturing engineers conduct studies to optimize processes.",
        "esco_uri": "http://data.europa.eu/esco/occupation/mfg-001",
        "esco_description": "Industrial engineers design efficient systems for production.",
        "industry_sector": "Manufacturing",
        "frey_osborne_probability": 0.018,
    },
    {
        "occupation_id": "occ-016",
        "standard_title": "Quality Control Inspector",
        "onet_code": "51-9061.00",
        "onet_description": "Inspect, test, sort, sample, or weigh materials or products for defects.",
        "noc_2026_code": "94100",
        "noc_teer_category": 4,
        "noc_description": "Inspectors and testers verify products meet quality standards.",
        "esco_uri": "http://data.europa.eu/esco/occupation/mfg-002",
        "esco_description": "Quality control inspectors examine products for defects.",
        "industry_sector": "Manufacturing",
        "frey_osborne_probability": 0.980,
    },
    {
        "occupation_id": "occ-017",
        "standard_title": "CNC Machine Operator",
        "onet_code": "51-4041.00",
        "onet_description": "Set up and operate computer-controlled machines to perform machining operations.",
        "noc_2026_code": "94104",
        "noc_teer_category": 3,
        "noc_description": "Machine operators set up and operate CNC equipment.",
        "esco_uri": "http://data.europa.eu/esco/occupation/mfg-003",
        "esco_description": "CNC operators program and operate computer-controlled machines.",
        "industry_sector": "Manufacturing",
        "frey_osborne_probability": 0.865,
    },
    # TRANSPORTATION
    {
        "occupation_id": "occ-018",
        "standard_title": "Heavy Truck Driver",
        "onet_code": "53-3032.00",
        "onet_description": "Drive a tractor-trailer combination or a truck with a capacity of at least 26,000 pounds.",
        "noc_2026_code": "73300",
        "noc_teer_category": 3,
        "noc_description": "Transport truck drivers operate heavy trucks to transport goods.",
        "esco_uri": "http://data.europa.eu/esco/occupation/trans-001",
        "esco_description": "Heavy truck drivers transport goods over long distances.",
        "industry_sector": "Transportation",
        "frey_osborne_probability": 0.790,
    },
    {
        "occupation_id": "occ-019",
        "standard_title": "Logistics Coordinator",
        "onet_code": "13-1081.00",
        "onet_description": "Coordinate and expedite the flow of materials within or between departments.",
        "noc_2026_code": "13201",
        "noc_teer_category": 1,
        "noc_description": "Logistics specialists coordinate supply chain and shipping.",
        "esco_uri": "http://data.europa.eu/esco/occupation/trans-002",
        "esco_description": "Logistics coordinators manage the movement of goods.",
        "industry_sector": "Transportation",
        "frey_osborne_probability": 0.590,
    },
    # EDUCATION
    {
        "occupation_id": "occ-020",
        "standard_title": "Elementary School Teacher",
        "onet_code": "25-2021.00",
        "onet_description": "Teach students basic academic and social skills in elementary school.",
        "noc_2026_code": "41221",
        "noc_teer_category": 0,
        "noc_description": "Elementary school teachers teach basic subjects to students.",
        "esco_uri": "http://data.europa.eu/esco/occupation/edu-001",
        "esco_description": "Primary school teachers educate children in fundamental subjects.",
        "industry_sector": "Education",
        "frey_osborne_probability": 0.007,
    },
    {
        "occupation_id": "occ-021",
        "standard_title": "Teaching Assistant",
        "onet_code": "25-9041.00",
        "onet_description": "Assist teachers by performing duties such as tutoring and clerical work.",
        "noc_2026_code": "43100",
        "noc_teer_category": 3,
        "noc_description": "Educational assistants assist teachers with classroom activities.",
        "esco_uri": "http://data.europa.eu/esco/occupation/edu-002",
        "esco_description": "Teaching assistants support classroom instruction.",
        "industry_sector": "Education",
        "frey_osborne_probability": 0.560,
    },
    # RETAIL
    {
        "occupation_id": "occ-022",
        "standard_title": "Retail Salesperson",
        "onet_code": "41-2031.00",
        "onet_description": "Sell merchandise in establishments such as retail stores.",
        "noc_2026_code": "64100",
        "noc_teer_category": 4,
        "noc_description": "Retail salespersons sell goods directly to customers.",
        "esco_uri": "http://data.europa.eu/esco/occupation/retail-001",
        "esco_description": "Retail sales workers assist customers and process sales.",
        "industry_sector": "Retail",
        "frey_osborne_probability": 0.920,
    },
    {
        "occupation_id": "occ-023",
        "standard_title": "Cashier",
        "onet_code": "41-2011.00",
        "onet_description": "Receive and disburse money in establishments other than financial institutions.",
        "noc_2026_code": "65100",
        "noc_teer_category": 5,
        "noc_description": "Cashiers operate cash registers and process transactions.",
        "esco_uri": "http://data.europa.eu/esco/occupation/retail-002",
        "esco_description": "Cashiers handle customer payments and transactions.",
        "industry_sector": "Retail",
        "frey_osborne_probability": 0.970,
    },
    # ACCOUNTING (Detailed)
    {
        "occupation_id": "occ-024",
        "standard_title": "Bookkeeping Clerk",
        "onet_code": "43-3031.00",
        "onet_description": "Compute, classify, record, and verify numerical data for use in maintaining accounting records.",
        "noc_2026_code": "14200",
        "noc_teer_category": 3,
        "noc_description": "Bookkeepers maintain financial records and ledgers.",
        "esco_uri": "http://data.europa.eu/esco/occupation/fin-003",
        "esco_description": "Bookkeeping clerks record financial transactions.",
        "industry_sector": "Finance",
        "frey_osborne_probability": 0.976,
    },
    {
        "occupation_id": "occ-025",
        "standard_title": "Personal Financial Advisor",
        "onet_code": "13-2052.00",
        "onet_description": "Advise clients on financial plans utilizing knowledge of tax and investment strategies.",
        "noc_2026_code": "11102",
        "noc_teer_category": 0,
        "noc_description": "Financial planners develop financial plans for clients.",
        "esco_uri": "http://data.europa.eu/esco/occupation/fin-004",
        "esco_description": "Financial advisors help clients plan for financial goals.",
        "industry_sector": "Finance",
        "frey_osborne_probability": 0.058,
    },
    # HR
    {
        "occupation_id": "occ-026",
        "standard_title": "Human Resources Specialist",
        "onet_code": "13-1071.00",
        "onet_description": "Perform activities in human resources area including recruitment, personnel policies.",
        "noc_2026_code": "11200",
        "noc_teer_category": 1,
        "noc_description": "Human resources professionals recruit and manage employees.",
        "esco_uri": "http://data.europa.eu/esco/occupation/hr-001",
        "esco_description": "HR specialists handle recruitment and employee relations.",
        "industry_sector": "Human Resources",
        "frey_osborne_probability": 0.310,
    },
    {
        "occupation_id": "occ-027",
        "standard_title": "Recruiter",
        "onet_code": "13-1071.01",
        "onet_description": "Seek out, interview, and screen applicants to fill existing and future job openings.",
        "noc_2026_code": "11201",
        "noc_teer_category": 1,
        "noc_description": "Recruiters source and screen job candidates.",
        "esco_uri": "http://data.europa.eu/esco/occupation/hr-002",
        "esco_description": "Recruiters find and evaluate candidates for positions.",
        "industry_sector": "Human Resources",
        "frey_osborne_probability": 0.410,
    },
    # MARKETING
    {
        "occupation_id": "occ-028",
        "standard_title": "Marketing Manager",
        "onet_code": "11-2021.00",
        "onet_description": "Plan, direct, or coordinate marketing policies and programs.",
        "noc_2026_code": "10022",
        "noc_teer_category": 0,
        "noc_description": "Advertising and marketing managers plan marketing campaigns.",
        "esco_uri": "http://data.europa.eu/esco/occupation/mkt-001",
        "esco_description": "Marketing managers develop and execute marketing strategies.",
        "industry_sector": "Marketing",
        "frey_osborne_probability": 0.014,
    },
    {
        "occupation_id": "occ-029",
        "standard_title": "Market Research Analyst",
        "onet_code": "13-1161.00",
        "onet_description": "Research market conditions to examine potential sales of a product or service.",
        "noc_2026_code": "41402",
        "noc_teer_category": 1,
        "noc_description": "Market research analysts study market conditions and trends.",
        "esco_uri": "http://data.europa.eu/esco/occupation/mkt-002",
        "esco_description": "Market researchers analyze consumer behavior and trends.",
        "industry_sector": "Marketing",
        "frey_osborne_probability": 0.610,
    },
]

# =============================================================================
# EXTENDED TASKS
# =============================================================================

EXTENDED_TASKS = [
    # LAWYER TASKS
    {
        "task_id": "task-018",
        "occupation_id": "occ-013",
        "task_description": "Analyze legal issues and apply relevant laws and precedents",
        "task_category": "Legal Analysis",
        "frequency_score": 5,
        "human_interaction_level": 2,
        "cognitive_complexity": 5,
        "physical_requirement": 1,
        "is_routine": False,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": True,
        "requires_creativity": True,
        "requires_physical_presence": False,
    },
    {
        "task_id": "task-019",
        "occupation_id": "occ-013",
        "task_description": "Draft legal documents and contracts",
        "task_category": "Documentation",
        "frequency_score": 4,
        "human_interaction_level": 2,
        "cognitive_complexity": 4,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": True,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    {
        "task_id": "task-020",
        "occupation_id": "occ-013",
        "task_description": "Represent clients in court proceedings",
        "task_category": "Litigation",
        "frequency_score": 3,
        "human_interaction_level": 5,
        "cognitive_complexity": 5,
        "physical_requirement": 2,
        "is_routine": False,
        "is_cognitive": True,
        "is_digital_native": False,
        "requires_judgment": True,
        "requires_creativity": True,
        "requires_physical_presence": True,
    },
    # PARALEGAL TASKS
    {
        "task_id": "task-021",
        "occupation_id": "occ-014",
        "task_description": "Conduct legal research using databases and case law",
        "task_category": "Research",
        "frequency_score": 5,
        "human_interaction_level": 1,
        "cognitive_complexity": 3,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": False,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    {
        "task_id": "task-022",
        "occupation_id": "occ-014",
        "task_description": "Organize and maintain legal files and case documentation",
        "task_category": "Administration",
        "frequency_score": 5,
        "human_interaction_level": 1,
        "cognitive_complexity": 2,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": False,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    # INDUSTRIAL ENGINEER TASKS
    {
        "task_id": "task-023",
        "occupation_id": "occ-015",
        "task_description": "Analyze production workflows and identify inefficiencies",
        "task_category": "Process Analysis",
        "frequency_score": 4,
        "human_interaction_level": 3,
        "cognitive_complexity": 5,
        "physical_requirement": 2,
        "is_routine": False,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": True,
        "requires_creativity": True,
        "requires_physical_presence": True,
    },
    {
        "task_id": "task-024",
        "occupation_id": "occ-015",
        "task_description": "Design automation solutions for manufacturing processes",
        "task_category": "Engineering Design",
        "frequency_score": 3,
        "human_interaction_level": 2,
        "cognitive_complexity": 5,
        "physical_requirement": 1,
        "is_routine": False,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": True,
        "requires_creativity": True,
        "requires_physical_presence": False,
    },
    # QC INSPECTOR TASKS
    {
        "task_id": "task-025",
        "occupation_id": "occ-016",
        "task_description": "Visually inspect products for defects and quality standards",
        "task_category": "Inspection",
        "frequency_score": 5,
        "human_interaction_level": 1,
        "cognitive_complexity": 2,
        "physical_requirement": 2,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": False,
        "requires_judgment": True,
        "requires_creativity": False,
        "requires_physical_presence": True,
    },
    {
        "task_id": "task-026",
        "occupation_id": "occ-016",
        "task_description": "Record inspection results and generate quality reports",
        "task_category": "Documentation",
        "frequency_score": 5,
        "human_interaction_level": 1,
        "cognitive_complexity": 1,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": False,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    # TRUCK DRIVER TASKS
    {
        "task_id": "task-027",
        "occupation_id": "occ-018",
        "task_description": "Operate heavy commercial vehicle safely on highways",
        "task_category": "Vehicle Operation",
        "frequency_score": 5,
        "human_interaction_level": 1,
        "cognitive_complexity": 3,
        "physical_requirement": 3,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": False,
        "requires_judgment": True,
        "requires_creativity": False,
        "requires_physical_presence": True,
    },
    {
        "task_id": "task-028",
        "occupation_id": "occ-018",
        "task_description": "Complete delivery documentation and electronic logs",
        "task_category": "Documentation",
        "frequency_score": 5,
        "human_interaction_level": 2,
        "cognitive_complexity": 1,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": False,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    # TEACHER TASKS
    {
        "task_id": "task-029",
        "occupation_id": "occ-020",
        "task_description": "Develop lesson plans and instructional materials",
        "task_category": "Curriculum Development",
        "frequency_score": 4,
        "human_interaction_level": 1,
        "cognitive_complexity": 4,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": True,
        "requires_creativity": True,
        "requires_physical_presence": False,
    },
    {
        "task_id": "task-030",
        "occupation_id": "occ-020",
        "task_description": "Deliver classroom instruction to students",
        "task_category": "Teaching",
        "frequency_score": 5,
        "human_interaction_level": 5,
        "cognitive_complexity": 4,
        "physical_requirement": 2,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": False,
        "requires_judgment": True,
        "requires_creativity": True,
        "requires_physical_presence": True,
    },
    {
        "task_id": "task-031",
        "occupation_id": "occ-020",
        "task_description": "Grade student assignments and provide feedback",
        "task_category": "Assessment",
        "frequency_score": 4,
        "human_interaction_level": 2,
        "cognitive_complexity": 3,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": True,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    # CASHIER TASKS
    {
        "task_id": "task-032",
        "occupation_id": "occ-023",
        "task_description": "Scan items and process customer payments",
        "task_category": "Transaction Processing",
        "frequency_score": 5,
        "human_interaction_level": 3,
        "cognitive_complexity": 1,
        "physical_requirement": 2,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": False,
        "requires_creativity": False,
        "requires_physical_presence": True,
    },
    {
        "task_id": "task-033",
        "occupation_id": "occ-023",
        "task_description": "Balance cash drawer at end of shift",
        "task_category": "Reconciliation",
        "frequency_score": 4,
        "human_interaction_level": 1,
        "cognitive_complexity": 2,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": False,
        "requires_creativity": False,
        "requires_physical_presence": True,
    },
    # BOOKKEEPER TASKS
    {
        "task_id": "task-034",
        "occupation_id": "occ-024",
        "task_description": "Record financial transactions in accounting software",
        "task_category": "Data Entry",
        "frequency_score": 5,
        "human_interaction_level": 1,
        "cognitive_complexity": 2,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": False,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    {
        "task_id": "task-035",
        "occupation_id": "occ-024",
        "task_description": "Reconcile bank statements with ledger entries",
        "task_category": "Reconciliation",
        "frequency_score": 4,
        "human_interaction_level": 1,
        "cognitive_complexity": 2,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": False,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    # HR RECRUITER TASKS
    {
        "task_id": "task-036",
        "occupation_id": "occ-027",
        "task_description": "Screen resumes and applications for job requirements",
        "task_category": "Screening",
        "frequency_score": 5,
        "human_interaction_level": 1,
        "cognitive_complexity": 3,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": True,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    {
        "task_id": "task-037",
        "occupation_id": "occ-027",
        "task_description": "Conduct interviews with job candidates",
        "task_category": "Interview",
        "frequency_score": 4,
        "human_interaction_level": 5,
        "cognitive_complexity": 4,
        "physical_requirement": 1,
        "is_routine": False,
        "is_cognitive": True,
        "is_digital_native": False,
        "requires_judgment": True,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    # MARKET RESEARCH TASKS
    {
        "task_id": "task-038",
        "occupation_id": "occ-029",
        "task_description": "Collect and analyze consumer survey data",
        "task_category": "Data Analysis",
        "frequency_score": 4,
        "human_interaction_level": 1,
        "cognitive_complexity": 3,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": False,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
    {
        "task_id": "task-039",
        "occupation_id": "occ-029",
        "task_description": "Generate reports on market trends and competitor activity",
        "task_category": "Reporting",
        "frequency_score": 3,
        "human_interaction_level": 2,
        "cognitive_complexity": 4,
        "physical_requirement": 1,
        "is_routine": True,
        "is_cognitive": True,
        "is_digital_native": True,
        "requires_judgment": True,
        "requires_creativity": False,
        "requires_physical_presence": False,
    },
]

# =============================================================================
# QUEBEC-SPECIFIC COMPLIANCE RULES
# =============================================================================

QUEBEC_COMPLIANCE_RULES = [
    # OIQ - Professional Engineering
    {
        "compliance_id": str(uuid.uuid4()),
        "task_id": "task-024",  # Design automation solutions
        "jurisdiction": "Quebec",
        "regulatory_body": "OIQ (Ordre des ingenieurs du Quebec)",
        "eu_ai_act_risk_level": None,
        "hitl_required": True,
        "human_signature_required": True,  # P.Eng seal required
        "audit_trail_required": True,
        "transparency_notice_required": False,
        "compliance_penalty_factor": 0.0,  # BLOCKED
        "legal_reference": "Quebec Engineers Act R.S.Q. c. I-9 - Engineering work requires P.Eng seal",
    },
    # CAI - Privacy for HR
    {
        "compliance_id": str(uuid.uuid4()),
        "task_id": "task-036",  # Screen resumes
        "jurisdiction": "Quebec",
        "regulatory_body": "CAI (Commission d'acces a l'information)",
        "eu_ai_act_risk_level": None,
        "hitl_required": True,
        "human_signature_required": False,
        "audit_trail_required": True,
        "transparency_notice_required": True,
        "compliance_penalty_factor": 0.6,
        "legal_reference": "Quebec Act respecting the protection of personal information - Law 25 (2023) - Automated decision-making disclosure required",
    },
    # CNESST - Occupational Safety
    {
        "compliance_id": str(uuid.uuid4()),
        "task_id": "task-025",  # QC Inspection
        "jurisdiction": "Quebec",
        "regulatory_body": "CNESST (Commission des normes, de l'equite, de la sante et de la securite du travail)",
        "eu_ai_act_risk_level": None,
        "hitl_required": True,
        "human_signature_required": True,  # Safety inspection requires certified inspector
        "audit_trail_required": True,
        "transparency_notice_required": False,
        "compliance_penalty_factor": 0.0,  # BLOCKED
        "legal_reference": "Quebec Act respecting occupational health and safety - Safety inspections require certified professionals",
    },
    # CPA Quebec - Accounting
    {
        "compliance_id": str(uuid.uuid4()),
        "task_id": "task-034",  # Record financial transactions
        "jurisdiction": "Quebec",
        "regulatory_body": "CPA Quebec (Ordre des comptables professionnels agrees)",
        "eu_ai_act_risk_level": None,
        "hitl_required": False,
        "human_signature_required": False,
        "audit_trail_required": True,
        "transparency_notice_required": False,
        "compliance_penalty_factor": 0.95,
        "legal_reference": "Quebec Chartered Professional Accountants Act - Routine bookkeeping exempt from CPA requirements",
    },
    # Barreau du Quebec - Legal
    {
        "compliance_id": str(uuid.uuid4()),
        "task_id": "task-018",  # Legal analysis
        "jurisdiction": "Quebec",
        "regulatory_body": "Barreau du Quebec",
        "eu_ai_act_risk_level": None,
        "hitl_required": True,
        "human_signature_required": True,  # Legal advice requires licensed lawyer
        "audit_trail_required": True,
        "transparency_notice_required": True,
        "compliance_penalty_factor": 0.0,  # BLOCKED
        "legal_reference": "Quebec Bar Act - Practice of law restricted to members of the Bar",
    },
    {
        "compliance_id": str(uuid.uuid4()),
        "task_id": "task-021",  # Legal research
        "jurisdiction": "Quebec",
        "regulatory_body": "Barreau du Quebec",
        "eu_ai_act_risk_level": None,
        "hitl_required": False,
        "human_signature_required": False,
        "audit_trail_required": False,
        "transparency_notice_required": False,
        "compliance_penalty_factor": 1.0,  # Legal research is not practice of law
        "legal_reference": "Quebec Bar Act - Legal research may be performed by non-lawyers under supervision",
    },
]

# =============================================================================
# EU AI ACT EXTENDED COMPLIANCE
# =============================================================================

EU_AI_ACT_EXTENDED = [
    # Employment - CV Screening (Annex III)
    {
        "compliance_id": str(uuid.uuid4()),
        "task_id": "task-036",  # Screen resumes
        "jurisdiction": "EU",
        "regulatory_body": "EU AI Office",
        "eu_ai_act_risk_level": "High-Risk",
        "eu_ai_act_annex": "Annex III",
        "hitl_required": True,
        "human_signature_required": False,
        "audit_trail_required": True,
        "transparency_notice_required": True,
        "compliance_penalty_factor": 0.5,
        "legal_reference": "EU AI Act Art. 6, Annex III Section 4(a) - AI in recruitment and selection of candidates",
    },
    {
        "compliance_id": str(uuid.uuid4()),
        "task_id": "task-037",  # Conduct interviews
        "jurisdiction": "EU",
        "regulatory_body": "EU AI Office",
        "eu_ai_act_risk_level": "High-Risk",
        "eu_ai_act_annex": "Annex III",
        "hitl_required": True,
        "human_signature_required": True,  # Final hiring decision requires human
        "audit_trail_required": True,
        "transparency_notice_required": True,
        "compliance_penalty_factor": 0.3,
        "legal_reference": "EU AI Act Art. 6, Annex III Section 4(b) - AI for making decisions affecting employment",
    },
    # Education - Grading (Annex III)
    {
        "compliance_id": str(uuid.uuid4()),
        "task_id": "task-031",  # Grade assignments
        "jurisdiction": "EU",
        "regulatory_body": "EU AI Office",
        "eu_ai_act_risk_level": "High-Risk",
        "eu_ai_act_annex": "Annex III",
        "hitl_required": True,
        "human_signature_required": False,
        "audit_trail_required": True,
        "transparency_notice_required": True,
        "compliance_penalty_factor": 0.6,
        "legal_reference": "EU AI Act Art. 6, Annex III Section 3(a) - AI determining access to education",
    },
    # Limited Risk - Chatbots
    {
        "compliance_id": str(uuid.uuid4()),
        "task_id": "task-014",  # Customer inquiries
        "jurisdiction": "EU",
        "regulatory_body": "EU AI Office",
        "eu_ai_act_risk_level": "Limited-Risk",
        "eu_ai_act_annex": None,
        "hitl_required": False,
        "human_signature_required": False,
        "audit_trail_required": False,
        "transparency_notice_required": True,  # Must disclose AI interaction
        "compliance_penalty_factor": 0.9,
        "legal_reference": "EU AI Act Art. 50 - Transparency obligations for AI systems interacting with natural persons",
    },
]

# =============================================================================
# EXTENDED SKILLS
# =============================================================================

EXTENDED_SKILLS = [
    {
        "skill_id": str(uuid.uuid4()),
        "skill_name": "Legal Research",
        "skill_description": "Ability to research case law, statutes, and legal precedents",
        "taxonomy_source": "O*NET",
        "skill_type": "Hard",
        "skill_category": "Legal",
        "competency_level_required": 4,
        "importance_level": 0.9,
        "is_automatable": True,
        "automation_tool_category": "LLM",
    },
    {
        "skill_id": str(uuid.uuid4()),
        "skill_name": "Quality Inspection",
        "skill_description": "Ability to identify defects and quality issues in products",
        "taxonomy_source": "OaSIS SCT 2025",
        "skill_type": "Hard",
        "skill_category": "Manufacturing",
        "competency_level_required": 3,
        "importance_level": 0.85,
        "is_automatable": True,
        "automation_tool_category": "Computer Vision",
    },
    {
        "skill_id": str(uuid.uuid4()),
        "skill_name": "Commercial Driving",
        "skill_description": "Operating heavy commercial vehicles safely",
        "taxonomy_source": "NOC",
        "skill_type": "Hard",
        "skill_category": "Transportation",
        "competency_level_required": 3,
        "importance_level": 0.95,
        "is_automatable": True,
        "automation_tool_category": "Autonomous Systems",
    },
    {
        "skill_id": str(uuid.uuid4()),
        "skill_name": "Classroom Management",
        "skill_description": "Managing student behavior and engagement in educational settings",
        "taxonomy_source": "ESCO",
        "skill_type": "Soft",
        "skill_category": "Education",
        "competency_level_required": 4,
        "importance_level": 0.9,
        "is_automatable": False,
        "automation_tool_category": None,
    },
    {
        "skill_id": str(uuid.uuid4()),
        "skill_name": "Cash Handling",
        "skill_description": "Processing cash and electronic payments accurately",
        "taxonomy_source": "OaSIS SCT 2025",
        "skill_type": "Hard",
        "skill_category": "Retail",
        "competency_level_required": 2,
        "importance_level": 0.7,
        "is_automatable": True,
        "automation_tool_category": "Self-checkout/Kiosk",
    },
    {
        "skill_id": str(uuid.uuid4()),
        "skill_name": "Process Optimization",
        "skill_description": "Analyzing and improving operational workflows",
        "taxonomy_source": "O*NET",
        "skill_type": "Hard",
        "skill_category": "Engineering",
        "competency_level_required": 4,
        "importance_level": 0.85,
        "is_automatable": True,
        "automation_tool_category": "LLM + Analytics",
    },
    {
        "skill_id": str(uuid.uuid4()),
        "skill_name": "Talent Assessment",
        "skill_description": "Evaluating candidate qualifications and cultural fit",
        "taxonomy_source": "ESCO",
        "skill_type": "Soft",
        "skill_category": "Human Resources",
        "competency_level_required": 4,
        "importance_level": 0.85,
        "is_automatable": True,
        "automation_tool_category": "LLM",
    },
    {
        "skill_id": str(uuid.uuid4()),
        "skill_name": "Bank Reconciliation",
        "skill_description": "Matching financial records with bank statements",
        "taxonomy_source": "O*NET",
        "skill_type": "Hard",
        "skill_category": "Accounting",
        "competency_level_required": 2,
        "importance_level": 0.8,
        "is_automatable": True,
        "automation_tool_category": "RPA",
    },
]

# =============================================================================
# EXTENDED CROSSWALKS
# =============================================================================

EXTENDED_CROSSWALKS = [
    {
        "crosswalk_id": str(uuid.uuid4()),
        "onet_code": "23-1011.00",
        "noc_2021_code": "41101",
        "noc_2026_code": "41101",
        "esco_uri": "http://data.europa.eu/esco/occupation/legal-001",
        "isco_08_code": "2611",
        "match_quality": "Exact",
        "match_confidence": 0.95,
        "mapping_notes": "Lawyer - Consistent classification globally",
    },
    {
        "crosswalk_id": str(uuid.uuid4()),
        "onet_code": "17-2112.00",
        "noc_2021_code": "21321",
        "noc_2026_code": "21321",
        "esco_uri": "http://data.europa.eu/esco/occupation/mfg-001",
        "isco_08_code": "2141",
        "match_quality": "Exact",
        "match_confidence": 0.92,
        "mapping_notes": "Industrial Engineer - Consistent across systems",
    },
    {
        "crosswalk_id": str(uuid.uuid4()),
        "onet_code": "25-2021.00",
        "noc_2021_code": "41221",
        "noc_2026_code": "41221",
        "esco_uri": "http://data.europa.eu/esco/occupation/edu-001",
        "isco_08_code": "2341",
        "match_quality": "Exact",
        "match_confidence": 0.98,
        "mapping_notes": "Elementary School Teacher - Universal classification",
    },
    {
        "crosswalk_id": str(uuid.uuid4()),
        "onet_code": "41-2011.00",
        "noc_2021_code": "65100",
        "noc_2026_code": "65100",
        "esco_uri": "http://data.europa.eu/esco/occupation/retail-002",
        "isco_08_code": "5230",
        "match_quality": "Exact",
        "match_confidence": 0.95,
        "mapping_notes": "Cashier - High automation potential globally",
    },
    {
        "crosswalk_id": str(uuid.uuid4()),
        "onet_code": "53-3032.00",
        "noc_2021_code": "73300",
        "noc_2026_code": "73300",
        "esco_uri": "http://data.europa.eu/esco/occupation/trans-001",
        "isco_08_code": "8332",
        "match_quality": "Exact",
        "match_confidence": 0.90,
        "mapping_notes": "Heavy Truck Driver - Autonomous vehicle impact",
    },
    {
        "crosswalk_id": str(uuid.uuid4()),
        "onet_code": "13-1071.01",
        "noc_2021_code": "11201",
        "noc_2026_code": "11201",
        "esco_uri": "http://data.europa.eu/esco/occupation/hr-002",
        "isco_08_code": "2423",
        "match_quality": "Close",
        "match_confidence": 0.85,
        "mapping_notes": "Recruiter - EU AI Act High-Risk for automated hiring",
    },
]
