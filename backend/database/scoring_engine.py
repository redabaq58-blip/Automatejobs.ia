"""
Deterministic Automation Scoring Engine
Hallucination-free logic engine using mathematical formulas, not LLMs.

Formula: S_task = (D * w_d + C * w_c) * P
Where:
    D = Digital Feasibility (0.0-1.0)
    C = Cognitive Routine Index (0.0-1.0)
    w_d = Weight for digital (default 0.5)
    w_c = Weight for cognitive (default 0.5)
    P = Compliance Penalty (0.0-1.0, where 0 = blocked)
"""
from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum


class AutomationTier(Enum):
    NONE = "None"           # 0-10: Cannot be automated
    LOW = "Low"             # 11-30: Minimal automation potential
    MEDIUM = "Medium"       # 31-60: Partial automation with HITL
    HIGH = "High"           # 61-85: High automation potential
    FULL = "Full"           # 86-100: Fully automatable


class RecommendedApproach(Enum):
    MANUAL_ONLY = "Manual only - No automation recommended"
    HITL_REQUIRED = "Human-in-the-loop required - Compliance mandate"
    RPA_BASIC = "Basic RPA - Rule-based automation"
    RPA_ADVANCED = "Advanced RPA - Complex workflow automation"
    LLM_ASSISTED = "LLM-assisted - AI copilot for human worker"
    LLM_FULL = "Full LLM automation - AI agent capable"
    HYBRID = "Hybrid approach - RPA + LLM combination"


@dataclass
class TaskAttributes:
    """Input attributes for scoring a task."""
    # Core attributes (1-5 scale)
    frequency_score: int = 3           # How often performed
    human_interaction_level: int = 3   # Physical/social interaction required
    cognitive_complexity: int = 3      # Mental effort required
    physical_requirement: int = 1      # Physical effort required
    
    # Boolean task characteristics
    is_routine: bool = True
    is_cognitive: bool = True
    is_digital_native: bool = False
    requires_judgment: bool = False
    requires_creativity: bool = False
    requires_physical_presence: bool = False
    
    # Data characteristics
    data_structure_score: float = 0.5  # 0.0-1.0
    decision_tree_complexity: float = 0.5  # 0.0-1.0
    error_tolerance: float = 0.5  # 0.0-1.0


@dataclass
class ComplianceConstraints:
    """Compliance rules that affect automation score."""
    hitl_required: bool = False
    human_signature_required: bool = False
    eu_ai_act_risk_level: Optional[str] = None  # "Prohibited", "High-Risk", "Limited-Risk", "Minimal"
    jurisdiction: str = "USA-Federal"


@dataclass
class AutomationScore:
    """Output of the scoring engine."""
    digital_feasibility: float
    cognitive_routine_index: float
    compliance_penalty: float
    final_score: float  # 0-100
    tier: AutomationTier
    recommended_approach: RecommendedApproach
    llm_suitability: float
    rpa_suitability: float
    confidence: float
    explanation: str


