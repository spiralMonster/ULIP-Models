from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from .get_info_roadway_route_specs import GetRoadwayRouteInfoSpecs

def GetInfoRoadRoute(model,source,destination):
    parser = JsonOutputParser(pydantic_object=GetRoadwayRouteInfoSpecs)
    template = """
    You are given the source and destination of the route by roadways.
    Provide the given information about the route:
     - Name of the highway
     - Time required for journey
     - Distance covered
     - Expected expenditure
     - Carbon emitted

    Source:{source}
    Destination:{destination}
    Use the following format instructions:
    {format_instructions}

    *Note*: 
     -Just provide value and nothing else
    """
    prompt = PromptTemplate.from_template(template=template,
                                          input_variable=['source', 'destination'],
                                          partial_variables={'format_instructions': parser.get_format_instructions()})
    chain = prompt | model | parser
    results = chain.invoke({
        'source':source,
        'destination':destination
    })
    results['Departure City']=source
    results['Arrival City']=destination
    print("Checking Roadway Routes...")
    return results

if __name__=="__main__":
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key='AIzaSyCve8Wj4fQj52DNw9qvjzcOesPfko4D084'
    )
    results=GetInfoRoadRoute(model,'Chennai','Mumbai')
    print(results)

