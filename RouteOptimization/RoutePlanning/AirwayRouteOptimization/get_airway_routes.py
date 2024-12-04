from serpapi.google_search import GoogleSearch
from langchain_google_genai import ChatGoogleGenerativeAI
from .get_IATA_code import GetIATACode
from .get_distance_between_cities import GetDistanceBtwCities
from datetime import datetime,timedelta

def GetInfoAirwayRoute(model,dep_city,arr_city,date):
  dep_id = GetIATACode(model, dep_city)['code']
  arr_id = GetIATACode(model, arr_city)['code']
  params = {
    "engine": "google_flights",
    "departure_id": dep_id,
    "arrival_id": arr_id,
    "outbound_date": date,
    "type": "2",
    "currency": "INR",
    "hl": "en",
    "api_key": "0f2a817e7c3c9611960278ea9b89bf10398f53df74953a5dc6f32fa58c72a41e"
  }

  search = GoogleSearch(params)
  results = search.get_dict()
  output = {}
  best_flights = results['best_flights'][0]
  dep_air_name = best_flights['flights'][0]['departure_airport']['name']
  dep_time = best_flights['flights'][0]['departure_airport']['time']
  arr_air_name = best_flights['flights'][0]['arrival_airport']['name']
  arr_time = best_flights['flights'][0]['arrival_airport']['time']
  flight_duration = best_flights['flights'][0]['duration']
  airplane = best_flights['flights'][0]['airplane']
  airline = best_flights['flights'][0]['airline']
  carbon_emission = best_flights['carbon_emissions']['this_flight']/1000
  expend=best_flights['price']

  output['distance']=GetDistanceBtwCities(model,dep_city,arr_city)['distance']
  output['Departure City']=dep_city
  output['Arrival City']=arr_city
  output['Departure Airport'] = dep_air_name
  output['Arrival Airport'] = arr_air_name
  output['Departure Time'] = dep_time
  output['Arrival Time'] = arr_time
  output['Flight duration'] = str(flight_duration) + " minutes"
  output['Airplane'] = airplane
  output['Airline'] = airline
  output['Expected Carbon Emission'] = str(carbon_emission)+" kgs"
  output['Expected Expenditure']=int(expend)
  print("Checking Airway Routes.....")
  return output

if __name__=='__main__':
  model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    api_key='AIzaSyBJBdBSWeIiba3zG2TEx6qEXfWuWvFcH8M'
  )
  time_to_add=timedelta(hours=24,minutes=0)
  date=(datetime.now()+time_to_add).date()
  result=GetInfoAirwayRoute(model,'Mumbai','Chennai',date)
  print(result)