
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from .get_IATA_code_specs import GetIATACodeSpecs



def GetIATACode(model,city):
    parser=JsonOutputParser(pydantic_object=GetIATACodeSpecs)
    template="""
    You are given city name.Provide the 3-letter IATA code for the city.
    City name: {city}
    Use the following format instructions:
    {format_instructions}
    **Note**:
     -Just give the code and nothing else.
    """

    prompt=PromptTemplate.from_template(template=template,
                                        input_variable=['city'],
                                        partial_variables={'format_instructions':parser.get_format_instructions()})
    chain=prompt|model|parser
    results=chain.invoke({
        'city':city
    })
    return results

if __name__=='__main__':
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key='AIzaSyD8-disvMK2_QG5guNwCJrrTg1aYYDGnkM'
    )
    results = GetIATACode(model,'Mumbai')
    print(results)