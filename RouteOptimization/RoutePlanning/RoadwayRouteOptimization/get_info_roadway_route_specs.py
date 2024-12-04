from pydantic import BaseModel,Field

class GetRoadwayRouteInfoSpecs(BaseModel):
    highway_name: str = Field(description='Name of the highway.')
    distance_covered: str = Field(description='Total distance covered in kms.')
    time_required : int =Field(description='Time required for the journey in hours.')
    expected_cost : int= Field(description='Expected cost for the journey in INR.')
    carbon_emission: int =Field(description='Expected carbon emitted during journey in kgs')