class DeterministicScoringEngine:
    """
    Pure algorithmic scoring - no LLM, no hallucination.
    Every calculation is traceable and reproducible.
    """
    
    DEFAULT_WEIGHT_DIGITAL = 0.5
    DEFAULT_WEIGHT_COGNITIVE = 0.5
    
    @classmethod
    def calculate_digital_feasibility(cls, attrs: TaskAttributes) -> float:
        """
        Calculate D (Digital Feasibility) based on task attributes.
        
        High D when:
        - Task is already digital native
        - Data is structured
        - Low physical requirements
        - High frequency (worth automating)
        """
        score = 0.0
        
        # Digital native tasks score high (0.3)
        if attrs.is_digital_native:
            score += 0.3
        
        # Data structure score (0.25)
        score += attrs.data_structure_score * 0.25
        
        # Low physical requirements boost score (0.15)
        physical_factor = (5 - attrs.physical_requirement) / 4  # 1.0 when physical=1, 0.0 when physical=5
        score += physical_factor * 0.15
        
        # No physical presence requirement (0.15)
        if not attrs.requires_physical_presence:
            score += 0.15
        
        # High frequency justifies investment (0.15)
        frequency_factor = attrs.frequency_score / 5
        score += frequency_factor * 0.15
        
        return min(score, 1.0)
    
    @classmethod
    def calculate_cognitive_routine_index(cls, attrs: TaskAttributes) -> float:
        """
        Calculate C (Cognitive Routine Index).
        
        High C when:
        - Task is routine (repetitive)
        - Low cognitive complexity
        - Doesn't require judgment/creativity
        - Decisions can be modeled as rules
        """
        score = 0.0
        
        # Routine tasks score high (0.25)
        if attrs.is_routine:
            score += 0.25
        
        # Low cognitive complexity boosts score (0.2)
        cognitive_factor = (5 - attrs.cognitive_complexity) / 4  # 1.0 when complexity=1, 0.0 when complexity=5
        score += cognitive_factor * 0.2
        
        # No judgment required (0.2)
        if not attrs.requires_judgment:
            score += 0.2
        
        # No creativity required (0.15)
        if not attrs.requires_creativity:
            score += 0.15
        
        # Decision tree complexity inverse (0.2)
        # Lower complexity = more automatable
        decision_factor = 1.0 - attrs.decision_tree_complexity
        score += decision_factor * 0.2
        
        return min(score, 1.0)
    
    @classmethod
    def calculate_compliance_penalty(cls, constraints: ComplianceConstraints) -> Tuple[float, str]:
        """
        Calculate P (Compliance Penalty).
        
        Returns 0.0 if task cannot be automated due to legal requirements.
        Returns 1.0 if no compliance restrictions.
        """
        penalty = 1.0
        reasons = []
        
        # EU AI Act: Prohibited = complete block
        if constraints.eu_ai_act_risk_level == "Prohibited":
            return 0.0, "Blocked: EU AI Act Prohibited category"
        
        # Human signature required = complete block for full automation
        if constraints.human_signature_required:
            return 0.0, "Blocked: Human signature legally required"
        
        # EU AI Act: High-Risk = significant penalty, HITL enforced
        if constraints.eu_ai_act_risk_level == "High-Risk":
            penalty *= 0.5
            reasons.append("EU AI Act High-Risk: HITL mandatory")
        
        # HITL required = 60% penalty (can still automate with human oversight)
        if constraints.hitl_required:
            penalty *= 0.6
            reasons.append("Human-in-the-loop required")
        
        # Quebec/jurisdiction-specific penalties
        if constraints.jurisdiction == "Quebec":
            # Quebec has strict professional requirements
            penalty *= 0.9
            reasons.append("Quebec jurisdiction: Professional oversight required")
        
        explanation = "; ".join(reasons) if reasons else "No compliance restrictions"
        return penalty, explanation
    
    @classmethod
    def calculate_llm_suitability(cls, attrs: TaskAttributes) -> float:
        """
        Calculate suitability for LLM-based automation.
        LLMs excel at: language tasks, reasoning, unstructured data, creative work.
        """
        score = 0.0
        
        # Cognitive tasks suit LLMs (0.3)
        if attrs.is_cognitive:
            score += 0.3
        
        # Low structure data = LLM opportunity (0.3)
        unstructured_factor = 1.0 - attrs.data_structure_score
        score += unstructured_factor * 0.3
        
        # Some creativity suits LLMs (0.2)
        if attrs.requires_creativity:
            score += 0.2
        
        # Complex decisions can use LLM reasoning (0.2)
        score += attrs.decision_tree_complexity * 0.2
        
        return min(score, 1.0)
    
    @classmethod
    def calculate_rpa_suitability(cls, attrs: TaskAttributes) -> float:
        """
        Calculate suitability for RPA automation.
        RPA excels at: routine tasks, structured data, rule-based decisions.
        """
        score = 0.0
        
        # Routine tasks suit RPA (0.3)
        if attrs.is_routine:
            score += 0.3
        
        # Digital native = easy RPA (0.25)
        if attrs.is_digital_native:
            score += 0.25
        
        # Structured data = perfect for RPA (0.25)
        score += attrs.data_structure_score * 0.25
        
        # Simple decisions suit RPA (0.2)
        simple_decision_factor = 1.0 - attrs.decision_tree_complexity
        score += simple_decision_factor * 0.2
        
        return min(score, 1.0)
    
    @classmethod
    def determine_tier(cls, final_score: float) -> AutomationTier:
        """Map final score to automation tier."""
        if final_score <= 10:
            return AutomationTier.NONE
        elif final_score <= 30:
            return AutomationTier.LOW
        elif final_score <= 60:
            return AutomationTier.MEDIUM
        elif final_score <= 85:
            return AutomationTier.HIGH
        else:
            return AutomationTier.FULL
    
    @classmethod
    def determine_approach(
        cls, 
        final_score: float, 
        llm_suit: float, 
        rpa_suit: float,
        compliance: ComplianceConstraints
    ) -> RecommendedApproach:
        """Determine recommended automation approach based on scores and compliance."""
        
        # Compliance overrides
        if compliance.human_signature_required:
            return RecommendedApproach.MANUAL_ONLY
        
        if compliance.hitl_required or compliance.eu_ai_act_risk_level == "High-Risk":
            return RecommendedApproach.HITL_REQUIRED
        
        # Score-based recommendations
        if final_score <= 10:
            return RecommendedApproach.MANUAL_ONLY
        
        if final_score <= 30:
            if llm_suit > 0.5:
                return RecommendedApproach.LLM_ASSISTED
            return RecommendedApproach.RPA_BASIC
        
        if final_score <= 60:
            if llm_suit > rpa_suit:
                return RecommendedApproach.LLM_ASSISTED
            return RecommendedApproach.RPA_ADVANCED
        
        if final_score <= 85:
            if llm_suit > 0.7 and rpa_suit > 0.5:
                return RecommendedApproach.HYBRID
            elif llm_suit > rpa_suit:
                return RecommendedApproach.LLM_FULL
            return RecommendedApproach.RPA_ADVANCED
        
        # Full automation
        if llm_suit > 0.7:
            return RecommendedApproach.LLM_FULL
        elif rpa_suit > 0.7:
            return RecommendedApproach.RPA_ADVANCED
        return RecommendedApproach.HYBRID
    
    @classmethod
    def score_task(
        cls,
        attrs: TaskAttributes,
        compliance: ComplianceConstraints,
        weight_digital: float = DEFAULT_WEIGHT_DIGITAL,
        weight_cognitive: float = DEFAULT_WEIGHT_COGNITIVE
    ) -> AutomationScore:
        """
        Main scoring function.
        
        Formula: S_task = (D * w_d + C * w_c) * P * 100
        """
        # Calculate component scores
        D = cls.calculate_digital_feasibility(attrs)
        C = cls.calculate_cognitive_routine_index(attrs)
        P, compliance_reason = cls.calculate_compliance_penalty(compliance)
        
        # Calculate LLM/RPA suitability
        llm_suit = cls.calculate_llm_suitability(attrs)
        rpa_suit = cls.calculate_rpa_suitability(attrs)
        
        # Apply formula
        raw_score = (D * weight_digital + C * weight_cognitive)
        final_score = raw_score * P * 100
        
        # Determine tier and approach
        tier = cls.determine_tier(final_score)
        approach = cls.determine_approach(final_score, llm_suit, rpa_suit, compliance)
        
        # Build explanation
        explanation_parts = [
            f"Digital Feasibility (D): {D:.2f}",
            f"Cognitive Routine Index (C): {C:.2f}",
            f"Compliance Penalty (P): {P:.2f}",
            f"Formula: ({D:.2f} * {weight_digital} + {C:.2f} * {weight_cognitive}) * {P:.2f} * 100 = {final_score:.1f}",
        ]
        if compliance_reason != "No compliance restrictions":
            explanation_parts.append(f"Compliance note: {compliance_reason}")
        
        # Confidence based on data quality
        confidence = 0.85  # Base confidence for deterministic scoring
        if attrs.is_digital_native:
            confidence += 0.05  # More confident about digital tasks
        if compliance.eu_ai_act_risk_level:
            confidence += 0.05  # Compliance data increases confidence
        
        return AutomationScore(
            digital_feasibility=D,
            cognitive_routine_index=C,
            compliance_penalty=P,
            final_score=round(final_score, 1),
            tier=tier,
            recommended_approach=approach,
            llm_suitability=round(llm_suit, 2),
            rpa_suitability=round(rpa_suit, 2),
            confidence=min(confidence, 1.0),
            explanation="\n".join(explanation_parts)
        )


