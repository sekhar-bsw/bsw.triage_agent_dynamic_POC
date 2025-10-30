
## 🔄 New Simulation Endpoint

### `POST /specs/simulate/{spec_id}`
This endpoint automatically loads the spec from the `configs/` folder using the `spec_id` path parameter.

### ✅ Example Usage
**Endpoint**:
```
/specs/simulate/BH_ROUTING_LIKEMIND_V1
```

**Request Body**:
```json
{
  "bh_has_active_likemind_care_plan": true
}
```

**Expected Outcome**:
```json
{
  "outcome": "LIKEMIND_DASHBOARD_CONNECT",
  "rationale": "User is enrolled in Likemind",
  "ai_response": "..."
}
```

You no longer need to send the full spec in the request body.
