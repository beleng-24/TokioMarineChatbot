"""
AI-Enabled Plan Document Review System
Automates checklist generation from Orange workflow output
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher
import pandas as pd
from pathlib import Path


class LearningEngine:
    """Manages continuous learning and term mappings"""
    
    def __init__(self, learned_mappings_path: str = "learned_mappings.json"):
        self.mappings_path = Path(learned_mappings_path)
        self.learned_mappings = self._load_mappings()
    
    def _load_mappings(self) -> Dict:
        """Load learned mappings from JSON file"""
        if self.mappings_path.exists():
            with open(self.mappings_path, 'r') as f:
                return json.load(f)
        return {
            "synonyms": {},  # term: [list of synonyms]
            "corrections": {},  # incorrect_term: correct_term
            "custom_rules": [],  # user-defined validation rules
            "learning_history": []  # audit trail
        }
    
    def _save_mappings(self):
        """Save learned mappings to JSON file"""
        with open(self.mappings_path, 'w') as f:
            json.dump(self.learned_mappings, f, indent=2)
    
    def add_synonym(self, term: str, synonym: str, user: str = "system"):
        """Learn a new synonym for a term"""
        if term not in self.learned_mappings["synonyms"]:
            self.learned_mappings["synonyms"][term] = []
        
        if synonym not in self.learned_mappings["synonyms"][term]:
            self.learned_mappings["synonyms"][term].append(synonym)
            self._log_learning("synonym_added", term, synonym, user)
            self._save_mappings()
    
    def add_correction(self, incorrect: str, correct: str, user: str = "system"):
        """Learn a correction"""
        self.learned_mappings["corrections"][incorrect] = correct
        self._log_learning("correction_added", incorrect, correct, user)
        self._save_mappings()
    
    def _log_learning(self, action: str, term: str, value: str, user: str):
        """Log learning activity"""
        self.learned_mappings["learning_history"].append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "term": term,
            "value": value,
            "user": user
        })
    
    def get_synonyms(self, term: str) -> List[str]:
        """Get all known synonyms for a term"""
        return self.learned_mappings["synonyms"].get(term, [])
    
    def get_correction(self, term: str) -> Optional[str]:
        """Get correction for a term if it exists"""
        return self.learned_mappings["corrections"].get(term)


class DefinitionsParser:
    """Parses and manages the definitions document"""
    
    def __init__(self, definitions_data: Dict):
        self.definitions = self._parse_definitions(definitions_data)
    
    def _parse_definitions(self, data: Dict) -> Dict:
        """Parse definitions into structured format"""
        # Sample structure based on Appendix 3 document
        definitions = {}
        
        # Define key fields and their identifiers/definitions
        fields = {
            "Group Name": {
                "identifiers": ["Policyholder", "Employer", "Group"],
                "location": "PA system only",
                "definition": "Policyholder, Employer, Group"
            },
            "Group Effective Date": {
                "identifiers": ["Effective", "Retated", "Revised effective dates"],
                "location": "PA system only",
                "definition": "Effective date of the contract"
            },
            "TPA": {
                "identifiers": ["Claims Administrator", "Third Party Administrator", "TPA", 
                               "Claims Provider", "Plan Administrator", "Plan Supervisor"],
                "location": "Plan Document",
                "definition": "A TPA performs administrative services for the Plan including payment of claims"
            },
            "UR Vendor": {
                "identifiers": ["Utilization Review", "Utilization Management", 
                               "Utilization Review Organization", "Pre-Certification", 
                               "Pre-Authorization", "MedAxis", "MedBridge", "Apex Medical Review"],
                "location": "Plan Document",
                "definition": "The process of certifying medical necessity for hospitalization and procedures"
            },
            "PPO Network": {
                "identifiers": ["PPO Network", "Preferred Provider Network", "Provider Network",
                               "Preferred Provider Organization", "HealthSphere", "StellarCare", 
                               "UnityHealth"],
                "location": "Plan Document",
                "definition": "An organization that has contracted with various providers"
            },
            "Min. Hour Requirement": {
                "identifiers": ["30 hours", "28 hours", "32 hours", "hours per week", "full-time"],
                "location": "Eligibility Section",
                "definition": "Employee is required to work specified hours per week"
            },
            "Retirees": {
                "identifiers": ["Retiree", "retirees", "retired employees"],
                "location": "Eligibility Section",
                "definition": "Coverage for retired employees"
            },
            "BOD, Directors, Officers": {
                "identifiers": ["Board of Directors", "Directors", "Officers", "owners", "partners"],
                "location": "Eligibility Section",
                "definition": "Board members, directors, or officers eligibility"
            },
            "Dependent Definitions": {
                "identifiers": ["Dependent", "legal spouse", "child", "domestic partner"],
                "location": "Eligibility Section",
                "definition": "Defined eligible dependent of an eligible employee"
            },
            "Req Adding Dependents": {
                "identifiers": ["special enrollment", "31 days", "30 days", "marriage", "birth", 
                               "adoption", "proof of relationship"],
                "location": "Special Enrollment Section",
                "definition": "Requirements for adding dependents"
            },
            "Dependent to Age 26": {
                "identifiers": ["26th birthday", "age 26", "until 26"],
                "location": "Eligibility Section",
                "definition": "Dependent child coverage until age 26"
            },
            "Grandchildren": {
                "identifiers": ["grandchildren", "children of dependent children", "legal guardian"],
                "location": "Eligibility Section",
                "definition": "Children of dependent children"
            },
            "Termination Provisions": {
                "identifiers": ["Termination", "coverage ends", "last day of employment"],
                "location": "Termination Section",
                "definition": "Circumstances in which coverage ends"
            },
            "Open Enrollment": {
                "identifiers": ["Open Enrollment", "annual enrollment", "once a year"],
                "location": "Eligibility Section",
                "definition": "Annual period for enrollment"
            },
            "Leave of Absence": {
                "identifiers": ["Leave of Absence", "LOA", "Leave", "FMLA", "3 months", "12 weeks"],
                "location": "Termination Section or FMLA Section",
                "definition": "Coverage continuation during leave"
            },
            "Medically Necessary": {
                "identifiers": ["Medically Necessary", "medical necessity", "preventing", "diagnosing", "treating"],
                "location": "Definitions Section",
                "definition": "Health care services required for diagnosis or treatment"
            },
            "E&I": {
                "identifiers": ["Experimental", "Investigational", "Unproven"],
                "location": "Exclusions Section or Definitions",
                "definition": "Experimental and Investigational treatments"
            },
            "R&C": {
                "identifiers": ["Reasonable & Customary", "Reasonable and Customary", 
                               "typical charge", "geographic area"],
                "location": "Definitions Section",
                "definition": "Typical charge for a service in a geographic area"
            },
            "Workers Comp": {
                "identifiers": ["Workers' Compensation", "Workers Compensation", "Occupational"],
                "location": "Exclusions Section",
                "definition": "Workers compensation exclusion"
            },
            "Transplant": {
                "identifiers": ["Transplant", "organ", "tissue transplant", "donor"],
                "location": "Transplant Benefits Section",
                "definition": "Transplant services coverage"
            },
            "ETS Gene Therapy": {
                "identifiers": ["ETS", "Emerging Therapy Solutions", "Gene Therapy"],
                "location": "Plan Document",
                "definition": "ETS Centers of Excellence for gene therapy"
            },
            "Coordination of Benefits": {
                "identifiers": ["Coordination of Benefits", "COB", "more than one Plan"],
                "location": "Coordination of Benefits Section",
                "definition": "Coordination when covered by multiple plans"
            },
            "COBRA": {
                "identifiers": ["COBRA", "Consolidated Omnibus Budget Reconciliation Act", 
                               "continuation", "18 months"],
                "location": "COBRA Section",
                "definition": "COBRA continuation coverage"
            },
            "Subrogation": {
                "identifiers": ["Subrogation", "Right to Reimbursement", "Reimbursement", 
                               "third party"],
                "location": "Subrogation Section",
                "definition": "Right to recover costs from third parties"
            },
            "Infertility": {
                "identifiers": ["Infertility", "$20,000", "$15,000", "$10,000"],
                "location": "Schedule of Benefits",
                "definition": "Infertility treatment coverage and limits"
            }
        }
        
        return fields
    
    def get_identifiers(self, field: str) -> List[str]:
        """Get all identifiers for a field"""
        return self.definitions.get(field, {}).get("identifiers", [])
    
    def get_location(self, field: str) -> str:
        """Get expected location for a field"""
        return self.definitions.get(field, {}).get("location", "Unknown")
    
    def get_definition(self, field: str) -> str:
        """Get definition for a field"""
        return self.definitions.get(field, {}).get("definition", "")


class Validator:
    """Validates extracted data and flags issues"""
    
    def __init__(self, definitions: DefinitionsParser, learning_engine: LearningEngine):
        self.definitions = definitions
        self.learning_engine = learning_engine
    
    def fuzzy_match(self, str1: str, str2: str, threshold: float = 0.8) -> bool:
        """Check if two strings are similar (catches typos)"""
        ratio = SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
        return ratio >= threshold
    
    def validate_field(self, field: str, extracted_value: Optional[str], 
                      plan_text: str) -> Dict:
        """
        Validate a field and return validation results
        Returns: {
            "status": "found" | "missing" | "possible_typo" | "unidentifiable",
            "value": extracted_value,
            "confidence": 0.0-1.0,
            "suggestions": [],
            "warnings": []
        }
        """
        result = {
            "field": field,
            "status": "missing",
            "value": extracted_value,
            "confidence": 0.0,
            "suggestions": [],
            "warnings": []
        }
        
        # Check if value was extracted
        if not extracted_value or extracted_value == "N/F":
            result["status"] = "missing"
            result["warnings"].append(f"No information found for {field}")
            return result
        
        # Get expected identifiers
        identifiers = self.definitions.get_identifiers(field)
        
        # Check for learned synonyms
        for identifier in identifiers:
            learned_synonyms = self.learning_engine.get_synonyms(identifier)
            identifiers.extend(learned_synonyms)
        
        # Check if extracted value matches known identifiers
        matched = False
        for identifier in identifiers:
            if identifier.lower() in extracted_value.lower():
                matched = True
                result["confidence"] = 1.0
                break
            
            # Fuzzy matching for typos
            if self.fuzzy_match(identifier, extracted_value, threshold=0.85):
                matched = True
                result["status"] = "possible_typo"
                result["confidence"] = 0.7
                result["suggestions"].append(f"Did you mean '{identifier}'?")
                result["warnings"].append(f"Possible typo detected in {field}")
                break
        
        if matched and result["status"] != "possible_typo":
            result["status"] = "found"
        elif not matched:
            result["status"] = "unidentifiable"
            result["confidence"] = 0.3
            result["warnings"].append(f"Could not identify '{extracted_value}' for {field}")
            result["suggestions"].append(f"Expected one of: {', '.join(identifiers[:3])}")
        
        # Check for corrections
        correction = self.learning_engine.get_correction(extracted_value)
        if correction:
            result["suggestions"].append(f"Previously corrected to: {correction}")
        
        return result
    
    def validate_checklist(self, checklist_data: Dict, plan_text: str = "") -> Dict:
        """Validate entire checklist and return validation report"""
        validation_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "complete",
            "fields_validated": 0,
            "fields_found": 0,
            "fields_missing": 0,
            "fields_with_issues": 0,
            "field_results": {},
            "warnings": [],
            "suggestions": []
        }
        
        for field, value in checklist_data.items():
            if field in ["Group Name", "Group Eff Date", "TPA", "Benefit Plan Name"]:
                # Header fields
                continue
            
            validation = self.validate_field(field, value, plan_text)
            validation_report["field_results"][field] = validation
            validation_report["fields_validated"] += 1
            
            if validation["status"] == "found":
                validation_report["fields_found"] += 1
            elif validation["status"] == "missing":
                validation_report["fields_missing"] += 1
                validation_report["warnings"].extend(validation["warnings"])
            else:
                validation_report["fields_with_issues"] += 1
                validation_report["warnings"].extend(validation["warnings"])
                validation_report["suggestions"].extend(validation["suggestions"])
        
        # Determine overall status
        if validation_report["fields_missing"] > 5:
            validation_report["overall_status"] = "incomplete"
        elif validation_report["fields_with_issues"] > 3:
            validation_report["overall_status"] = "needs_review"
        
        return validation_report


class OrangeOutputParser:
    """Parses Orange workflow Excel output"""
    
    def __init__(self, excel_path: Optional[str] = None):
        self.excel_path = excel_path
        self.data = None
        if excel_path:
            self.load_excel(excel_path)
    
    def load_excel(self, path: str):
        """Load Orange output Excel file"""
        try:
            self.data = pd.read_excel(path)
            print(f"✓ Loaded Orange output: {len(self.data)} rows")
            
            # Check for Group_Name column (combined file)
            if 'Group_Name' in self.data.columns:
                unique_groups = self.data['Group_Name'].unique()
                print(f"  Found {len(unique_groups)} group(s): {', '.join(unique_groups)}")
            
            # Validate expected columns
            required_cols = ['Field', 'Extracted_Value']
            missing_cols = [col for col in required_cols if col not in self.data.columns]
            
            if missing_cols:
                print(f"⚠️  Warning: Missing expected columns: {', '.join(missing_cols)}")
                print(f"   Available columns: {', '.join(self.data.columns)}")
            else:
                print(f"✓ Excel structure validated")
                
        except FileNotFoundError:
            print(f"✗ Error: File not found: {path}")
            print(f"   Make sure the path is correct")
        except Exception as e:
            print(f"✗ Error loading Excel: {e}")
            print(f"   Expected columns: Field, Extracted_Value, Confidence, Page_Number")
    
    def create_mock_orange_output(self, group_name: str) -> pd.DataFrame:
        """
        Create mock Orange output for testing
        In production, this would be replaced with actual Orange workflow output
        """
        # Mock data based on plan documents
        mock_data = {
            "Aurora Dynamics": {
                "Field": ["Group Name", "Group Eff Date", "TPA", "UR Vendor", "PPO Network",
                         "Min Hour Requirement", "Retirees", "BOD Directors Officers",
                         "Dependent Definitions", "Req Adding Dependents", "Dependent to Age 26",
                         "Grandchildren", "Termination Provisions", "Open Enrollment", 
                         "Leave of Absence", "Medically Necessary", "E&I", "R&C", 
                         "Workers Comp", "Transplant", "ETS Gene Therapy", "COB", "COBRA",
                         "Subrogation", "Infertility"],
                "Extracted_Value": ["Aurora Dynamics", "March 1, 2026", "BluePeak Benefits Solutions",
                                   "MedAxis Review Group", "HealthSphere Alliance", "28 hours per week",
                                   "Not Found", "Not eligible", "Legal spouse, child, domestic partner",
                                   "Within 30 days of qualifying event", "End of month child turns 26",
                                   "Not eligible unless legal guardian", "Final day of employment",
                                   "N/F", "N/F", "Services required to diagnose or treat",
                                   "Not widely accepted as standard care", 
                                   "Typical charge in geographic area $1,000 example",
                                   "Excluded", "Covered - see Transplant Benefits Section",
                                   "N/F", "Coordinates when covered by multiple plans",
                                   "18 months post-employment", "N/F", "$15,000 per family per year"],
                "Confidence": [0.95, 0.95, 0.90, 0.92, 0.93, 0.88, 0.0, 0.91, 0.89, 0.87,
                              0.90, 0.85, 0.92, 0.0, 0.0, 0.88, 0.86, 0.89, 0.93, 0.91,
                              0.0, 0.88, 0.94, 0.0, 0.87],
                "Page_Number": [1, 1, 1, 1, 1, 1, 4, 4, 9, 8, 8, 9, 4, None, None, 8, 8, 8,
                               9, 5, None, 7, 4, None, 9]
            },
            "Helios Manufacturing Inc.": {
                "Field": ["Group Name", "Group Eff Date", "TPA", "UR Vendor", "PPO Network",
                         "Min Hour Requirement", "Retirees", "BOD Directors Officers",
                         "Dependent Definitions", "Req Adding Dependents", "Dependent to Age 26",
                         "Grandchildren", "Termination Provisions", "Open Enrollment",
                         "Leave of Absence", "Medically Necessary", "E&I", "R&C",
                         "Workers Comp", "Transplant", "ETS Gene Therapy", "COB", "COBRA",
                         "Subrogation", "Infertility"],
                "Extracted_Value": ["Helios Manufacturing Inc.", "January 1, 2025", 
                                   "Sunrise Claims Administration", "Apex Medical Review Services",
                                   "StellarCare Preferred Network", "30 hours per week",
                                   "Not Found", "Not eligible", "N/F",
                                   "Within qualifying life event", "N/F", "N/F",
                                   "Last day of employment", "N/F", "N/F", "N/F", "N/F",
                                   "Typical charge in geographic area", "N/F",
                                   "Covered - $500,000 lifetime max", "N/F",
                                   "Coverage under more than one Plan", "18 months after termination",
                                   "Recover costs from third parties", "N/F"],
                "Confidence": [0.96, 0.94, 0.91, 0.90, 0.92, 0.89, 0.0, 0.90, 0.0, 0.85,
                              0.0, 0.0, 0.93, 0.0, 0.0, 0.0, 0.0, 0.88, 0.0, 0.92,
                              0.0, 0.87, 0.93, 0.89, 0.0],
                "Page_Number": [1, 1, 2, 2, 1, 4, None, 4, None, 4, None, None, 4, None,
                               None, None, None, 11, None, 6, None, 9, 4, 10, None]
            },
            "Solstice Technologies": {
                "Field": ["Group Name", "Group Eff Date", "TPA", "UR Vendor", "PPO Network",
                         "Min Hour Requirement", "Retirees", "BOD Directors Officers",
                         "Dependent Definitions", "Req Adding Dependents", "Dependent to Age 26",
                         "Grandchildren", "Termination Provisions", "Open Enrollment",
                         "Leave of Absence", "Medically Necessary", "E&I", "R&C",
                         "Workers Comp", "Transplant", "ETS Gene Therapy", "COB", "COBRA",
                         "Subrogation", "Infertility"],
                "Extracted_Value": ["Solstice Technologies", "July 1, 2026",
                                   "Summit Benefit Partners", "MedBridge Solutions",
                                   "UnityHealth Network", "32 hours per week",
                                   "Not Found", "Not eligible", "Legal spouse, domestic partner, children",
                                   "Within 30 days of qualifying event", "Coverage ends at age 26",
                                   "Not eligible unless legal guardian", "Last day of employment",
                                   "N/F", "N/F",
                                   "Services for preventing, evaluating, diagnosing, treating",
                                   "Experimental, Investigational, Unproven",
                                   "Typical charge in geographic area - R&C example",
                                   "Excluded - Workers Compensation", "Covered - see Transplant section",
                                   "N/F", "Coordination when multiple plans",
                                   "18 months post-employment", "Plan may recover from third parties",
                                   "N/F"],
                "Confidence": [0.97, 0.95, 0.92, 0.91, 0.93, 0.90, 0.0, 0.91, 0.88, 0.86,
                              0.89, 0.84, 0.92, 0.0, 0.0, 0.89, 0.87, 0.90, 0.91, 0.90,
                              0.0, 0.88, 0.94, 0.87, 0.0],
                "Page_Number": [1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6, 6, 6, None, None, 12,
                               12, None, 12, 3, None, 11, 6, 11, None]
            }
        }
        
        if group_name in mock_data:
            return pd.DataFrame(mock_data[group_name])
        else:
            print(f"⚠ No mock data for '{group_name}', creating generic template")
            return self._create_generic_template()
    
    def _create_generic_template(self) -> pd.DataFrame:
        """Create a generic template for unknown groups"""
        fields = ["Group Name", "Group Eff Date", "TPA", "UR Vendor", "PPO Network",
                 "Min Hour Requirement", "Retirees", "BOD Directors Officers",
                 "Dependent Definitions", "Req Adding Dependents", "Dependent to Age 26",
                 "Grandchildren", "Termination Provisions", "Open Enrollment",
                 "Leave of Absence", "Medically Necessary", "E&I", "R&C",
                 "Workers Comp", "Transplant", "ETS Gene Therapy", "COB", "COBRA",
                 "Subrogation", "Infertility"]
        
        return pd.DataFrame({
            "Field": fields,
            "Extracted_Value": ["N/F"] * len(fields),
            "Confidence": [0.0] * len(fields),
            "Page_Number": [None] * len(fields)
        })
    
    def get_data_for_group(self, group_name: str) -> Dict:
        """Get extracted data for a specific group"""
        if self.data is None:
            # Use mock data
            df = self.create_mock_orange_output(group_name)
        else:
            # Filter actual Orange output
            df = self.data[self.data['Group_Name'] == group_name]
        
        # Convert to dictionary
        result = {}
        for _, row in df.iterrows():
            result[row['Field']] = {
                'value': row['Extracted_Value'],
                'confidence': row.get('Confidence', 0.0),
                'page': row.get('Page_Number', None)
            }
        
        return result


class ChecklistGenerator:
    """Generates and manages checklists"""
    
    def __init__(self, definitions: DefinitionsParser, validator: Validator):
        self.definitions = definitions
        self.validator = validator
    
    def generate_checklist(self, group_name: str, orange_data: Dict, 
                          pa_data: Dict = None) -> Dict:
        """
        Generate checklist from Orange output
        
        Args:
            group_name: Name of the group/company
            orange_data: Extracted data from Orange workflow
            pa_data: Plan Administrator system data (for comparison)
        
        Returns:
            Dictionary containing checklist data and metadata
        """
        checklist = {
            "metadata": {
                "group_name": group_name,
                "generated_at": datetime.now().isoformat(),
                "generator": "AI Plan Document Review System v1.0"
            },
            "group_info": {},
            "plan_details": {},
            "validation": {}
        }
        
        # Extract group information
        for field in ["Group Name", "Group Eff Date", "TPA", "UR Vendor", 
                     "PPO Network", "Min Hour Requirement"]:
            if field in orange_data:
                checklist["group_info"][field] = {
                    "value": orange_data[field]['value'],
                    "page": orange_data[field].get('page'),
                    "confidence": orange_data[field].get('confidence', 0.0),
                    "status": self._determine_status(orange_data[field])
                }
        
        # Extract plan details
        detail_fields = ["Retirees", "BOD Directors Officers", "Dependent Definitions",
                        "Req Adding Dependents", "Dependent to Age 26", "Grandchildren",
                        "Termination Provisions", "Open Enrollment", "Leave of Absence",
                        "Medically Necessary", "E&I", "R&C", "Workers Comp", "Transplant",
                        "ETS Gene Therapy", "COB", "COBRA", "Subrogation", "Infertility"]
        
        for field in detail_fields:
            if field in orange_data:
                checklist["plan_details"][field] = {
                    "value": orange_data[field]['value'],
                    "page": orange_data[field].get('page'),
                    "confidence": orange_data[field].get('confidence', 0.0),
                    "status": self._determine_status(orange_data[field])
                }
        
        return checklist
    
    def _determine_status(self, field_data: Dict) -> str:
        """Determine field status based on extracted data"""
        value = field_data.get('value', '')
        confidence = field_data.get('confidence', 0.0)
        
        if not value or value == "N/F" or value == "Not Found":
            return "missing"
        elif confidence < 0.7:
            return "needs_review"
        else:
            return "found"
    
    def export_to_dict(self, checklist: Dict) -> Dict:
        """Export checklist to simple dictionary format"""
        export = {
            "Group_Name": checklist["metadata"]["group_name"],
            "Generated_At": checklist["metadata"]["generated_at"]
        }
        
        # Flatten group info and plan details
        for field, data in checklist["group_info"].items():
            export[field] = data["value"]
            export[f"{field}_Page"] = data["page"]
            export[f"{field}_Status"] = data["status"]
        
        for field, data in checklist["plan_details"].items():
            export[field] = data["value"]
            export[f"{field}_Page"] = data["page"]
            export[f"{field}_Status"] = data["status"]
        
        return export
    
    def generate_html_form(self, checklist: Dict, validation_report: Dict) -> str:
        """Generate editable HTML form for checklist review"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Plan Document Checklist - {checklist['metadata']['group_name']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
        }}
        .header .meta {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .validation-summary {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}
        .validation-summary.incomplete {{
            border-left-color: #e74c3c;
        }}
        .validation-summary.needs_review {{
            border-left-color: #f39c12;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .stat-box {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}
        .stat-box .number {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-box .label {{
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .section h2 {{
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .form-group {{
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            background: #fafafa;
        }}
        .form-group.missing {{
            border-left: 4px solid #e74c3c;
            background: #fff5f5;
        }}
        .form-group.needs_review {{
            border-left: 4px solid #f39c12;
            background: #fffaf0;
        }}
        .form-group.found {{
            border-left: 4px solid #27ae60;
            background: #f0fff4;
        }}
        .form-group label {{
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }}
        .form-group input, .form-group textarea {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            font-family: inherit;
            box-sizing: border-box;
        }}
        .form-group textarea {{
            min-height: 80px;
            resize: vertical;
        }}
        .field-meta {{
            display: flex;
            gap: 15px;
            margin-top: 8px;
            font-size: 13px;
            color: #666;
        }}
        .field-meta span {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .badge.missing {{
            background: #e74c3c;
            color: white;
        }}
        .badge.needs_review {{
            background: #f39c12;
            color: white;
        }}
        .badge.found {{
            background: #27ae60;
            color: white;
        }}
        .warnings {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
        }}
        .warnings h3 {{
            margin-top: 0;
            color: #856404;
        }}
        .warnings ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .warnings li {{
            margin: 5px 0;
            color: #856404;
        }}
        .suggestions {{
            background: #d1ecf1;
            border: 1px solid #17a2b8;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
        }}
        .suggestions h3 {{
            margin-top: 0;
            color: #0c5460;
        }}
        .suggestions ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .suggestions li {{
            margin: 5px 0;
            color: #0c5460;
        }}
        .button-container {{
            display: flex;
            gap: 15px;
            margin-top: 30px;
            flex-wrap: wrap;
        }}
        .btn {{
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        .btn-secondary {{
            background: #6c757d;
            color: white;
        }}
        .btn-secondary:hover {{
            background: #5a6268;
        }}
        .btn-export {{
            background: #28a745;
            color: white;
        }}
        .btn-export:hover {{
            background: #218838;
        }}
        @media print {{
            .button-container, .warnings, .suggestions {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 Plan Document Checklist</h1>
        <div class="meta">
            <strong>Group:</strong> {checklist['metadata']['group_name']}<br>
            <strong>Generated:</strong> {checklist['metadata']['generated_at']}<br>
            <strong>System:</strong> {checklist['metadata']['generator']}
        </div>
    </div>
    
    <div class="validation-summary {validation_report['overall_status']}">
        <h2>🔍 Validation Summary</h2>
        <div class="stats">
            <div class="stat-box">
                <div class="number">{validation_report['fields_found']}</div>
                <div class="label">Fields Found</div>
            </div>
            <div class="stat-box">
                <div class="number">{validation_report['fields_missing']}</div>
                <div class="label">Missing Fields</div>
            </div>
            <div class="stat-box">
                <div class="number">{validation_report['fields_with_issues']}</div>
                <div class="label">Needs Review</div>
            </div>
            <div class="stat-box">
                <div class="number">{validation_report['fields_validated']}</div>
                <div class="label">Total Fields</div>
            </div>
        </div>
        
        {self._generate_warnings_html(validation_report)}
        {self._generate_suggestions_html(validation_report)}
    </div>
    
    <form id="checklistForm">
        <div class="section">
            <h2>📊 Group Information</h2>
"""
        
        # Generate group info fields
        for field, data in checklist["group_info"].items():
            status = data.get('status', 'unknown')
            value = data.get('value', '')
            page = data.get('page', 'N/A')
            confidence = data.get('confidence', 0.0)
            
            html += f"""
            <div class="form-group {status}">
                <label>
                    {field} <span class="badge {status}">{status}</span>
                </label>
                <input type="text" 
                       name="{field}" 
                       value="{value}" 
                       data-original="{value}"
                       data-status="{status}">
                <div class="field-meta">
                    <span>📄 Page: {page}</span>
                    <span>🎯 Confidence: {confidence*100:.0f}%</span>
                </div>
            </div>
"""
        
        html += """
        </div>
        
        <div class="section">
            <h2>📝 Plan Details</h2>
"""
        
        # Generate plan details fields
        for field, data in checklist["plan_details"].items():
            status = data.get('status', 'unknown')
            value = data.get('value', '')
            page = data.get('page', 'N/A')
            confidence = data.get('confidence', 0.0)
            
            html += f"""
            <div class="form-group {status}">
                <label>
                    {field} <span class="badge {status}">{status}</span>
                </label>
                <textarea name="{field}" 
                          data-original="{value}"
                          data-status="{status}"
                          rows="3">{value}</textarea>
                <div class="field-meta">
                    <span>📄 Page: {page}</span>
                    <span>🎯 Confidence: {confidence*100:.0f}%</span>
                </div>
            </div>
"""
        
        html += """
        </div>
        
        <div class="button-container">
            <button type="button" class="btn btn-primary" onclick="generatePDF()">
                📄 Generate PDF Checklist
            </button>
            <button type="button" class="btn btn-export" onclick="exportData()">
                💾 Export Data (JSON)
            </button>
            <button type="button" class="btn btn-export" onclick="exportExcel()">
                📊 Export to Excel
            </button>
            <button type="button" class="btn btn-secondary" onclick="saveChanges()">
                💬 Save & Continue Learning
            </button>
        </div>
    </form>
    
    <script>
        // Track changes for learning
        const changes = [];
        
        document.querySelectorAll('input, textarea').forEach(field => {{
            field.addEventListener('change', function() {{
                const original = this.getAttribute('data-original');
                const newValue = this.value;
                
                if (original !== newValue) {{
                    changes.push({{
                        field: this.name,
                        original: original,
                        corrected: newValue,
                        timestamp: new Date().toISOString()
                    }});
                    
                    // Visual feedback
                    this.style.borderLeft = '3px solid #3498db';
                }}
            }});
        }});
        
        function saveChanges() {{
            if (changes.length > 0) {{
                alert(`Saving ${{changes.length}} correction(s) to learning system...`);
                console.log('Changes to learn:', changes);
                // In production, send to backend
            }} else {{
                alert('No changes to save.');
            }}
        }}
        
        function generatePDF() {{
            alert('Generating PDF checklist...');
            window.print();
        }}
        
        function exportData() {{
            const formData = new FormData(document.getElementById('checklistForm'));
            const data = {{}};
            
            for (let [key, value] of formData.entries()) {{
                data[key] = value;
            }}
            
            const json = JSON.stringify(data, null, 2);
            const blob = new Blob([json], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'checklist_data.json';
            a.click();
        }}
        
        function exportExcel() {{
            alert('Excel export would be generated here using a backend service.');
            // In production, send form data to backend for Excel generation
        }}
    </script>
</body>
</html>
"""
        
        return html
    
    def _generate_warnings_html(self, validation_report: Dict) -> str:
        """Generate warnings HTML section"""
        if not validation_report.get('warnings'):
            return ""
        
        html = '<div class="warnings"><h3>⚠️ Warnings</h3><ul>'
        for warning in validation_report['warnings'][:10]:  # Limit to 10
            html += f'<li>{warning}</li>'
        html += '</ul></div>'
        return html
    
    def _generate_suggestions_html(self, validation_report: Dict) -> str:
        """Generate suggestions HTML section"""
        if not validation_report.get('suggestions'):
            return ""
        
        html = '<div class="suggestions"><h3>💡 Suggestions</h3><ul>'
        for suggestion in validation_report['suggestions'][:10]:  # Limit to 10
            html += f'<li>{suggestion}</li>'
        html += '</ul></div>'
        return html


class PDFGenerator:
    """Generates PDF checklist from validated data"""
    
    def __init__(self):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
            from reportlab.lib.enums import TA_LEFT, TA_CENTER
            
            self.letter = letter
            self.colors = colors
            self.getSampleStyleSheet = getSampleStyleSheet
            self.ParagraphStyle = ParagraphStyle
            self.inch = inch
            self.SimpleDocTemplate = SimpleDocTemplate
            self.Table = Table
            self.TableStyle = TableStyle
            self.Paragraph = Paragraph
            self.Spacer = Spacer
            self.PageBreak = PageBreak
            self.TA_LEFT = TA_LEFT
            self.TA_CENTER = TA_CENTER
            self.available = True
        except ImportError:
            self.available = False
            print("⚠️ reportlab not installed. Install with: pip install reportlab")
    
    def generate_pdf(self, checklist: Dict, output_path: str, 
                    validation_report: Dict = None):
        """Generate PDF checklist"""
        if not self.available:
            print("✗ Cannot generate PDF - reportlab not installed")
            return False
        
        try:
            # Create PDF
            doc = self.SimpleDocTemplate(output_path, pagesize=self.letter)
            story = []
            styles = self.getSampleStyleSheet()
            
            # Title
            title_style = self.ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=self.colors.HexColor('#667eea'),
                spaceAfter=30,
                alignment=self.TA_CENTER
            )
            
            title = self.Paragraph(
                f"Plan Document Checklist<br/>{checklist['metadata']['group_name']}",
                title_style
            )
            story.append(title)
            story.append(self.Spacer(1, 0.3*self.inch))
            
            # Metadata
            metadata_data = [
                ["Generated:", checklist['metadata']['generated_at']],
                ["System:", checklist['metadata']['generator']]
            ]
            
            if validation_report:
                metadata_data.extend([
                    ["Status:", validation_report['overall_status'].upper()],
                    ["Fields Found:", str(validation_report['fields_found'])],
                    ["Missing Fields:", str(validation_report['fields_missing'])]
                ])
            
            metadata_table = self.Table(metadata_data, colWidths=[2*self.inch, 4.5*self.inch])
            metadata_table.setStyle(self.TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), self.colors.HexColor('#f0f0f0')),
                ('TEXTCOLOR', (0, 0), (-1, -1), self.colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, self.colors.grey)
            ]))
            story.append(metadata_table)
            story.append(self.Spacer(1, 0.5*self.inch))
            
            # Group Information Section
            story.append(self.Paragraph("Group Information", styles['Heading2']))
            story.append(self.Spacer(1, 0.2*self.inch))
            
            group_data = [["Field", "Value", "Page", "Status"]]
            for field, data in checklist["group_info"].items():
                group_data.append([
                    field,
                    str(data.get('value', 'N/A')),
                    str(data.get('page', 'N/A')),
                    data.get('status', 'unknown').upper()
                ])
            
            group_table = self.Table(group_data, colWidths=[2*self.inch, 2.5*self.inch, 
                                                            0.8*self.inch, 1*self.inch])
            group_table.setStyle(self._get_table_style())
            story.append(group_table)
            story.append(self.Spacer(1, 0.4*self.inch))
            
            # Plan Details Section
            story.append(self.Paragraph("Plan Details", styles['Heading2']))
            story.append(self.Spacer(1, 0.2*self.inch))
            
            details_data = [["Field", "Value", "Page", "Status"]]
            for field, data in checklist["plan_details"].items():
                details_data.append([
                    field,
                    str(data.get('value', 'N/A'))[:100],  # Truncate long values
                    str(data.get('page', 'N/A')),
                    data.get('status', 'unknown').upper()
                ])
            
            details_table = self.Table(details_data, colWidths=[2*self.inch, 2.5*self.inch,
                                                                0.8*self.inch, 1*self.inch])
            details_table.setStyle(self._get_table_style())
            story.append(details_table)
            
            # Build PDF
            doc.build(story)
            print(f"✓ PDF generated: {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error generating PDF: {e}")
            return False
    
    def _get_table_style(self):
        """Get standard table style"""
        return self.TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), self.colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [self.colors.white, self.colors.lightgrey])
        ])


class ChatbotInterface:
    """Interactive chatbot interface for the system"""
    
    def __init__(self):
        self.learning_engine = LearningEngine()
        self.definitions = DefinitionsParser({})
        self.validator = Validator(self.definitions, self.learning_engine)
        self.orange_parser = OrangeOutputParser()
        self.checklist_generator = ChecklistGenerator(self.definitions, self.validator)
        self.pdf_generator = PDFGenerator()
        self.current_checklist = None
        self.current_validation = None
    
    def print_banner(self):
        """Print welcome banner"""
        print("\n" + "="*70)
        print("🤖 AI-Enabled Plan Document Review System")
        print("="*70)
        print("📋 Automated Checklist Generation & Validation")
        print("🧠 Continuous Learning System")
        print("📄 PDF Export & Data Management")
        print("="*70 + "\n")
    
    def print_menu(self):
        """Print main menu"""
        print("\n📌 Main Menu:")
        print("1. 📊 Load Orange Output (Excel)")
        print("2. 🔨 Generate Checklist for Group")
        print("3. 🔍 Validate Current Checklist")
        print("4. 📝 Preview Checklist (HTML)")
        print("5. 📄 Export to PDF")
        print("6. 💾 Export Data (JSON/Excel)")
        print("7. 🧠 Teach Chatbot (Add Synonym/Correction)")
        print("8. 📚 View Learning History")
        print("9. 💬 Chat Mode (Ask Questions)")
        print("0. ❌ Exit")
        print()
    
    def process_group(self, group_name: str):
        """Process a group and generate checklist"""
        print(f"\n🔄 Processing group: {group_name}")
        
        # Get Orange data (mock for now)
        orange_data = self.orange_parser.get_data_for_group(group_name)
        print(f"✓ Loaded {len(orange_data)} fields from Orange output")
        
        # Generate checklist
        self.current_checklist = self.checklist_generator.generate_checklist(
            group_name, orange_data
        )
        print(f"✓ Generated checklist for {group_name}")
        
        # Validate
        checklist_simple = self.checklist_generator.export_to_dict(self.current_checklist)
        self.current_validation = self.validator.validate_checklist(checklist_simple)
        
        # Print summary
        print(f"\n📊 Validation Summary:")
        print(f"   Status: {self.current_validation['overall_status'].upper()}")
        print(f"   Fields Found: {self.current_validation['fields_found']}")
        print(f"   Missing Fields: {self.current_validation['fields_missing']}")
        print(f"   Needs Review: {self.current_validation['fields_with_issues']}")
        
        if self.current_validation['warnings']:
            print(f"\n⚠️  {len(self.current_validation['warnings'])} Warning(s)")
            for warning in self.current_validation['warnings'][:5]:
                print(f"     • {warning}")
        
        return True
    
    def preview_html(self):
        """Generate and save HTML preview"""
        if not self.current_checklist:
            print("✗ No checklist generated yet. Generate a checklist first.")
            return
        
        html_content = self.checklist_generator.generate_html_form(
            self.current_checklist,
            self.current_validation
        )
        
        output_path = f"checklist_preview_{self.current_checklist['metadata']['group_name'].replace(' ', '_')}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTML preview generated: {output_path}")
        print(f"  Open in browser to edit before PDF export")
    
    def export_pdf(self):
        """Export current checklist to PDF"""
        if not self.current_checklist:
            print("✗ No checklist generated yet. Generate a checklist first.")
            return
        
        output_path = f"checklist_{self.current_checklist['metadata']['group_name'].replace(' ', '_')}.pdf"
        
        success = self.pdf_generator.generate_pdf(
            self.current_checklist,
            output_path,
            self.current_validation
        )
        
        if success:
            print(f"✓ PDF exported: {output_path}")
    
    def export_data(self):
        """Export checklist data"""
        if not self.current_checklist:
            print("✗ No checklist generated yet. Generate a checklist first.")
            return
        
        # JSON export
        json_path = f"checklist_data_{self.current_checklist['metadata']['group_name'].replace(' ', '_')}.json"
        with open(json_path, 'w') as f:
            json.dump(self.current_checklist, f, indent=2)
        print(f"✓ JSON exported: {json_path}")
        
        # Excel export
        try:
            excel_path = f"checklist_data_{self.current_checklist['metadata']['group_name'].replace(' ', '_')}.xlsx"
            export_dict = self.checklist_generator.export_to_dict(self.current_checklist)
            df = pd.DataFrame([export_dict])
            df.to_excel(excel_path, index=False)
            print(f"✓ Excel exported: {excel_path}")
        except Exception as e:
            print(f"✗ Error exporting Excel: {e}")
    
    def teach_chatbot(self):
        """Interactive teaching mode"""
        print("\n🧠 Teaching Mode")
        print("1. Add Synonym")
        print("2. Add Correction")
        print("3. Back")
        
        choice = input("Choose option: ").strip()
        
        if choice == "1":
            term = input("Enter term: ").strip()
            synonym = input("Enter synonym: ").strip()
            user = input("Your name (optional): ").strip() or "user"
            
            self.learning_engine.add_synonym(term, synonym, user)
            print(f"✓ Learned: '{synonym}' is a synonym for '{term}'")
        
        elif choice == "2":
            incorrect = input("Enter incorrect term: ").strip()
            correct = input("Enter correct term: ").strip()
            user = input("Your name (optional): ").strip() or "user"
            
            self.learning_engine.add_correction(incorrect, correct, user)
            print(f"✓ Learned: '{incorrect}' should be '{correct}'")
    
    def view_learning_history(self):
        """View learning history"""
        history = self.learning_engine.learned_mappings.get('learning_history', [])
        
        if not history:
            print("\n📚 No learning history yet.")
            return
        
        print(f"\n📚 Learning History ({len(history)} entries):")
        for i, entry in enumerate(history[-10:], 1):  # Last 10 entries
            print(f"\n{i}. {entry['action'].upper()}")
            print(f"   Term: {entry['term']}")
            print(f"   Value: {entry['value']}")
            print(f"   User: {entry['user']}")
            print(f"   Time: {entry['timestamp']}")
    
    def chat_mode(self):
        """Interactive chat mode"""
        print("\n💬 Chat Mode (type 'exit' to return to menu)")
        print("Ask me anything about the system or current checklist!\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'back']:
                break
            
            if not user_input:
                continue
            
            # Simple keyword-based responses
            response = self._generate_response(user_input)
            print(f"🤖 Bot: {response}\n")
    
    def _generate_response(self, user_input: str) -> str:
        """Generate chatbot response"""
        user_input_lower = user_input.lower()
        
        # Status queries
        if any(word in user_input_lower for word in ['status', 'summary', 'overview']):
            if self.current_checklist:
                return f"Current checklist for {self.current_checklist['metadata']['group_name']}. " + \
                       f"Status: {self.current_validation['overall_status']}. " + \
                       f"{self.current_validation['fields_found']} fields found, " + \
                       f"{self.current_validation['fields_missing']} missing."
            else:
                return "No checklist loaded yet. Use option 2 to generate one."
        
        # Missing fields queries
        elif 'missing' in user_input_lower:
            if self.current_validation:
                missing_count = self.current_validation['fields_missing']
                return f"There are {missing_count} missing fields. Check the validation report for details."
            else:
                return "No validation data available yet."
        
        # Export queries
        elif any(word in user_input_lower for word in ['export', 'pdf', 'save']):
            return "You can export to PDF (option 5) or data formats (option 6)."
        
        # Learning queries
        elif any(word in user_input_lower for word in ['learn', 'teach', 'train']):
            return "Use option 7 to teach me new synonyms or corrections. I'll remember them!"
        
        # Help queries
        elif any(word in user_input_lower for word in ['help', 'how', 'what']):
            return "I can help you process plan documents, generate checklists, validate data, " + \
                   "and learn from corrections. Check the main menu for all options!"
        
        # Default response
        else:
            return "I'm here to help with plan document review. Try asking about status, " + \
                   "missing fields, exports, or use 'help' for more info."
    
    def run(self):
        """Main chatbot loop"""
        self.print_banner()
        
        while True:
            self.print_menu()
            choice = input("Choose an option (0-9): ").strip()
            
            if choice == "0":
                print("\n👋 Thank you for using the Plan Document Review System!")
                break
            
            elif choice == "1":
                excel_path = input("Enter Excel path (or press Enter for mock data): ").strip()
                if excel_path:
                    self.orange_parser.load_excel(excel_path)
                else:
                    print("✓ Using mock Orange data")
            
            elif choice == "2":
                print("\nAvailable groups (mock data):")
                print("  • Aurora Dynamics")
                print("  • Helios Manufacturing Inc.")
                print("  • Solstice Technologies")
                group_name = input("\nEnter group name: ").strip()
                if group_name:
                    self.process_group(group_name)
            
            elif choice == "3":
                if self.current_checklist:
                    checklist_simple = self.checklist_generator.export_to_dict(self.current_checklist)
                    self.current_validation = self.validator.validate_checklist(checklist_simple)
                    print("✓ Validation complete")
                else:
                    print("✗ No checklist to validate. Generate one first.")
            
            elif choice == "4":
                self.preview_html()
            
            elif choice == "5":
                self.export_pdf()
            
            elif choice == "6":
                self.export_data()
            
            elif choice == "7":
                self.teach_chatbot()
            
            elif choice == "8":
                self.view_learning_history()
            
            elif choice == "9":
                self.chat_mode()
            
            else:
                print("❌ Invalid option. Please try again.")


# Main execution
if __name__ == "__main__":
    chatbot = ChatbotInterface()
    chatbot.run()