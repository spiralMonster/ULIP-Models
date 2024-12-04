from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from datetime import datetime
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from .get_info_rail_routes_specs import GetInfoRailRoutesSpec

def GetTrainFaresAndCarbonEmission(model,source,destination):
    parser=JsonOutputParser(pydantic_object=GetInfoRailRoutesSpec)
    template="""
    There is a journey from {source} to {destination} by train.
    Your job is to provide with:
     - Total expenditure during journey in INR
     - Expected carbon emission during journey in kgs
     - Distance between the source and destination in kms
    **Note**:
     -Just provide value and nothing else.
     
    Use the following format_instructions:
    {format_instructions}
    """
    prompt=PromptTemplate.from_template(template=template,
                                        input_variable=['source','destination'],
                                        partial_variables={'format_instructions':parser.get_format_instructions()})
    chain=prompt|model|parser
    results=chain.invoke(
        {
            'source':source,
            'destination':destination
        }
    )
    return results

def GetInfoRailRoutes(model,source,destination,curr_time):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = uc.Chrome(options=options)

    url = f"https://www.google.com/search?q={source}+to+{destination}+trains&sca_esv=ffa11d673dff9c7c&sxsrf=ADLYWII5tSgRltRFbVVOi0lVoE_Z199MfQ%3A1733145886472&ei=HrVNZ---HLuM2roP1NLsiQo&ved=0ahUKEwjvxaDHl4mKAxU7hlYBHVQpO6EQ4dUDCA8&uact=5&oq=pune+to+mumbai+trains&gs_lp=Egxnd3Mtd2l6LXNlcnAaAhgCIhVwdW5lIHRvIG11bWJhaSB0cmFpbnMyCxAAGIAEGJECGIoFMgUQABiABDIFEAAYgAQyBRAAGIAEMgoQABiABBgUGIcCMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIqkdQfViWRnAFeAGQAQSYAYwCoAHML6oBBjAuMjMuObgBA8gBAPgBAZgCHqACxyaoAhHCAgoQABiwAxjWBBhHwgINEAAYgAQYsAMYQxiKBcICChAAGIAEGEMYigXCAgoQIxiABBgnGIoFwgILEAAYgAQYsQMYgwHCAggQABiABBixA8ICCxAuGIAEGLEDGOUEwgIREC4YgAQYsQMY0QMYgwEYxwHCAgcQIxgnGOoCwgITEAAYgAQYQxi0AhiKBRjqAtgBAcICFBAAGIAEGOMEGLQCGOkEGOoC2AEBwgIdEC4YgAQY0QMY4wQYtAIYxwEYyAMY6QQY6gLYAQHCAgQQIxgnwgIKEC4YgAQYJxiKBcICCxAuGIAEGLEDGIMBwgINEAAYgAQYQxiKBRiLA8ICGRAuGIAEGEMYpgMYxwEYqAMYigUYiwMYrwHCAhAQABiABBixAxhDGIoFGIsDwgIIEAAYgAQYiwPCAgsQABiABBixAxiLA8ICHBAuGIAEGEMYpgMYxwEY-AUYqAMYigUYiwMYrwHCAhQQLhiABBimAxjHARioAxiLAxivAcICERAuGIAEGKIFGKgDGIsDGJ0DwgIrEC4YgAQYQximAxjHARj4BRioAxiKBRiLAxivARiXBRjcBBjeBBjgBNgBAcICCxAuGIAEGMcBGK8BwgIKEC4YgAQY1AIYCsICBxAAGIAEGArCAg0QABiABBixAxhDGIoFwgIUEC4YgAQYsQMYgwEYxwEYigUYrwHCAg4QABiABBiRAhixAxiKBZgDB4gGAZAGCboGBggBEAEYAZIHBjUuMTguN6AHm4AC&sclient=gws-wiz-serp"


    try:
        results = {}
        driver.get(url)
        driver.implicitly_wait(30)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')

        results['Departure City']=source
        results['Arrival City']=destination

        dep_time = driver.find_elements(By.CLASS_NAME, "yfbxi")

        ind=0
        flag=0
        for i,d in enumerate(dep_time):
            train_time=d.text
            train_time=train_time.strip()
            if train_time=='':
                flag=1
                break
            else:
                time = datetime.strptime(train_time, "%H:%M").time()
                if time >= curr_time.time():
                    ind = i
                    break
        if flag==1:
            url=f"https://www.google.com/search?q=train+from+{source}+to+{destination}+on+{curr_time.date().strftime('%d-%m-%Y')}&oq=train+from+mumbai+to+chennai+on+2024-12-05&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIKCAEQABiABBiiBDIKCAIQABiABBiiBDIKCAMQABiABBiiBNIBCTIzNjQ0ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8"
            driver.get(url)
            driver.implicitly_wait(30)
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')

        train_name = driver.find_elements(By.CLASS_NAME, "B6O8xe")
        text = train_name[ind].text
        text = text.replace("\n", "")
        results['Train Name'] = text

        station_names = driver.find_elements(By.CLASS_NAME, "iQfFNc")
        text = station_names[ind].text
        text = text.split("\n")
        dep = text[0]
        arr = text[1]
        results['Departure Station'] = dep
        results['Arrival Station'] = arr

        durations = driver.find_elements(By.CLASS_NAME, "tMGvNe")
        dur = durations[ind].text
        results['Train Duration'] = dur

        dep_date = driver.find_elements(By.CLASS_NAME, "Ggd3ie")
        dep_d = dep_date[ind].text
        results['Departure Date'] = dep_d

        arr_date = driver.find_elements(By.CLASS_NAME, "ALe5qd")
        arr_d = arr_date[ind].text
        results['Arrival Date'] = arr_d

        dep_time = driver.find_elements(By.CLASS_NAME, "yfbxi")
        dep_t = dep_time[ind].text
        results['Departure Time'] = dep_t

        arr_time = driver.find_elements(By.CLASS_NAME, "OmbbVe")
        arr_t = arr_time[ind].text
        results['Arrival Time'] = arr_t

        other_info=GetTrainFaresAndCarbonEmission(model,source,destination)
        results['Total Expenditure']=other_info['expenditure']
        results['Carbon Emission']=other_info['carbon_emission']
        results['distance']=other_info['distance']

    except Exception as e:

        results = {}
        driver.get(url)
        driver.implicitly_wait(20)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')

        results['Departure City'] = source
        results['Arrival City'] = destination

        dep_time = driver.find_elements(By.CLASS_NAME, "yfbxi")

        ind = 0
        for i, d in enumerate(dep_time):
            train_time = d.text
            train_time = datetime.strptime(train_time, "%H:%M").time()
            if train_time >= curr_time.time():
                ind = i
                break

        train_name = driver.find_elements(By.CLASS_NAME, "B6O8xe")
        text = train_name[ind].text
        text = text.replace("\n", "")
        results['Train name'] = text

        station_names = driver.find_elements(By.CLASS_NAME, "iQfFNc")
        text = station_names[ind].text
        text = text.split("\n")
        dep = text[0]
        arr = text[1]
        results['Departure Station'] = dep
        results['Arrival Station'] = arr

        durations = driver.find_elements(By.CLASS_NAME, "tMGvNe")
        dur = durations[ind].text
        results['Train Duration'] = dur

        dep_date = driver.find_elements(By.CLASS_NAME, "Ggd3ie")
        dep_d = dep_date[ind].text
        results['Departure Date'] = dep_d

        arr_date = driver.find_elements(By.CLASS_NAME, "ALe5qd")
        arr_d = arr_date[ind].text
        results['Arrival Date'] = arr_d

        dep_time = driver.find_elements(By.CLASS_NAME, "yfbxi")
        dep_t = dep_time[ind].text
        results['Departure Time'] = dep_t

        arr_time = driver.find_elements(By.CLASS_NAME, "OmbbVe")
        arr_t = arr_time[ind].text
        results['Arrival Time'] = arr_t

        other_info = GetTrainFaresAndCarbonEmission(model, source, destination)
        results['Total Expenditure'] = other_info['expenditure']
        results['Carbon Emission'] = other_info['carbon_emission']
    print("Checking Railway Routes....")
    return results

if __name__=='__main__':
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key='AIzaSyD8-disvMK2_QG5guNwCJrrTg1aYYDGnkM'
    )
    curr_time=datetime.now()
    print(GetInfoRailRoutes(model,'Mumbai','Chennai',curr_time))






