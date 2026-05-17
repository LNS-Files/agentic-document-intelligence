from typing import Optional
from pydantic import BaseModel, Field

class BenefitPlan(BaseModel):
    plan_name: str = Field(description="Name of the health insurance plan")
    deductible: str = Field(description="Individual annual deductible")
    out_of_pocket_max: str = Field(description="Individual out-of-pocket maximum")
    emergency_room_cost: str = Field(description="Cost for an ER visit")
    primary_care_visit: str = Field(description="Cost for a primary care visit")
    specialist_visit: Optional[str] = Field(default="Not specified", description="Cost for a specialist visit")
    prescription_tier1: Optional[str] = Field(default="Not specified", description="Tier 1 prescription drug cost")
