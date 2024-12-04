from pydantic import BaseModel,Field

class GetInfoRailRoutesSpec(BaseModel):
    expenditure: int = Field(description="The expected expenditure by travelling through train in INR.")
    carbon_emission: int = Field(description="The expected carbon emission during the journey in kgs.")
    distance: int = Field(description="The distance between source and destination in kms.")