from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel,Field

class GetDistanceBtwCitiesSpecs(BaseModel):
    distance: int =Field(description="Distance between two cities in kms.")

def GetDistanceBtwCities(model,source,destination):
    parser=JsonOutputParser(pydantic_object=GetDistanceBtwCitiesSpecs)

    template="""
    Find the distance between {source} and {destination} in kms.
    Use the following format_instructions:
    {format_instructions}
    **Note**:
     -Just give single value and nothing else.
    """
    prompt=PromptTemplate.from_template(template=template,
                                        input_variable=['source','destination'],
                                        partial_variables={'format_instructions':parser.get_format_instructions()})

    chain=prompt|model|parser
    results=chain.invoke({
        'source':source,
        'destination':destination
    })
    return results