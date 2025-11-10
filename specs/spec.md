
# Feature Specification: Dynamic Decision Routing – Config Management & Test API
**Feature ID**: spike-dynamic-routing-config  
**Created**: 2025-11-05 
**Status**: DISCOVERY / POC  
**Target Release**: TBD  

## Executive Summary
This spike explores a Python-based configuration management and test API for Dynamic Decision Routing. The goal is to validate a pattern for maintaining and testing routing configurations (DecisionSpecs) across multiple flows without requiring code changes for each program.  

**Key Value**:  
- Enable configuration-driven routing logic for triage agents (e.g., Behavioral Health / Likemind).  
- Reduce engineering overhead by decoupling routing logic from application code.  
- Provide safe “test mode” for simulation without persisting data.  

## User Story
**As a Developer**, I need to research and prototype a Python-based configuration management and test API for Dynamic Decision Routing so that we can determine the feasibility of supporting configuration-driven routing logic (DecisionSpecs) across multiple FIGMA-style flows without requiring code changes for each program.

## Functional Details
- Validate approach for creating, versioning, and managing DecisionSpecs in the existing Python triage repository.
- Implement FastAPI endpoints for:
  - Listing specs
  - Saving new versions
  - Validating specs
  - Simulating routing decisions in test mode
  - Publishing specs
- Confirm runtime usage of DecisionSpecs from Cosmos DB without code changes.
- Ensure “test mode” simulates routing decisions safely without writing to Cosmos DB.

## Expected Outputs
- Working POC for Triage API
- Python Pydantic models for:
  - TraitQuestion
  - TraitRule
  - OutcomeDefinition
  - DecisionSpec
- Simulation endpoint demonstrating test mode functionality
- Findings and recommendations for scaling to other service lines

## Technical Details
**Implementation Tech**:
- Python (FastAPI)
- Azure Cosmos DB for config storage (draft, active, retired)
- Existing triage repository

**Implementation Steps**:
- Develop sample `BH_ROUTING_LIKEMIND_V1` DecisionSpec for testing.
- Validate “test mode” can evaluate outcomes and identify missing traits without writing to Cosmos.
- Deliver findings report and recommendation for production readiness.

## Functional Requirements
### FR-1: DecisionSpec Management
**Description**: Create, validate, and version DecisionSpecs in Python repository.  
**Acceptance Criteria**:
- Specs stored in Cosmos DB with status: draft, active, retired.
- Versioning enforced via `spec_id` + `version`.
- Validation endpoint checks schema compliance using Pydantic.

### FR-2: FastAPI Endpoints
| Endpoint                | Purpose                                      |
|-------------------------|----------------------------------------------|
| `GET /specs`           | List available DecisionSpecs                |
| `POST /specs`          | Save a new DecisionSpec version             |
| `POST /specs/validate` | Validate a DecisionSpec                     |
| `POST /specs/simulate` | Run test-mode simulation with mock trait data|
| `POST /specs/publish`  | Mark a spec version as active               |
| `GET /specs/{spec_id}` | Retrieve a specific spec                    |

### FR-3: Simulation Mode
**Description**: Evaluate routing decisions without persisting data.  
**Acceptance Criteria**:
- Accept mock trait data in request body.
- Return predicted outcome and missing traits.
- Do not write to Cosmos DB during simulation.

### FR-4: Runtime Integration
**Description**: Triage agents load DecisionSpecs dynamically from Cosmos DB.  
**Acceptance Criteria**:
- No code changes required for new routing logic.
- Agents read `DecisionSpec` from Cosmos DB at runtime.

## Success Criteria
- POC demonstrates configuration-driven routing logic.
- Simulation endpoint validates outcomes and identifies missing traits.
- Findings report includes recommendation for production readiness.

## Assumptions
- Cosmos DB available for config storage.
- Existing triage repository supports integration.
- LLM agent layer can be extended for question phrasing.

## Dependencies
- Azure Cosmos DB
- FastAPI
- Pydantic models
- Existing triage orchestration layer

## Next Steps
- Build POC endpoints.
- Implement sample DecisionSpec.
- Validate simulation mode.
- Document findings and recommendations.

## Sample DecisionSpec JSON
```json
{
  "spec_id": "BH_ROUTING_LIKEMIND_V1",
  "version": "1.0.0",
  "intent": "BEHAVIORAL_HEALTH_ROUTING",
  "business_goal": "Route user to Likemind, BH Assisted, or BH Self-Service",
  "traits": [
    {
      "trait_target_key": "bh_has_active_likemind_care_plan",
      "question_text": "Are you currently enrolled in a Likemind care plan?",
      "answer_type": "yes_no"
    },
    {
      "trait_target_key": "bh_needs_assisted_support",
      "question_text": "Would you prefer to speak with a behavioral health specialist?",
      "answer_type": "yes_no"
    }
  ],
  "outcomes": [
    {
      "outcome_id": "LIKEMIND_DASHBOARD_CONNECT",
      "label": "Likemind Dashboard",
      "description": "User is enrolled in Likemind",
      "immediate_select_if": [
        {
          "trait_target_key": "bh_has_active_likemind_care_plan",
          "operator": "==",
          "value": true
        }
      ],
      "decision_rules": [],
      "resolution_text": "Access your Likemind dashboard",
      "resolution_button_label": "Go to Dashboard",
      "resolution_button_url": "https://likemind.example.com/dashboard",
      "analytics_resolution_code": "LM_CONNECT"
    },
    {
      "outcome_id": "BH_ASSISTED_SUPPORT",
      "label": "Assisted Support",
      "description": "User prefers assisted support",
      "immediate_select_if": [],
      "decision_rules": [
        {
          "trait_target_key": "bh_needs_assisted_support",
          "operator": "==",
          "value": true
        }
      ],
      "resolution_text": "Connect with a behavioral health specialist",
      "resolution_button_label": "Get Support",
      "resolution_button_url": "https://bh.example.com/support",
      "analytics_resolution_code": "BH_ASSIST"
    },
    {
      "outcome_id": "BH_SELF_SERVICE",
      "label": "Self-Service",
      "description": "Default outcome for self-service",
      "immediate_select_if": [],
      "decision_rules": [],
      "resolution_text": "Explore self-service behavioral health resources",
      "resolution_button_label": "Explore Resources",
      "resolution_button_url": "https://bh.example.com/resources",
      "analytics_resolution_code": "BH_SELF"
    }
  ],
  "safety_preamble": "You are assisting with behavioral health navigation. Ask only one question at a time. Do not diagnose. Be calm and supportive."
}
```

> Note: Resolution text may be dynamically generated using Azure OpenAI based on trait context and outcome.
