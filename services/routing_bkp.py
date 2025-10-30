
from models.models import DecisionSpec, TraitRule
from typing import Dict, Optional
import openai
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-endpoint.openai.azure.com")
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OPENAI_KEY", "your-api-key")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "your-deployment-name")

LOG_FILE = "triage_agent_poc/ai_responses.log"



def evaluate_rule(rule: TraitRule, data: Dict) -> bool:
    value = data.get(rule.trait_target_key)
    if rule.operator == "==":
        return value == rule.value
    elif rule.operator == "!=":
        return value != rule.value
    elif rule.operator == ">":
        return value > rule.value
    elif rule.operator == "<":
        return value < rule.value
    elif rule.operator == ">=":
        return value >= rule.value
    elif rule.operator == "<=":
        return value <= rule.value
    elif rule.operator == "in":
        return value in rule.value
    elif rule.operator == "not_in":
        return value not in rule.value
    elif rule.operator == "exists":
        return rule.trait_target_key in data
    return False

def query_azure_ai(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for behavioral health triage."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response["choices"][0]["message"]["content"]
        
        return content
    except Exception as e:
        error_msg = f"Azure AI error: {str(e)}"
        
        return error_msg

def simulate_routing(spec: DecisionSpec, data: Dict) -> Optional[Dict]:
    for outcome in spec.outcomes:
        if all(evaluate_rule(rule, data) for rule in outcome.immediate_select_if):
            ai_response = query_azure_ai(outcome.description)
            return {"outcome": outcome.outcome_id, "rationale": outcome.description, "ai_response": ai_response}
    for outcome in spec.outcomes:
        if all(evaluate_rule(rule, data) for rule in outcome.decision_rules):
            ai_response = query_azure_ai(outcome.description)
            return {"outcome": outcome.outcome_id, "rationale": outcome.description, "ai_response": ai_response}
    return None
