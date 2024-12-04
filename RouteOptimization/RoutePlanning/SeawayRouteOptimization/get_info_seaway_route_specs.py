from pydantic import BaseModel,Field

class GetSeawayRouteInfoSpecs(BaseModel):
    source_port_name: str = Field(description='Name of the source port.')
    destination_port_name: str = Field(description='Name of the destination port.')
    ferry_name : str =Field(description='Name of the ferry.')
    distance_covered: str = Field(description='Total distance covered in kms.')
    time_required : int =Field(description='Time required for the journey in hours.')
    expected_cost : int= Field(description='Expected cost for the journey in INR.')
    carbon_emission: int =Field(description='Expected carbon emitted during journey in kgs')