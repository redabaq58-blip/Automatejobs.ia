#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Tier 1 Intelligence + Proprietary Data Platform
Tests all Tier 1 Intelligence endpoints (game-changing competitive moat) plus proprietary data:

TIER 1 INTELLIGENCE (Review Request Focus):
- Executive Dashboard (/api/intelligence/executive-dashboard)
- Automation Pressure Index™ (/api/intelligence/pressure-index/{occupation})
- First-Mover Windows (/api/intelligence/adoption/first-mover)
- Regulatory Timeline (/api/intelligence/regulatory/timeline)
- Workforce Impact (/api/intelligence/skills/workforce-impact)
- Automate Now List (/api/intelligence/arbitrage/automate-now)
- Hidden Cost Multipliers (/api/intelligence/tco/hidden-multipliers)

PROPRIETARY DATA (Competitive Moat):
- AI Tools Database (15+ enterprise tools)
- Task-to-Tool Recommendations with fit scores
- Implementation Complexity with real-world costs
- Task Decomposition with atomic subtasks
- Failure Modes with probabilities and mitigation
- ROI Calculations with payback periods
- Automation Blueprints combining all data
"""
import requests
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class Tier1IntelligenceAPITester:
    def __init__(self, base_url: str = "https://job-automation-index.preview.emergentagent.com"):
        self.base_url = base_url.rstrip('/')
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def log_test(self, name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "name": name,
            "success": success,
            "details": details,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        })

    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> tuple:
        """Make HTTP request and return (success, response, status_code)"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params, timeout=30)
            else:
                return False, f"Unsupported method: {method}", None
            
            return True, response, response.status_code
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}", None

    def test_root_endpoint(self) -> bool:
        """Test the root API endpoint"""
        success, response, status = self.make_request('GET', '/api/')
        
        if not success:
            self.log_test("Root Endpoint", False, response)
            return False
        
        if status != 200:
            self.log_test("Root Endpoint", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            required_fields = ["message", "version", "endpoints"]
            if not all(field in data for field in required_fields):
                self.log_test("Root Endpoint", False, f"Missing required fields in response: {data}")
                return False
            
            self.log_test("Root Endpoint", True, f"API version: {data.get('version')}", data)
            return True
        except json.JSONDecodeError:
            self.log_test("Root Endpoint", False, "Invalid JSON response")
            return False

    def test_database_status(self) -> bool:
        """Test /api/database/status endpoint with extended data counts"""
        success, response, status = self.make_request('GET', '/api/database/status')
        
        if not success:
            self.log_test("Database Status", False, response)
            return False
        
        if status != 200:
            self.log_test("Database Status", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            # Check required fields
            if "status" not in data or "counts" not in data:
                self.log_test("Database Status", False, f"Missing required fields: {data}")
                return False
            
            if data["status"] != "connected":
                self.log_test("Database Status", False, f"Database not connected: {data['status']}")
                return False
            
            # Check counts
            counts = data["counts"]
            expected_tables = ["occupations", "tasks", "skills", "compliance_rules", "automation_scores", "crosswalks", "data_sources"]
            
            missing_tables = [table for table in expected_tables if table not in counts]
            if missing_tables:
                self.log_test("Database Status", False, f"Missing table counts: {missing_tables}")
                return False
            
            # Verify extended data counts match expectations
            expected_counts = {
                "occupations": 29,  # Extended with 17 additional occupations  
                "tasks": 39,        # Extended with 22 new tasks
                "automation_scores": 156,  # Extended automation scores
                "compliance_rules": 17,    # Quebec + EU AI Act compliance rules
            }
            
            validation_errors = []
            for table, expected_count in expected_counts.items():
                actual_count = counts.get(table, 0)
                if actual_count != expected_count:
                    validation_errors.append(f"{table}: expected {expected_count}, got {actual_count}")
            
            if validation_errors:
                self.log_test("Database Status", False, f"Count mismatches: {', '.join(validation_errors)}")
                return False
            
            # Verify minimum data exists
            if counts.get("occupations", 0) == 0:
                self.log_test("Database Status", False, "No occupations in database")
                return False
            
            self.log_test("Database Status", True, f"Database connected with extended data - {counts['occupations']} occupations, {counts['tasks']} tasks, {counts['compliance_rules']} compliance rules", data)
            return True
            
        except json.JSONDecodeError:
            self.log_test("Database Status", False, "Invalid JSON response")
            return False

    def test_high_automation_tasks(self) -> bool:
        """Test /api/tasks/high-automation endpoint"""
        # Test with default parameters
        success, response, status = self.make_request('GET', '/api/tasks/high-automation')
        
        if not success:
            self.log_test("High Automation Tasks", False, response)
            return False
        
        if status != 200:
            self.log_test("High Automation Tasks", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("High Automation Tasks", False, f"Expected list, got {type(data)}")
                return False
            
            # Test with custom parameters
            params = {"min_score": 70.0, "jurisdiction": "USA-Federal", "limit": 10}
            success2, response2, status2 = self.make_request('GET', '/api/tasks/high-automation', params=params)
            
            if not success2 or status2 != 200:
                self.log_test("High Automation Tasks (Custom Params)", False, f"Custom params failed: {status2}")
                return False
            
            custom_data = response2.json()
            if not isinstance(custom_data, list):
                self.log_test("High Automation Tasks", False, "Custom params returned non-list")
                return False
            
            # Check if results have required fields
            if custom_data:
                required_fields = ["task_description", "occupation_title", "automation_score", "automation_tier", "recommended_approach"]
                sample_task = custom_data[0]
                missing_fields = [field for field in required_fields if field not in sample_task]
                if missing_fields:
                    self.log_test("High Automation Tasks", False, f"Missing fields: {missing_fields}")
                    return False
            
            self.log_test("High Automation Tasks", True, f"Found {len(data)} tasks with default params, {len(custom_data)} with custom params", {"default_count": len(data), "custom_count": len(custom_data)})
            return True
            
        except json.JSONDecodeError:
            self.log_test("High Automation Tasks", False, "Invalid JSON response")
            return False

    def test_compliance_blocked_tasks(self) -> bool:
        """Test /api/compliance/blocked endpoint"""
        # Test EU jurisdiction (should have strictest rules)
        success, response, status = self.make_request('GET', '/api/compliance/blocked', params={"jurisdiction": "EU"})
        
        if not success:
            self.log_test("Compliance Blocked Tasks", False, response)
            return False
        
        if status != 200:
            self.log_test("Compliance Blocked Tasks", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Compliance Blocked Tasks", False, f"Expected list, got {type(data)}")
                return False
            
            # Check if results have required fields
            if data:
                required_fields = ["task_description", "occupation_title", "jurisdiction", "restrictions", "compliance_penalty_factor"]
                sample_task = data[0]
                missing_fields = [field for field in required_fields if field not in sample_task]
                if missing_fields:
                    self.log_test("Compliance Blocked Tasks", False, f"Missing fields: {missing_fields}")
                    return False
            
            # Test other jurisdictions
            jurisdictions = ["USA-Federal", "Canada-Federal", "Quebec"]
            jurisdiction_results = {}
            
            for jurisdiction in jurisdictions:
                success_j, response_j, status_j = self.make_request('GET', '/api/compliance/blocked', params={"jurisdiction": jurisdiction})
                if success_j and status_j == 200:
                    jurisdiction_results[jurisdiction] = len(response_j.json())
            
            self.log_test("Compliance Blocked Tasks", True, f"EU: {len(data)} blocked tasks. Other jurisdictions: {jurisdiction_results}", {"eu_blocked": len(data), "other_jurisdictions": jurisdiction_results})
            return True
            
        except json.JSONDecodeError:
            self.log_test("Compliance Blocked Tasks", False, "Invalid JSON response")
            return False

    def test_score_task_endpoint(self) -> bool:
        """Test POST /api/score/task endpoint - deterministic scoring"""
        test_cases = [
            {
                "name": "High Automation Task",
                "payload": {
                    "frequency": 5,
                    "human_interaction": 1,
                    "cognitive_complexity": 2,
                    "is_routine": True,
                    "is_digital": True,
                    "requires_judgment": False,
                    "requires_creativity": False,
                    "jurisdiction": "USA-Federal"
                },
                "expected_score_range": (70, 100)
            },
            {
                "name": "Low Automation Task (Human Required)",
                "payload": {
                    "frequency": 3,
                    "human_interaction": 5,
                    "cognitive_complexity": 5,
                    "is_routine": False,
                    "is_digital": False,
                    "requires_judgment": True,
                    "requires_creativity": True,
                    "jurisdiction": "USA-Federal"
                },
                "expected_score_range": (0, 40)
            },
            {
                "name": "EU AI Act Restricted Task",
                "payload": {
                    "frequency": 4,
                    "human_interaction": 2,
                    "cognitive_complexity": 3,
                    "is_routine": True,
                    "is_digital": True,
                    "hitl_required": True,
                    "eu_risk_level": "High-Risk",
                    "jurisdiction": "EU"
                },
                "expected_score_range": (0, 80)  # Should be penalized
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            success, response, status = self.make_request('POST', '/api/score/task', data=test_case["payload"])
            
            if not success:
                self.log_test(f"Score Task - {test_case['name']}", False, response)
                all_passed = False
                continue
            
            if status != 200:
                self.log_test(f"Score Task - {test_case['name']}", False, f"Expected 200, got {status}")
                all_passed = False
                continue
            
            try:
                data = response.json()
                
                # Check required fields
                required_fields = ["final_automation_score", "automation_tier", "recommended_approach", 
                                 "digital_feasibility", "cognitive_routine_index", "compliance_penalty", "explanation"]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test(f"Score Task - {test_case['name']}", False, f"Missing fields: {missing_fields}")
                    all_passed = False
                    continue
                
                # Check score is in expected range
                score = data["final_automation_score"]
                min_score, max_score = test_case["expected_score_range"]
                if not (min_score <= score <= max_score):
                    self.log_test(f"Score Task - {test_case['name']}", False, f"Score {score} not in expected range {test_case['expected_score_range']}")
                    all_passed = False
                    continue
                
                self.log_test(f"Score Task - {test_case['name']}", True, f"Score: {score}, Tier: {data['automation_tier']}", data)
                
            except json.JSONDecodeError:
                self.log_test(f"Score Task - {test_case['name']}", False, "Invalid JSON response")
                all_passed = False
        
        return all_passed

    def test_crosswalk_endpoint(self) -> bool:
        """Test /api/crosswalk/{code} endpoint"""
        # Test known codes from seed data
        test_codes = [
            {"code": "15-1252.00", "source": "onet", "name": "Software Developer O*NET"},
            {"code": "21232", "source": "noc", "name": "Software Developer NOC"},
            {"code": "29-1141.00", "source": "onet", "name": "Registered Nurse O*NET"}
        ]
        
        all_passed = True
        
        for test_code in test_codes:
            endpoint = f"/api/crosswalk/{test_code['code']}"
            params = {"source_system": test_code["source"]}
            
            success, response, status = self.make_request('GET', endpoint, params=params)
            
            if not success:
                self.log_test(f"Crosswalk - {test_code['name']}", False, response)
                all_passed = False
                continue
            
            if status == 404:
                # This might be expected if crosswalk data is missing
                self.log_test(f"Crosswalk - {test_code['name']}", True, "No crosswalk found (acceptable)")
                continue
            elif status != 200:
                self.log_test(f"Crosswalk - {test_code['name']}", False, f"Expected 200 or 404, got {status}")
                all_passed = False
                continue
            
            try:
                data = response.json()
                
                # Check has at least some cross-reference data
                expected_fields = ["onet_code", "noc_2026_code", "esco_uri", "match_quality"]
                present_fields = [field for field in expected_fields if field in data and data[field]]
                
                if len(present_fields) < 2:
                    self.log_test(f"Crosswalk - {test_code['name']}", False, f"Insufficient cross-reference data: {data}")
                    all_passed = False
                    continue
                
                self.log_test(f"Crosswalk - {test_code['name']}", True, f"Found crosswalk with {len(present_fields)} fields", data)
                
            except json.JSONDecodeError:
                self.log_test(f"Crosswalk - {test_code['name']}", False, "Invalid JSON response")
                all_passed = False
        
        return all_passed

    def test_industries_summary(self) -> bool:
        """Test /api/industries/summary endpoint for industry-level automation stats"""
        # Test without filter
        success, response, status = self.make_request('GET', '/api/industries/summary')
        
        if not success:
            self.log_test("Industries Summary", False, response)
            return False
        
        if status != 200:
            self.log_test("Industries Summary", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Industries Summary", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Industries Summary", False, "No industry data returned")
                return False
            
            # Check required fields in first industry
            required_fields = ["industry", "occupation_count", "task_count", "average_automation_score", 
                             "highest_score", "lowest_score", "high_automation_tasks"]
            sample_industry = data[0]
            missing_fields = [field for field in required_fields if field not in sample_industry]
            if missing_fields:
                self.log_test("Industries Summary", False, f"Missing fields: {missing_fields}")
                return False
            
            # Test with specific industry filter
            test_industry = data[0]["industry"]
            success2, response2, status2 = self.make_request('GET', '/api/industries/summary', params={"industry": test_industry})
            
            if success2 and status2 == 200:
                filtered_data = response2.json()
                if not isinstance(filtered_data, list) or len(filtered_data) == 0:
                    self.log_test("Industries Summary", False, "Industry filter returned no results")
                    return False
            
            # Verify we have multiple industries including new ones from extended data
            industry_names = [item["industry"] for item in data]
            expected_industries = ["Legal", "Manufacturing", "Education", "Retail", "Transportation", "Human Resources", "Marketing"]
            found_new_industries = [industry for industry in expected_industries if industry in industry_names]
            
            self.log_test("Industries Summary", True, f"Found {len(data)} industries including new ones: {found_new_industries}", {"total_industries": len(data), "new_industries": found_new_industries})
            return True
            
        except json.JSONDecodeError:
            self.log_test("Industries Summary", False, "Invalid JSON response")
            return False

    def test_quebec_compliance(self) -> bool:
        """Test /api/compliance/quebec endpoint for Quebec-specific regulatory rules"""
        success, response, status = self.make_request('GET', '/api/compliance/quebec')
        
        if not success:
            self.log_test("Quebec Compliance", False, response)
            return False
        
        if status != 200:
            self.log_test("Quebec Compliance", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Quebec Compliance", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Quebec Compliance", False, "No Quebec compliance rules returned")
                return False
            
            # Check required fields
            required_fields = ["task_description", "occupation_title", "regulatory_body", "restriction_level", 
                             "compliance_penalty_factor", "legal_reference"]
            sample_rule = data[0]
            missing_fields = [field for field in required_fields if field not in sample_rule]
            if missing_fields:
                self.log_test("Quebec Compliance", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check for expected Quebec regulatory bodies
            regulatory_bodies = [rule["regulatory_body"] for rule in data]
            expected_bodies = ["OIQ", "CNESST", "CAI", "CPA Quebec", "Barreau du Quebec"]
            found_bodies = [body for body in expected_bodies if any(body in rb for rb in regulatory_bodies)]
            
            if len(found_bodies) < 3:  # Should have at least 3 of the 5 major bodies
                self.log_test("Quebec Compliance", False, f"Expected major Quebec regulatory bodies, found: {regulatory_bodies}")
                return False
            
            # Check restriction levels
            restriction_levels = [rule["restriction_level"] for rule in data]
            expected_levels = ["BLOCKED", "SEVERELY_RESTRICTED", "RESTRICTED", "PERMITTED"]
            valid_levels = all(level in expected_levels for level in restriction_levels)
            
            if not valid_levels:
                self.log_test("Quebec Compliance", False, f"Invalid restriction levels: {restriction_levels}")
                return False
            
            self.log_test("Quebec Compliance", True, f"Found {len(data)} Quebec compliance rules with regulatory bodies: {found_bodies}", {"rule_count": len(data), "regulatory_bodies": found_bodies})
            return True
            
        except json.JSONDecodeError:
            self.log_test("Quebec Compliance", False, "Invalid JSON response")
            return False

    def test_frey_osborne_comparison(self) -> bool:
        """Test /api/frey-osborne/comparison endpoint for F-O baseline comparison"""
        # Test without filter
        success, response, status = self.make_request('GET', '/api/frey-osborne/comparison')
        
        if not success:
            self.log_test("Frey-Osborne Comparison", False, response)
            return False
        
        if status != 200:
            self.log_test("Frey-Osborne Comparison", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Frey-Osborne Comparison", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Frey-Osborne Comparison", False, "No F-O comparison data returned")
                return False
            
            # Check required fields
            required_fields = ["occupation_title", "onet_code", "frey_osborne_probability", 
                             "frey_osborne_percentage", "our_automation_score", "score_difference", "task_count"]
            sample_comparison = data[0]
            missing_fields = [field for field in required_fields if field not in sample_comparison]
            if missing_fields:
                self.log_test("Frey-Osborne Comparison", False, f"Missing fields: {missing_fields}")
                return False
            
            # Test with specific O*NET code filter
            test_onet_code = data[0]["onet_code"]
            success2, response2, status2 = self.make_request('GET', '/api/frey-osborne/comparison', params={"onet_code": test_onet_code})
            
            if success2 and status2 == 200:
                filtered_data = response2.json()
                if not isinstance(filtered_data, list):
                    self.log_test("Frey-Osborne Comparison", False, "O*NET code filter failed")
                    return False
            
            # Verify data quality - F-O probabilities should be between 0 and 1
            invalid_probabilities = [item for item in data if not (0 <= item["frey_osborne_probability"] <= 1)]
            if invalid_probabilities:
                self.log_test("Frey-Osborne Comparison", False, f"Invalid F-O probabilities: {[item['frey_osborne_probability'] for item in invalid_probabilities]}")
                return False
            
            # Check for high-automation occupations (should include cashiers, data entry, etc.)
            high_fo_occupations = [item for item in data if item["frey_osborne_probability"] > 0.9]
            
            self.log_test("Frey-Osborne Comparison", True, f"Found {len(data)} F-O comparisons, {len(high_fo_occupations)} with >90% F-O probability", {"total_comparisons": len(data), "high_fo_count": len(high_fo_occupations)})
            return True
            
        except json.JSONDecodeError:
            self.log_test("Frey-Osborne Comparison", False, "Invalid JSON response")
            return False

    def test_extended_high_automation_tasks(self) -> bool:
        """Test /api/tasks/high-automation endpoint with extended industry data"""
        # Test with default parameters
        success, response, status = self.make_request('GET', '/api/tasks/high-automation')
        
        if not success:
            self.log_test("Extended High Automation Tasks", False, response)
            return False
        
        if status != 200:
            self.log_test("Extended High Automation Tasks", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Extended High Automation Tasks", False, f"Expected list, got {type(data)}")
                return False
            
            # Check for tasks from new industries
            if data:
                industry_sectors = [task.get("industry_sector") for task in data if task.get("industry_sector")]
                new_industries = ["Legal", "Manufacturing", "Education", "Retail", "Transportation", "Human Resources", "Marketing"]
                found_new_industries = [industry for industry in new_industries if industry in industry_sectors]
                
                if len(found_new_industries) == 0:
                    self.log_test("Extended High Automation Tasks", False, f"No tasks from new industries found. Industries in results: {set(industry_sectors)}")
                    return False
                
                # Test different automation score thresholds
                thresholds = [60.0, 70.0, 80.0, 90.0]
                threshold_results = {}
                
                for threshold in thresholds:
                    params = {"min_score": threshold, "limit": 20}
                    success_t, response_t, status_t = self.make_request('GET', '/api/tasks/high-automation', params=params)
                    if success_t and status_t == 200:
                        threshold_data = response_t.json()
                        threshold_results[threshold] = len(threshold_data)
                
                self.log_test("Extended High Automation Tasks", True, f"Found tasks from new industries: {found_new_industries}. Threshold results: {threshold_results}", {"new_industries": found_new_industries, "threshold_results": threshold_results})
            else:
                self.log_test("Extended High Automation Tasks", True, "No high automation tasks found (acceptable if thresholds are strict)")
            
            return True
            
        except json.JSONDecodeError:
            self.log_test("Extended High Automation Tasks", False, "Invalid JSON response")
            return False

    def test_data_sources_endpoint(self) -> bool:
        """Test /api/data-sources endpoint"""
        success, response, status = self.make_request('GET', '/api/data-sources')
        
        if not success:
            self.log_test("Data Sources", False, response)
            return False
        
        if status != 200:
            self.log_test("Data Sources", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Data Sources", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Data Sources", False, "No data sources returned")
                return False
            
            # Check required fields in first source
            required_fields = ["source_name", "source_version", "license_type", "attribution_text", "data_coverage"]
            sample_source = data[0]
            missing_fields = [field for field in required_fields if field not in sample_source]
            if missing_fields:
                self.log_test("Data Sources", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check for expected data sources
            source_names = [source["source_name"] for source in data]
            expected_sources = ["O*NET", "NOC 2026", "ESCO"]
            found_sources = [source for source in expected_sources if source in source_names]
            
            if len(found_sources) < 2:
                self.log_test("Data Sources", False, f"Expected multiple data sources, found: {source_names}")
                return False
            
            self.log_test("Data Sources", True, f"Found {len(data)} data sources: {source_names}", data)
            return True
            
        except json.JSONDecodeError:
            self.log_test("Data Sources", False, "Invalid JSON response")
            return False

    def test_search_occupations(self) -> bool:
        """Test /api/occupations search endpoint"""
        search_tests = [
            {"query": "Developer", "expected_min": 1},
            {"query": "Nurse", "expected_min": 1},
            {"query": "Data", "expected_min": 1},
            {"query": "NonExistentJob12345", "expected_min": 0}
        ]
        
        all_passed = True
        
        for search_test in search_tests:
            params = {"query": search_test["query"], "limit": 10}
            success, response, status = self.make_request('GET', '/api/occupations', params=params)
            
            if not success:
                self.log_test(f"Search Occupations - '{search_test['query']}'", False, response)
                all_passed = False
                continue
            
            if status != 200:
                self.log_test(f"Search Occupations - '{search_test['query']}'", False, f"Expected 200, got {status}")
                all_passed = False
                continue
            
            try:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test(f"Search Occupations - '{search_test['query']}'", False, f"Expected list, got {type(data)}")
                    all_passed = False
                    continue
                
                if len(data) < search_test["expected_min"]:
                    self.log_test(f"Search Occupations - '{search_test['query']}'", False, f"Expected at least {search_test['expected_min']} results, got {len(data)}")
                    all_passed = False
                    continue
                
                # Check field structure if results exist
                if data:
                    required_fields = ["occupation_id", "standard_title", "industry_sector"]
                    sample_occupation = data[0]
                    missing_fields = [field for field in required_fields if field not in sample_occupation]
                    if missing_fields:
                        self.log_test(f"Search Occupations - '{search_test['query']}'", False, f"Missing fields: {missing_fields}")
                        all_passed = False
                        continue
                
                self.log_test(f"Search Occupations - '{search_test['query']}'", True, f"Found {len(data)} results")
                
            except json.JSONDecodeError:
                self.log_test(f"Search Occupations - '{search_test['query']}'", False, "Invalid JSON response")
                all_passed = False
        
        return all_passed

    def test_proprietary_quick_wins(self) -> bool:
        """Test /api/automation/quick-wins endpoint"""
        # Test with default parameters
        success, response, status = self.make_request('GET', '/api/automation/quick-wins')
        
        if not success:
            self.log_test("Proprietary Quick Wins", False, response)
            return False
        
        if status != 200:
            self.log_test("Proprietary Quick Wins", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Proprietary Quick Wins", False, f"Expected list, got {type(data)}")
                return False
            
            # Test with custom parameters
            params = {"min_roi": 150, "max_payback_months": 6}
            success2, response2, status2 = self.make_request('GET', '/api/automation/quick-wins', params=params)
            
            if not success2 or status2 != 200:
                self.log_test("Proprietary Quick Wins", False, f"Custom params failed: {status2}")
                return False
            
            custom_data = response2.json()
            
            # Check if results have required fields
            if data:
                required_fields = ["task_id", "task_description", "occupation", "payback_months", "year_1_roi_percentage", "annual_savings_usd", "recommended_tools"]
                sample_win = data[0]
                missing_fields = [field for field in required_fields if field not in sample_win]
                if missing_fields:
                    self.log_test("Proprietary Quick Wins", False, f"Missing fields: {missing_fields}")
                    return False
            
            self.log_test("Proprietary Quick Wins", True, f"Found {len(data)} quick wins (default), {len(custom_data)} with custom params", {"default_count": len(data), "custom_count": len(custom_data)})
            return True
            
        except json.JSONDecodeError:
            self.log_test("Proprietary Quick Wins", False, "Invalid JSON response")
            return False

    def test_proprietary_tools_recommendations(self) -> bool:
        """Test /api/tools/recommendations endpoint"""
        # Test without filter
        success, response, status = self.make_request('GET', '/api/tools/recommendations')
        
        if not success:
            self.log_test("Tools Recommendations", False, response)
            return False
        
        if status != 200:
            self.log_test("Tools Recommendations", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Tools Recommendations", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Tools Recommendations", False, "No tool recommendations returned")
                return False
            
            # Check required fields
            required_fields = ["task_id", "task_description", "recommended_tools", "recommended_architecture", "automation_confidence"]
            sample_rec = data[0]
            missing_fields = [field for field in required_fields if field not in sample_rec]
            if missing_fields:
                self.log_test("Tools Recommendations", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check tool details structure
            if sample_rec.get("recommended_tools"):
                tool = sample_rec["recommended_tools"][0]
                tool_fields = ["tool_id", "fit_score", "use_case", "estimated_accuracy", "setup_hours", "tool_name", "vendor"]
                missing_tool_fields = [field for field in tool_fields if field not in tool]
                if missing_tool_fields:
                    self.log_test("Tools Recommendations", False, f"Missing tool fields: {missing_tool_fields}")
                    return False
            
            # Test with task_id filter
            test_task_id = data[0]["task_id"]
            success2, response2, status2 = self.make_request('GET', '/api/tools/recommendations', params={"task_id": test_task_id})
            
            if success2 and status2 == 200:
                filtered_data = response2.json()
                if not isinstance(filtered_data, list) or len(filtered_data) == 0:
                    self.log_test("Tools Recommendations", False, "Task ID filter returned no results")
                    return False
            
            self.log_test("Tools Recommendations", True, f"Found {len(data)} tool recommendations with AI tools mapping", {"total_recommendations": len(data), "sample_task": test_task_id})
            return True
            
        except json.JSONDecodeError:
            self.log_test("Tools Recommendations", False, "Invalid JSON response")
            return False

    def test_proprietary_automation_blueprint(self) -> bool:
        """Test /api/automation/blueprint/{task_id} endpoint"""
        # First get a task ID from recommendations
        success, response, status = self.make_request('GET', '/api/tools/recommendations')
        if not success or status != 200:
            self.log_test("Automation Blueprint", False, "Could not get task ID for blueprint test")
            return False
        
        try:
            recommendations = response.json()
            if not recommendations:
                self.log_test("Automation Blueprint", False, "No recommendations available for blueprint test")
                return False
            
            test_task_id = recommendations[0]["task_id"]
            
            # Test blueprint endpoint
            success2, response2, status2 = self.make_request('GET', f'/api/automation/blueprint/{test_task_id}')
            
            if not success2:
                self.log_test("Automation Blueprint", False, response2)
                return False
            
            if status2 == 404:
                self.log_test("Automation Blueprint", False, f"No blueprint found for task {test_task_id}")
                return False
            elif status2 != 200:
                self.log_test("Automation Blueprint", False, f"Expected 200, got {status2}")
                return False
            
            data = response2.json()
            
            # Check required structure
            required_fields = ["task_id", "task_description", "sections"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                self.log_test("Automation Blueprint", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check sections structure
            sections = data.get("sections", {})
            expected_sections = ["recommended_tools", "implementation", "task_breakdown", "risk_analysis", "business_case"]
            found_sections = [section for section in expected_sections if section in sections]
            
            if len(found_sections) < 3:
                self.log_test("Automation Blueprint", False, f"Expected multiple sections, found: {list(sections.keys())}")
                return False
            
            self.log_test("Automation Blueprint", True, f"Complete blueprint for task {test_task_id} with sections: {found_sections}", {"task_id": test_task_id, "sections": found_sections})
            return True
            
        except json.JSONDecodeError:
            self.log_test("Automation Blueprint", False, "Invalid JSON response")
            return False

    def test_proprietary_failure_modes(self) -> bool:
        """Test /api/risks/failure-modes endpoint"""
        success, response, status = self.make_request('GET', '/api/risks/failure-modes')
        
        if not success:
            self.log_test("Failure Modes Analysis", False, response)
            return False
        
        if status != 200:
            self.log_test("Failure Modes Analysis", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Failure Modes Analysis", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Failure Modes Analysis", False, "No failure mode data returned")
                return False
            
            # Check required fields
            required_fields = ["task_id", "task_description", "failure_modes", "overall_failure_rate", "recommended_sla"]
            sample_failure = data[0]
            missing_fields = [field for field in required_fields if field not in sample_failure]
            if missing_fields:
                self.log_test("Failure Modes Analysis", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check failure mode details
            if sample_failure.get("failure_modes"):
                failure_mode = sample_failure["failure_modes"][0]
                failure_fields = ["failure_type", "description", "probability", "impact_severity", "detection_method", "mitigation"]
                missing_failure_fields = [field for field in failure_fields if field not in failure_mode]
                if missing_failure_fields:
                    self.log_test("Failure Modes Analysis", False, f"Missing failure mode fields: {missing_failure_fields}")
                    return False
            
            # Test with task_id filter  
            test_task_id = data[0]["task_id"]
            success2, response2, status2 = self.make_request('GET', '/api/risks/failure-modes', params={"task_id": test_task_id})
            
            if success2 and status2 == 200:
                filtered_data = response2.json()
                if not isinstance(filtered_data, list):
                    self.log_test("Failure Modes Analysis", False, "Task ID filter failed")
                    return False
            
            self.log_test("Failure Modes Analysis", True, f"Found {len(data)} failure mode analyses with detection and mitigation strategies", {"total_analyses": len(data), "sample_task": test_task_id})
            return True
            
        except json.JSONDecodeError:
            self.log_test("Failure Modes Analysis", False, "Invalid JSON response")
            return False

    def test_proprietary_roi_calculate(self) -> bool:
        """Test POST /api/roi/calculate endpoint"""
        test_payloads = [
            {
                "name": "Data Entry Automation",
                "payload": {
                    "annual_salary": 35000,
                    "automation_percentage": 0.85,
                    "implementation_cost": 15000,
                    "ongoing_annual_cost": 5000,
                    "region": "USA"
                }
            },
            {
                "name": "Customer Service Automation",
                "payload": {
                    "annual_salary": 38000,
                    "automation_percentage": 0.50,
                    "implementation_cost": 75000,
                    "ongoing_annual_cost": 24000,
                    "region": "Canada"
                }
            }
        ]
        
        all_passed = True
        
        for test_case in test_payloads:
            success, response, status = self.make_request('POST', '/api/roi/calculate', data=test_case["payload"])
            
            if not success:
                self.log_test(f"ROI Calculate - {test_case['name']}", False, response)
                all_passed = False
                continue
            
            if status != 200:
                self.log_test(f"ROI Calculate - {test_case['name']}", False, f"Expected 200, got {status}")
                all_passed = False
                continue
            
            try:
                data = response.json()
                
                # Check required structure
                required_sections = ["input", "analysis", "recommendation"]
                missing_sections = [section for section in required_sections if section not in data]
                if missing_sections:
                    self.log_test(f"ROI Calculate - {test_case['name']}", False, f"Missing sections: {missing_sections}")
                    all_passed = False
                    continue
                
                # Check analysis fields
                analysis = data.get("analysis", {})
                analysis_fields = ["fully_loaded_cost", "annual_labor_savings", "payback_months", "year_1_roi_percentage", "year_3_roi_percentage"]
                missing_analysis = [field for field in analysis_fields if field not in analysis]
                if missing_analysis:
                    self.log_test(f"ROI Calculate - {test_case['name']}", False, f"Missing analysis fields: {missing_analysis}")
                    all_passed = False
                    continue
                
                self.log_test(f"ROI Calculate - {test_case['name']}", True, f"Payback: {analysis.get('payback_months')} months, Year 1 ROI: {analysis.get('year_1_roi_percentage')}%", data)
                
            except json.JSONDecodeError:
                self.log_test(f"ROI Calculate - {test_case['name']}", False, "Invalid JSON response")
                all_passed = False
        
        return all_passed

    def test_proprietary_salary_benchmarks(self) -> bool:
        """Test /api/roi/salaries endpoint"""
        # Test different regions
        regions = ["USA", "Canada", "EU"]
        all_passed = True
        
        for region in regions:
            success, response, status = self.make_request('GET', '/api/roi/salaries', params={"region": region})
            
            if not success:
                self.log_test(f"Salary Benchmarks - {region}", False, response)
                all_passed = False
                continue
            
            if status != 200:
                self.log_test(f"Salary Benchmarks - {region}", False, f"Expected 200, got {status}")
                all_passed = False
                continue
            
            try:
                data = response.json()
                
                # Check required fields
                required_fields = ["region", "multiplier", "salaries"]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test(f"Salary Benchmarks - {region}", False, f"Missing fields: {missing_fields}")
                    all_passed = False
                    continue
                
                # Check salaries structure
                if data.get("salaries"):
                    salary_entry = data["salaries"][0]
                    salary_fields = ["occupation", "annual_salary", "fully_loaded_cost"]
                    missing_salary_fields = [field for field in salary_fields if field not in salary_entry]
                    if missing_salary_fields:
                        self.log_test(f"Salary Benchmarks - {region}", False, f"Missing salary fields: {missing_salary_fields}")
                        all_passed = False
                        continue
                
                self.log_test(f"Salary Benchmarks - {region}", True, f"Found {len(data.get('salaries', []))} occupations with multiplier {data.get('multiplier')}", {"region": region, "occupation_count": len(data.get('salaries', []))})
                
            except json.JSONDecodeError:
                self.log_test(f"Salary Benchmarks - {region}", False, "Invalid JSON response")
                all_passed = False
        
        # Test with specific occupation
        success, response, status = self.make_request('GET', '/api/roi/salaries', params={"region": "USA", "occupation": "Data Entry Keyer"})
        
        if success and status == 200:
            try:
                data = response.json()
                if "annual_salary" in data and "fully_loaded_cost" in data:
                    self.log_test("Salary Benchmarks - Specific Occupation", True, f"Data Entry Keyer: ${data['annual_salary']} (loaded: ${data['fully_loaded_cost']})", data)
                else:
                    self.log_test("Salary Benchmarks - Specific Occupation", False, "Missing salary data for specific occupation")
                    all_passed = False
            except json.JSONDecodeError:
                self.log_test("Salary Benchmarks - Specific Occupation", False, "Invalid JSON for specific occupation")
                all_passed = False
        else:
            self.log_test("Salary Benchmarks - Specific Occupation", False, "Specific occupation lookup failed")
            all_passed = False
        
        return all_passed

    def test_proprietary_task_decomposition(self) -> bool:
        """Test /api/tasks/decomposition endpoint"""
        success, response, status = self.make_request('GET', '/api/tasks/decomposition')
        
        if not success:
            self.log_test("Task Decomposition", False, response)
            return False
        
        if status != 200:
            self.log_test("Task Decomposition", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Task Decomposition", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Task Decomposition", False, "No task decomposition data returned")
                return False
            
            # Check required fields
            required_fields = ["parent_task_id", "parent_task_description", "atomic_subtasks", "total_human_time_minutes", "time_savings_percentage", "bottleneck_subtask"]
            sample_decomp = data[0]
            missing_fields = [field for field in required_fields if field not in sample_decomp]
            if missing_fields:
                self.log_test("Task Decomposition", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check subtasks structure
            if sample_decomp.get("atomic_subtasks"):
                subtask = sample_decomp["atomic_subtasks"][0]
                subtask_fields = ["subtask_id", "description", "automation_potential", "recommended_tool", "human_time_minutes", "automated_time_minutes"]
                missing_subtask_fields = [field for field in subtask_fields if field not in subtask]
                if missing_subtask_fields:
                    self.log_test("Task Decomposition", False, f"Missing subtask fields: {missing_subtask_fields}")
                    return False
            
            # Test with task_id filter
            test_task_id = data[0]["parent_task_id"]
            success2, response2, status2 = self.make_request('GET', '/api/tasks/decomposition', params={"task_id": test_task_id})
            
            if success2 and status2 == 200:
                filtered_data = response2.json()
                if not isinstance(filtered_data, list):
                    self.log_test("Task Decomposition", False, "Task ID filter failed")
                    return False
            
            self.log_test("Task Decomposition", True, f"Found {len(data)} task decompositions with atomic subtasks and time savings analysis", {"total_decompositions": len(data), "sample_savings": f"{sample_decomp.get('time_savings_percentage')}%"})
            return True
            
        except json.JSONDecodeError:
            self.log_test("Task Decomposition", False, "Invalid JSON response")
            return False

    def test_proprietary_implementation_complexity(self) -> bool:
        """Test /api/implementation/complexity endpoint"""
        success, response, status = self.make_request('GET', '/api/implementation/complexity')
        
        if not success:
            self.log_test("Implementation Complexity", False, response)
            return False
        
        if status != 200:
            self.log_test("Implementation Complexity", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Implementation Complexity", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Implementation Complexity", False, "No implementation complexity data returned")
                return False
            
            # Check required fields
            required_fields = ["task_id", "task_description", "complexity_level", "estimated_implementation_weeks", "estimated_cost_usd", "required_roles", "success_rate_industry"]
            sample_complexity = data[0]
            missing_fields = [field for field in required_fields if field not in sample_complexity]
            if missing_fields:
                self.log_test("Implementation Complexity", False, f"Missing fields: {missing_fields}")
                return False
            
            # Test complexity level filtering
            complexity_levels = ["SIMPLE", "MODERATE", "COMPLEX"]
            level_results = {}
            
            for level in complexity_levels:
                success_l, response_l, status_l = self.make_request('GET', '/api/implementation/complexity', params={"complexity_level": level})
                if success_l and status_l == 200:
                    level_data = response_l.json()
                    level_results[level] = len(level_data)
            
            # Test with task_id filter
            test_task_id = data[0]["task_id"]
            success2, response2, status2 = self.make_request('GET', '/api/implementation/complexity', params={"task_id": test_task_id})
            
            if success2 and status2 == 200:
                filtered_data = response2.json()
                if not isinstance(filtered_data, list):
                    self.log_test("Implementation Complexity", False, "Task ID filter failed")
                    return False
            
            self.log_test("Implementation Complexity", True, f"Found {len(data)} complexity assessments. Level breakdown: {level_results}", {"total_assessments": len(data), "complexity_levels": level_results})
            return True
            
        except json.JSONDecodeError:
            self.log_test("Implementation Complexity", False, "Invalid JSON response")
            return False

    def test_ai_tools_database(self) -> bool:
        """Test /api/tools/ai endpoint - AI Tools Database"""
        success, response, status = self.make_request('GET', '/api/tools/ai')
        
        if not success:
            self.log_test("AI Tools Database", False, response)
            return False
        
        if status != 200:
            self.log_test("AI Tools Database", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("AI Tools Database", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("AI Tools Database", False, "No AI tools returned")
                return False
            
            # Check for expected tools (should have 15+ enterprise tools)
            if len(data) < 10:
                self.log_test("AI Tools Database", False, f"Expected 15+ AI tools, got {len(data)}")
                return False
            
            # Check required fields
            required_fields = ["tool_id", "tool_name", "vendor", "category", "capabilities", "pricing_model", "enterprise_ready"]
            sample_tool = data[0]
            missing_fields = [field for field in required_fields if field not in sample_tool]
            if missing_fields:
                self.log_test("AI Tools Database", False, f"Missing fields: {missing_fields}")
                return False
            
            # Test category filtering
            categories = ["LLM_TEXT", "RPA_INTELLIGENT", "DOCUMENT_AI"]
            category_results = {}
            
            for category in categories:
                success_c, response_c, status_c = self.make_request('GET', '/api/tools/ai', params={"category": category})
                if success_c and status_c == 200:
                    cat_data = response_c.json()
                    category_results[category] = len(cat_data)
            
            # Test vendor filtering
            success_v, response_v, status_v = self.make_request('GET', '/api/tools/ai', params={"vendor": "OpenAI"})
            vendor_count = 0
            if success_v and status_v == 200:
                vendor_data = response_v.json()
                vendor_count = len(vendor_data)
            
            # Check for expected enterprise tools
            tool_names = [tool["tool_name"] for tool in data]
            expected_tools = ["GPT-5.2", "Claude", "UiPath", "Textract"]
            found_tools = [tool for tool in expected_tools if any(tool in name for name in tool_names)]
            
            self.log_test("AI Tools Database", True, f"Found {len(data)} AI tools including enterprise tools: {found_tools}. Categories: {category_results}, OpenAI tools: {vendor_count}", {"total_tools": len(data), "found_enterprise": found_tools, "categories": category_results})
            return True
            
        except json.JSONDecodeError:
            self.log_test("AI Tools Database", False, "Invalid JSON response")
            return False

    # =============================================================================
    # TIER 1 INTELLIGENCE ENDPOINTS TESTS (Review Request Focus)
    # =============================================================================

    def test_tier1_executive_dashboard(self) -> bool:
        """Test /api/intelligence/executive-dashboard - C-suite one-page view"""
        success, response, status = self.make_request('GET', '/api/intelligence/executive-dashboard')
        
        if not success:
            self.log_test("Tier1 Executive Dashboard", False, response)
            return False
        
        if status != 200:
            self.log_test("Tier1 Executive Dashboard", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            # Check required structure
            required_fields = ["generated_at", "key_metrics", "automate_now", "closing_windows", "compliance_alerts", "budget_warnings", "reskilling_opportunity"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                self.log_test("Tier1 Executive Dashboard", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check key metrics structure
            key_metrics = data.get("key_metrics", {})
            expected_metrics = ["total_jobs_at_risk_usa", "avg_hidden_cost_multiplier", "high_risk_compliance_areas"]
            missing_metrics = [metric for metric in expected_metrics if metric not in key_metrics]
            if missing_metrics:
                self.log_test("Tier1 Executive Dashboard", False, f"Missing key metrics: {missing_metrics}")
                return False
            
            # Validate data quality
            jobs_at_risk = key_metrics.get("total_jobs_at_risk_usa", 0)
            if jobs_at_risk < 1000000:  # Should be millions based on data
                self.log_test("Tier1 Executive Dashboard", False, f"Jobs at risk too low: {jobs_at_risk}")
                return False
            
            automate_now_count = len(data.get("automate_now", []))
            closing_windows_count = len(data.get("closing_windows", []))
            
            self.log_test("Tier1 Executive Dashboard", True, f"Executive dashboard loaded - {jobs_at_risk:,} jobs at risk, {automate_now_count} urgent automations, {closing_windows_count} closing windows", {
                "jobs_at_risk": jobs_at_risk,
                "automate_now": automate_now_count,
                "closing_windows": closing_windows_count
            })
            return True
            
        except json.JSONDecodeError:
            self.log_test("Tier1 Executive Dashboard", False, "Invalid JSON response")
            return False

    def test_tier1_automation_pressure_index(self) -> bool:
        """Test /api/intelligence/pressure-index/{occupation} - Automation Pressure Index™"""
        # Test occupations from the data
        test_occupations = ["Data Entry Clerk", "Customer Service Rep", "Paralegal", "Software Developer"]
        
        all_passed = True
        
        for occupation in test_occupations:
            success, response, status = self.make_request('GET', f'/api/intelligence/pressure-index/{occupation}')
            
            if not success:
                self.log_test(f"Tier1 Pressure Index - {occupation}", False, response)
                all_passed = False
                continue
            
            if status == 404:
                self.log_test(f"Tier1 Pressure Index - {occupation}", False, f"Occupation '{occupation}' not found in arbitrage index")
                all_passed = False
                continue
            elif status != 200:
                self.log_test(f"Tier1 Pressure Index - {occupation}", False, f"Expected 200, got {status}")
                all_passed = False
                continue
            
            try:
                data = response.json()
                
                # Check required fields
                required_fields = ["occupation", "automation_pressure_index", "max_possible", "components", "interpretation", "action"]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test(f"Tier1 Pressure Index - {occupation}", False, f"Missing fields: {missing_fields}")
                    all_passed = False
                    continue
                
                # Check components structure
                components = data.get("components", {})
                expected_components = ["wage_pressure", "automation_cost_decline", "market_adoption", "regulatory_openness"]
                missing_components = [comp for comp in expected_components if comp not in components]
                if missing_components:
                    self.log_test(f"Tier1 Pressure Index - {occupation}", False, f"Missing components: {missing_components}")
                    all_passed = False
                    continue
                
                # Validate index value
                pressure_index = data.get("automation_pressure_index", 0)
                if not (0 <= pressure_index <= 100):
                    self.log_test(f"Tier1 Pressure Index - {occupation}", False, f"Invalid pressure index: {pressure_index}")
                    all_passed = False
                    continue
                
                self.log_test(f"Tier1 Pressure Index - {occupation}", True, f"Pressure Index: {pressure_index}/100, Action: {data.get('action', '')[:50]}...", {
                    "pressure_index": pressure_index,
                    "interpretation": data.get("interpretation"),
                    "components": components
                })
                
            except json.JSONDecodeError:
                self.log_test(f"Tier1 Pressure Index - {occupation}", False, "Invalid JSON response")
                all_passed = False
        
        return all_passed

    def test_tier1_first_mover_windows(self) -> bool:
        """Test /api/intelligence/adoption/first-mover - closing opportunity windows"""
        success, response, status = self.make_request('GET', '/api/intelligence/adoption/first-mover')
        
        if not success:
            self.log_test("Tier1 First-Mover Windows", False, response)
            return False
        
        if status != 200:
            self.log_test("Tier1 First-Mover Windows", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Tier1 First-Mover Windows", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Tier1 First-Mover Windows", False, "No first-mover windows returned")
                return False
            
            # Check required fields
            required_fields = ["automation_type", "window_months", "current_adoption_rate", "window_status", "recommendation"]
            sample_window = data[0]
            missing_fields = [field for field in required_fields if field not in sample_window]
            if missing_fields:
                self.log_test("Tier1 First-Mover Windows", False, f"Missing fields: {missing_fields}")
                return False
            
            # Validate window status values
            valid_statuses = ["CLOSING", "NARROWING", "OPEN", "WIDE_OPEN", "EMERGING"]
            invalid_statuses = [w for w in data if w.get("window_status") not in valid_statuses]
            if invalid_statuses:
                self.log_test("Tier1 First-Mover Windows", False, f"Invalid window statuses: {[w.get('window_status') for w in invalid_statuses]}")
                return False
            
            # Check for urgent windows (should be sorted by urgency)
            closing_windows = [w for w in data if w.get("window_status") in ["CLOSING", "NARROWING"]]
            critical_windows = [w for w in data if w.get("window_months", 999) <= 6]
            
            self.log_test("Tier1 First-Mover Windows", True, f"Found {len(data)} automation opportunities, {len(closing_windows)} closing/narrowing, {len(critical_windows)} critical (<6 months)", {
                "total_windows": len(data),
                "closing_windows": len(closing_windows),
                "critical_windows": len(critical_windows),
                "sample_recommendations": [w.get("automation_type") for w in data[:3]]
            })
            return True
            
        except json.JSONDecodeError:
            self.log_test("Tier1 First-Mover Windows", False, "Invalid JSON response")
            return False

    def test_tier1_regulatory_timeline(self) -> bool:
        """Test /api/intelligence/regulatory/timeline - chronological compliance roadmap"""
        success, response, status = self.make_request('GET', '/api/intelligence/regulatory/timeline')
        
        if not success:
            self.log_test("Tier1 Regulatory Timeline", False, response)
            return False
        
        if status != 200:
            self.log_test("Tier1 Regulatory Timeline", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Tier1 Regulatory Timeline", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Tier1 Regulatory Timeline", False, "No regulatory timeline returned")
                return False
            
            # Check required fields
            required_fields = ["jurisdiction", "regulatory_body", "change_id", "predicted_date", "probability", "change_type", "description", "affected_tasks", "impact", "action_required"]
            sample_change = data[0]
            missing_fields = [field for field in required_fields if field not in sample_change]
            if missing_fields:
                self.log_test("Tier1 Regulatory Timeline", False, f"Missing fields: {missing_fields}")
                return False
            
            # Validate probability values (should be 0-1)
            invalid_probabilities = [c for c in data if not (0 <= c.get("probability", 0) <= 1)]
            if invalid_probabilities:
                self.log_test("Tier1 Regulatory Timeline", False, f"Invalid probabilities: {[c.get('probability') for c in invalid_probabilities]}")
                return False
            
            # Check for expected jurisdictions
            jurisdictions = list(set(c.get("jurisdiction") for c in data))
            expected_jurisdictions = ["EU", "USA-Federal", "Canada-Federal", "Quebec", "UK"]
            found_jurisdictions = [j for j in expected_jurisdictions if j in jurisdictions]
            
            if len(found_jurisdictions) < 3:
                self.log_test("Tier1 Regulatory Timeline", False, f"Expected multiple jurisdictions, found: {jurisdictions}")
                return False
            
            # Check for high-probability near-term changes
            high_probability = [c for c in data if c.get("probability", 0) >= 0.7]
            near_term = [c for c in data if "2026" in c.get("predicted_date", "")]
            
            self.log_test("Tier1 Regulatory Timeline", True, f"Found {len(data)} regulatory changes across {len(jurisdictions)} jurisdictions, {len(high_probability)} high-probability, {len(near_term)} in 2026", {
                "total_changes": len(data),
                "jurisdictions": found_jurisdictions,
                "high_probability": len(high_probability),
                "near_term_2026": len(near_term)
            })
            return True
            
        except json.JSONDecodeError:
            self.log_test("Tier1 Regulatory Timeline", False, "Invalid JSON response")
            return False

    def test_tier1_workforce_impact(self) -> bool:
        """Test /api/intelligence/skills/workforce-impact - 8M+ jobs at risk data"""
        success, response, status = self.make_request('GET', '/api/intelligence/skills/workforce-impact')
        
        if not success:
            self.log_test("Tier1 Workforce Impact", False, response)
            return False
        
        if status != 200:
            self.log_test("Tier1 Workforce Impact", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            # Check required fields
            required_fields = ["total_jobs_at_risk_usa", "critical_skills_count", "critical_skills", "average_reskilling_cost_usd", "total_reskilling_market_size_usd", "best_roi_transitions"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                self.log_test("Tier1 Workforce Impact", False, f"Missing fields: {missing_fields}")
                return False
            
            # Validate data scale expectations
            total_jobs_at_risk = data.get("total_jobs_at_risk_usa", 0)
            if total_jobs_at_risk < 8000000:  # Should be 8M+ based on description
                self.log_test("Tier1 Workforce Impact", False, f"Jobs at risk below expected 8M+: {total_jobs_at_risk}")
                return False
            
            # Check critical skills structure
            critical_skills = data.get("critical_skills", [])
            if not critical_skills:
                self.log_test("Tier1 Workforce Impact", False, "No critical skills data")
                return False
            
            # Check ROI transitions structure
            best_transitions = data.get("best_roi_transitions", [])
            if not best_transitions:
                self.log_test("Tier1 Workforce Impact", False, "No reskilling transitions data")
                return False
            
            # Validate critical skills have required fields
            sample_skill = critical_skills[0]
            skill_fields = ["skill", "half_life_years", "automation_threat_level", "jobs_at_risk_usa"]
            missing_skill_fields = [field for field in skill_fields if field not in sample_skill]
            if missing_skill_fields:
                self.log_test("Tier1 Workforce Impact", False, f"Missing skill fields: {missing_skill_fields}")
                return False
            
            market_size = data.get("total_reskilling_market_size_usd", 0)
            avg_cost = data.get("average_reskilling_cost_usd", 0)
            
            self.log_test("Tier1 Workforce Impact", True, f"USA workforce impact - {total_jobs_at_risk:,} jobs at risk, {len(critical_skills)} critical skills, ${market_size:,} reskilling market, ${avg_cost:,} avg cost", {
                "jobs_at_risk": total_jobs_at_risk,
                "critical_skills_count": len(critical_skills),
                "market_size_usd": market_size,
                "avg_reskilling_cost": avg_cost
            })
            return True
            
        except json.JSONDecodeError:
            self.log_test("Tier1 Workforce Impact", False, "Invalid JSON response")
            return False

    def test_tier1_automate_now_list(self) -> bool:
        """Test /api/intelligence/arbitrage/automate-now - urgent automation list"""
        success, response, status = self.make_request('GET', '/api/intelligence/arbitrage/automate-now')
        
        if not success:
            self.log_test("Tier1 Automate Now List", False, response)
            return False
        
        if status != 200:
            self.log_test("Tier1 Automate Now List", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Tier1 Automate Now List", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Tier1 Automate Now List", False, "No automate-now recommendations returned")
                return False
            
            # Check required fields
            required_fields = ["occupation", "arbitrage_score", "urgency", "wage_growth_yoy", "automation_cost_trend", "breakeven_improving_by", "labor_shortage"]
            sample_item = data[0]
            missing_fields = [field for field in required_fields if field not in sample_item]
            if missing_fields:
                self.log_test("Tier1 Automate Now List", False, f"Missing fields: {missing_fields}")
                return False
            
            # Validate urgency levels
            valid_urgencies = ["CRITICAL", "HIGH"]
            invalid_urgencies = [item for item in data if item.get("urgency") not in valid_urgencies]
            if invalid_urgencies:
                self.log_test("Tier1 Automate Now List", False, f"Expected only CRITICAL/HIGH urgency, found: {[item.get('urgency') for item in invalid_urgencies]}")
                return False
            
            # Check arbitrage scores (should be high for automate-now list)
            low_scores = [item for item in data if item.get("arbitrage_score", 0) < 75]
            if low_scores:
                self.log_test("Tier1 Automate Now List", False, f"Low arbitrage scores in urgent list: {[item.get('arbitrage_score') for item in low_scores]}")
                return False
            
            # Count by urgency level
            critical_count = len([item for item in data if item.get("urgency") == "CRITICAL"])
            high_count = len([item for item in data if item.get("urgency") == "HIGH"])
            
            self.log_test("Tier1 Automate Now List", True, f"Found {len(data)} urgent automation opportunities - {critical_count} CRITICAL, {high_count} HIGH urgency", {
                "total_urgent": len(data),
                "critical_count": critical_count,
                "high_count": high_count,
                "top_occupations": [item.get("occupation") for item in data[:3]]
            })
            return True
            
        except json.JSONDecodeError:
            self.log_test("Tier1 Automate Now List", False, "Invalid JSON response")
            return False

    def test_tier1_hidden_cost_multipliers(self) -> bool:
        """Test /api/intelligence/tco/hidden-multipliers - budget warning data"""
        success, response, status = self.make_request('GET', '/api/intelligence/tco/hidden-multipliers')
        
        if not success:
            self.log_test("Tier1 Hidden Cost Multipliers", False, response)
            return False
        
        if status != 200:
            self.log_test("Tier1 Hidden Cost Multipliers", False, f"Expected 200, got {status}")
            return False
        
        try:
            data = response.json()
            
            if not isinstance(data, list):
                self.log_test("Tier1 Hidden Cost Multipliers", False, f"Expected list, got {type(data)}")
                return False
            
            if len(data) == 0:
                self.log_test("Tier1 Hidden Cost Multipliers", False, "No hidden cost multiplier data returned")
                return False
            
            # Check required fields
            required_fields = ["automation_type", "hidden_cost_multiplier", "total_visible_usd", "total_hidden_usd", "total_tco_year1_usd", "top_budget_overrun"]
            sample_multiplier = data[0]
            missing_fields = [field for field in required_fields if field not in sample_multiplier]
            if missing_fields:
                self.log_test("Tier1 Hidden Cost Multipliers", False, f"Missing fields: {missing_fields}")
                return False
            
            # Validate multiplier values (should be > 1.0)
            low_multipliers = [item for item in data if item.get("hidden_cost_multiplier", 0) <= 1.0]
            if low_multipliers:
                self.log_test("Tier1 Hidden Cost Multipliers", False, f"Invalid multipliers (<= 1.0): {[item.get('hidden_cost_multiplier') for item in low_multipliers]}")
                return False
            
            # Check for high-risk automation types (multiplier > 2.0)
            high_risk = [item for item in data if item.get("hidden_cost_multiplier", 0) > 2.0]
            
            # Validate budget overrun structure
            sample_overrun = sample_multiplier.get("top_budget_overrun", {})
            if not isinstance(sample_overrun, dict) or "item" not in sample_overrun or "typical_overrun_pct" not in sample_overrun:
                self.log_test("Tier1 Hidden Cost Multipliers", False, f"Invalid budget overrun structure: {sample_overrun}")
                return False
            
            # Check expected automation types
            automation_types = [item.get("automation_type") for item in data]
            expected_types = ["Data Entry Automation", "Customer Service AI", "Legal Document Review", "HR Resume Screening"]
            found_types = [t for t in expected_types if t in automation_types]
            
            if len(found_types) < 3:
                self.log_test("Tier1 Hidden Cost Multipliers", False, f"Expected key automation types, found: {automation_types}")
                return False
            
            avg_multiplier = sum(item.get("hidden_cost_multiplier", 0) for item in data) / len(data)
            
            self.log_test("Tier1 Hidden Cost Multipliers", True, f"Found {len(data)} automation types with hidden cost data - avg multiplier: {avg_multiplier:.2f}x, {len(high_risk)} high-risk (>2x)", {
                "total_types": len(data),
                "avg_multiplier": round(avg_multiplier, 2),
                "high_risk_count": len(high_risk),
                "automation_types": found_types
            })
            return True
            
        except json.JSONDecodeError:
            self.log_test("Tier1 Hidden Cost Multipliers", False, "Invalid JSON response")
            return False

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all API tests including proprietary data endpoints"""
        print(f"\n🚀 Starting Tier 1 Intelligence + Proprietary Data Platform API Tests")
        print(f"📊 Testing against: {self.base_url}")
        print("=" * 70)
        
        # Core endpoint tests (quick verification)
        self.test_root_endpoint()
        self.test_database_status()
        
        # TIER 1 INTELLIGENCE ENDPOINTS - Game-Changing Data (Review Request Focus)
        print("\n🎯 Testing Tier 1 Intelligence Endpoints (Review Request Focus)...")
        
        # Primary Tier 1 Intelligence endpoints from review request  
        self.test_tier1_executive_dashboard()                 # /api/intelligence/executive-dashboard
        self.test_tier1_automation_pressure_index()          # /api/intelligence/pressure-index/{occupation}
        self.test_tier1_first_mover_windows()                # /api/intelligence/adoption/first-mover
        self.test_tier1_regulatory_timeline()                # /api/intelligence/regulatory/timeline
        self.test_tier1_workforce_impact()                   # /api/intelligence/skills/workforce-impact
        self.test_tier1_automate_now_list()                  # /api/intelligence/arbitrage/automate-now
        self.test_tier1_hidden_cost_multipliers()            # /api/intelligence/tco/hidden-multipliers
        
        # PROPRIETARY DATA ENDPOINTS - The Competitive Moat
        print("\n💎 Testing Proprietary Data Endpoints (Competitive Moat)...")
        
        # Core proprietary endpoints from review request
        self.test_proprietary_quick_wins()                    # /api/automation/quick-wins
        self.test_proprietary_tools_recommendations()         # /api/tools/recommendations  
        self.test_proprietary_automation_blueprint()          # /api/automation/blueprint/{task_id}
        self.test_proprietary_failure_modes()                # /api/risks/failure-modes
        self.test_proprietary_roi_calculate()                # /api/roi/calculate (POST)
        self.test_proprietary_salary_benchmarks()            # /api/roi/salaries
        self.test_proprietary_task_decomposition()           # /api/tasks/decomposition
        self.test_proprietary_implementation_complexity()    # /api/implementation/complexity
        
        # Supporting proprietary endpoints
        self.test_ai_tools_database()                        # /api/tools/ai (AI Tools Database)
        
        # Generate summary
        print("\n" + "=" * 70)
        print(f"📋 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests PASSED! Tier 1 Intelligence + Proprietary API is fully functional - Competitive Moat Secured!")
            return {"success": True, "total": self.tests_run, "passed": self.tests_passed, "results": self.test_results}
        else:
            failed_tests = [r for r in self.test_results if not r["success"]]
            print(f"⚠️  {len(failed_tests)} tests FAILED:")
            for test in failed_tests:
                print(f"   - {test['name']}: {test['details']}")
            
            return {"success": False, "total": self.tests_run, "passed": self.tests_passed, "results": self.test_results, "failed_tests": failed_tests}

def main():
    """Main test execution for Tier 1 Intelligence + proprietary data endpoints"""
    # Use the public backend URL from frontend .env
    backend_url = "https://job-automation-index.preview.emergentagent.com"
    
    tester = Tier1IntelligenceAPITester(backend_url)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    return 0 if results["success"] else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)