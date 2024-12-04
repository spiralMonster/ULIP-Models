from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .get_info_seaway_route_specs import GetSeawayRouteInfoSpecs
from langchain_google_genai import ChatGoogleGenerativeAI

def GetInfoSeaRoute(model,source,destination):
    parser = JsonOutputParser(pydantic_object=GetSeawayRouteInfoSpecs)
    template = """
    You are given the source and destination of the route by seaways.
    Provide the given information about the route:
     - Source Port name
     - Destination Port name
     - Ferry name
     - Time required for journey
     - Distance covered
     - Expected expenditure
     - Carbon emitted

    Source:{source}
    Destination:{destination}
    Use the following format instructions:
    {format_instructions}

    *Note*: 
     -Just provide the value and nothing else.
    """
    prompt = PromptTemplate.from_template(template=template,
                                          input_variable=['source', 'destination'],
                                          partial_variables={'format_instructions': parser.get_format_instructions()})
    chain = prompt | model | parser
    results = chain.invoke({
        'source':source,
        'destination':destination
    })
    print("Checking Seaway Routes......")
    return results

if __name__=='__main__':
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key='AIzaSyD8-disvMK2_QG5guNwCJrrTg1aYYDGnkM'
    )
    results=GetInfoSeaRoute(model,'Chennai','Mumbai')
    print(results)
