from pydantic import BaseModel,Field

class GetIATACodeSpecs(BaseModel):
    code : str = Field(description="Get the 3 letter IATA code for a city.")