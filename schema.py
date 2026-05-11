from pydantic import BaseModel, Field

class BenefitPlan(BaseModel):
    plan_name: str = Field(description="Name of the health insurance plan")
    deductible: str = Field(description="Individual annual deductible")
    out_of_pocket_max: str = Field(description="Individual out-of-pocket maximum")
    emergency_room_cost: str = Field(description="Cost for an ER visit")
    primary_care_visit: str = Field(description="Cost for a primary care visit")