# Convenience function for direct scoring
def score_task_simple(
    frequency: int = 3,
    human_interaction: int = 3,
    cognitive_complexity: int = 3,
    is_routine: bool = True,
    is_digital: bool = False,
    requires_judgment: bool = False,
    requires_creativity: bool = False,
    hitl_required: bool = False,
    eu_risk_level: Optional[str] = None,
    jurisdiction: str = "USA-Federal"
) -> dict:
    """
    Simple interface to score a task.
    Returns a dictionary with all scoring details.
    """
    attrs = TaskAttributes(
        frequency_score=frequency,
        human_interaction_level=human_interaction,
        cognitive_complexity=cognitive_complexity,
        is_routine=is_routine,
        is_digital_native=is_digital,
        requires_judgment=requires_judgment,
        requires_creativity=requires_creativity,
    )
    
    compliance = ComplianceConstraints(
        hitl_required=hitl_required,
        eu_ai_act_risk_level=eu_risk_level,
        jurisdiction=jurisdiction,
    )
    
    result = DeterministicScoringEngine.score_task(attrs, compliance)
    
    return {
        "digital_feasibility": result.digital_feasibility,
        "cognitive_routine_index": result.cognitive_routine_index,
        "compliance_penalty": result.compliance_penalty,
        "final_automation_score": result.final_score,
        "automation_tier": result.tier.value,
        "recommended_approach": result.recommended_approach.value,
        "llm_suitability": result.llm_suitability,
        "rpa_suitability": result.rpa_suitability,
        "confidence": result.confidence,
        "explanation": result.explanation,
    }
