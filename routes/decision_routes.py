
from fastapi import APIRouter, HTTPException
from models.models import DecisionSpec
from services.routing import simulate_routing
import os, json

router = APIRouter(prefix="/specs", tags=["Decision Specs"])

@router.get("/")
def list_specs():
    files = os.listdir("configs")
    return [f.replace(".json", "") for f in files if f.endswith(".json")]

@router.post("/")
def save_spec(spec: DecisionSpec):
    path = f"configs/{spec.spec_id}.json"
    with open(path, "w") as f:
        json.dump(spec.dict(), f, indent=2)
    return {"message": "Spec saved", "spec_id": spec.spec_id}

@router.post("/validate")
def validate_spec(spec: DecisionSpec):
    return {"message": "Spec is valid", "spec_id": spec.spec_id}

@router.post("/simulate/{spec_id}")
def simulate_spec(spec_id: str, trait_data: dict):
    path = f"configs/{spec_id}.json"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Spec not found")
    with open(path, "r") as f:
        spec_data = json.load(f)
    spec = DecisionSpec(**spec_data)
    result = simulate_routing(spec, trait_data)
    if result:
        return result
    raise HTTPException(status_code=404, detail="No matching outcome found")

@router.post("/publish")
def publish_spec(spec_id: str):
    return {"message": f"Spec {spec_id} published"}

@router.get("/{spec_id}")
def get_spec(spec_id: str):
    path = f"configs/{spec_id}.json"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Spec not found")
    with open(path, "r") as f:
        return json.load(f)
