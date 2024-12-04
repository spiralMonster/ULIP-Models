from pydantic import BaseModel,Field
from typing import List

class BestPossibleRoutesSpecs(BaseModel):
    roadways : List = Field(description="Routes through road if possible")
    railways: List = Field(description="Routes through rail if possible")
    airways: List = Field(description="Routes through airways if possible")
    seaways: List = Field(description="Routes through seaways if possible")
