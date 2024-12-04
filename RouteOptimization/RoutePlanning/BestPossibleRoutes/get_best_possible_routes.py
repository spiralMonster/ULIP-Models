from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from .get_best_possible_routes_specs import BestPossibleRoutesSpecs



def GetBestPossibleRoute(model,source,destination):
    parser = JsonOutputParser(pydantic_object=BestPossibleRoutesSpecs)

    template = """
    You are given a source and a destination city.
    Your job is to give me 3 best route.
    The routes can contain roadways,railways,airways and seaways.

    Source:
    {source}
    Destination:
    {destination}

    The output should be as follows:
    {output_format}

    Use the following format instructions:
    {format_instructions}

    *Note*:
      -If no route is possible then leave the list empty.
      -And just provide the route and nothing else.
      -Use airways only when the cities cannot be reached by road,rail and seaways.
      -Use at least 2 modes of transport in your route.
      -Use 2-3 destinations in your route.
      -You can change the placing of modes of transport in the output.If the first route is by train then place railways at
       first and so on.

    """

    output_format = """
    [
      {
       roadways:[CityA-CityB,CityK-CityM],
       seaways:[CityD-CityE],
       airways:[CityM-cityN],
       railways:[cityQ-cityR]
       }
    ]
    """

    prompt = PromptTemplate.from_template(template=template,
                                          input_variable=['source', 'destination', 'output_format'],
                                          partial_variables={'format_instructions': parser.get_format_instructions()})

    chain = prompt | model | parser

    results = chain.invoke({'source': source, 'destination': destination, 'output_format': output_format})
    print('Best routes are found...')
    return results

if __name__=='__main__':
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key='AIzaSyD8-disvMK2_QG5guNwCJrrTg1aYYDGnkM'
    )
    results=GetBestPossibleRoute(model,'Chennai','Mumbai')
    print(results)

