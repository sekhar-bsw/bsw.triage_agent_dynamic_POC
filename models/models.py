
from typing import List, Dict, Literal, Optional, Any
from pydantic import BaseModel, Field

class TraitQuestion(BaseModel):
    trait_target_key: str
    question_text: str
    answer_type: Literal["yes_no", "number", "enum", "text"] = "yes_no"
    parse_hint: Optional[str] = None

class TraitRule(BaseModel):
    trait_target_key: str
    operator: Literal["==","!=",">","<",">=","<=","in","not_in","exists"]
    value: Any
    required_confidence: float = 0.9

class OutcomeDefinition(BaseModel):
    outcome_id: str
    label: str
    description: str
    immediate_select_if: List[TraitRule] = Field(default_factory=list)
    decision_rules: List[TraitRule]
    resolution_text: str
    resolution_button_label: Optional[str] = None
    resolution_button_url: Optional[str] = None
    analytics_resolution_code: Optional[str] = None

class DecisionSpec(BaseModel):
    spec_id: str
    version: str
    intent: str
    business_goal: str
    traits: List[TraitQuestion]
    outcomes: List[OutcomeDefinition]
    safety_preamble: str = Field(default="You are assisting with behavioral health navigation. Ask only one question at a time. Do not diagnose. Be calm and supportive.")
