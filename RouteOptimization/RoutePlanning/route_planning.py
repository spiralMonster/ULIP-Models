from datetime import datetime
import time
from future.backports.datetime import timedelta
from langchain_google_genai import ChatGoogleGenerativeAI
from .BestPossibleRoutes.get_best_possible_routes import GetBestPossibleRoute
from .RoadwayRouteOptimization.get_info_roadway_route import GetInfoRoadRoute
from .RailwayRouteOptimization.get_info_rail_routes import GetInfoRailRoutes
from .AirwayRouteOptimization.get_airway_routes import GetInfoAirwayRoute
from .SeawayRouteOptimization.get_info_seaway_route import GetInfoSeaRoute


def PerformRoutePlanning(model,source,destination):
    routes = GetBestPossibleRoute(model, source,destination)
    ind = 1
    final_result =[]
    for route in routes:
        results=[]
        current = datetime.now()
        j=1
        time_taken = 0
        carbon = 0
        cost = 0
        for key, value in route.items():
            if key == 'roadways':
                for src_dest in value:
                    roadway_route = {}
                    roadway_route['step'] = j
                    src_dest = src_dest.split("-")
                    src = src_dest[0]
                    dest = src_dest[1]
                    route_info = GetInfoRoadRoute(model, src, dest)
                    time_to_add = timedelta(hours=1, minutes=0)
                    current = current + time_to_add
                    route_info['Departure Date'] = current.date().strftime("%d-%m-%Y")
                    route_info['Departure Time'] = current.time().strftime("%H:%M")
                    journey_time = route_info['time_required']
                    route_info['time_required'] = str(route_info['time_required']) + " hours"
                    route_info['cost'] = str(route_info['expected_cost']) + " INR"
                    route_info['carbonEmission'] = str(route_info['carbon_emission']) + " (in kgs)"

                    time_taken += int(journey_time)
                    carbon+=int(route_info['carbon_emission'])
                    cost+=int(route_info['expected_cost'])

                    time_to_add = timedelta(hours=journey_time, minutes=0)
                    current = current + time_to_add
                    route_info['Arrival Date'] = current.date().strftime("%d-%m-%Y")
                    route_info['Arrival Time'] = current.time().strftime("%H:%M")

                    roadway_route['from']=route_info['Departure City']
                    roadway_route['to']=route_info['Arrival City']
                    roadway_route['by']='road'
                    roadway_route['distance']=route_info['distance_covered']
                    roadway_route['expectedTime']=route_info['time_required']
                    roadway_route['cost']=route_info['cost']
                    roadway_route['carbonEmission']=route_info['carbonEmission']
                    roadway_route['departureDate']=route_info['Departure Date']
                    roadway_route['departureTime']=route_info['Departure Time']
                    roadway_route['arrivalDate']=route_info['Arrival Date']
                    roadway_route['arrivalTime']=route_info['Arrival Time']

                    roadway_route['remarks']={
                        'highwayName':route_info['highway_name']
                   }
                    results.append(roadway_route)
                    j+=1


            elif key == 'railways':
                for src_dest in value:
                    railway_route={}
                    railway_route['step']=j
                    src_dest = src_dest.split("-")
                    src = src_dest[0]
                    dest = src_dest[1]
                    route_info = GetInfoRailRoutes(model, src, dest, current)

                    dep = route_info['Departure Date'] + ' ' + route_info['Departure Time']
                    dep = datetime.strptime(dep, "%d %b %H:%M").replace(year=2024)
                    route_info['Departure Date'] = dep.date().strftime("%d-%m-%Y")
                    route_info['Departure Time'] = dep.time().strftime("%H:%M")

                    arr = route_info['Arrival Date'] + ' ' + route_info['Arrival Time']
                    arr = datetime.strptime(arr, "%d %b %H:%M").replace(year=2024)
                    route_info['Arrival Date'] = arr.date().strftime("%d-%m-%Y")
                    route_info['Arrival Time'] = arr.time().strftime("%H:%M")

                    route_info['cost'] = str(route_info['Total Expenditure']) + " INR"
                    route_info['carbonEmission'] = str(route_info['Carbon Emission']) + ' (in kgs)'

                    current = arr
                    railway_route['from']=route_info['Departure City']
                    railway_route['to']=route_info['Arrival City']
                    railway_route['by']='rail'
                    railway_route['distance']=route_info['distance']
                    railway_route['expectedTime']=route_info['Train Duration']
                    railway_route['cost']=route_info['cost']
                    railway_route['carbonEmission']=route_info['carbonEmission']
                    railway_route['departureDate']=route_info['Departure Date']
                    railway_route['departureTime']=route_info['Departure Time']
                    railway_route['arrivalDate']=route_info['Arrival Date']
                    railway_route['arrivalTime']=route_info['Arrival Time']
                    railway_route['remarks']={
                        'trainName':route_info['Train Name'],
                        'departureStation':route_info['Departure Station'],
                        'arrivalStation':route_info['Arrival Station']
                    }

                    cost+=int(route_info['Total Expenditure'])
                    carbon+=int(route_info['Carbon Emission'])
                    time_taken+=int(route_info['Train Duration'].split(" ")[0][:-1])

                    results.append(railway_route)
                    j+=1


            elif key == 'airways':
                for src_dest in value:
                    airway_route={}
                    time_to_add = timedelta(hours=24, minutes=0)
                    current = current + time_to_add
                    src_dest = src_dest.split("-")
                    src = src_dest[0]
                    dest = src_dest[1]
                    airway_route['step']:j
                    route_info = GetInfoAirwayRoute(model, src, dest, current.date())

                    dep = route_info['Departure Time']
                    dep = datetime.strptime(dep, "%d %b %H:%M")
                    route_info['Departure Date'] = dep.date().strftime("%d-%m-%Y")
                    route_info['Departure Time'] = dep.time().strftime("%H:%M")

                    arr = route_info['Arrival Time']
                    arr = datetime.strptime(arr, "%d %b %H:%M")
                    route_info['Arrival Date'] = arr.date().strftime("%d-%m-%Y")
                    route_info['Arrival Time'] = arr.time().strftime("%H:%M")

                    current = arr
                    airway_route['from']=route_info['Departure City']
                    airway_route['to']=route_info['Arrival City']
                    airway_route['by']='airways'
                    airway_route['distance']=str(route_info['distance'])+' kms'
                    airway_route['expectedTime']=route_info['Flight Duration']
                    airway_route['cost']=str(route_info['Expected Expenditure'])+" INR"
                    airway_route['departureDate']=route_info['Departure Date']
                    airway_route['departureTime']=route_info['Departure Time']
                    airway_route['arrivalDate']= route_info['Arrival Date']
                    airway_route['arrivalTime']=route_info['Arrival Time']
                    airway_route['remarks']={
                        'departureAirport':route_info['Departure Airport'],
                        'arrivalAirport':route_info['Arrival Airport'],
                        'airplane':route_info['Airplane'],
                        'airline':route_info['Airline']
                    }

                    cost+=int(route_info['Expected Expenditure'])
                    time_taken+=int(route_info['Flight Duration'].split(" ")[0])//60
                    results.append(airway_route)
                    j+=1


            else:

                for src_dest in value:
                    roadway_route={}
                    roadway_route['step']=j
                    src_dest = src_dest.split("-")
                    src = src_dest[0]
                    dest = src_dest[1]
                    route_info = GetInfoSeaRoute(model, src, dest)
                    time_to_add = timedelta(hours=1, minutes=0)
                    current = current + time_to_add
                    route_info['Departure Date'] = current.date().strftime("%d-%m-%Y")
                    route_info['Departure Time'] = current.time().strftime("%H:%M")
                    journey_time = route_info['time_required']
                    route_info['time_required'] = str(route_info['time_required']) + " (in hours)"
                    route_info['cost'] = str(route_info['expected_cost']) + " (in INR)"
                    route_info['carbonEmission'] = str(route_info['carbon_emission']) + " (in kgs)"
                    time_to_add = timedelta(hours=journey_time, minutes=0)
                    current = current + time_to_add
                    route_info['Arrival Date'] = current.date().strftime("%d-%m-%Y")
                    route_info['Arrival Time'] = current.time().strftime("%H:%M")

                    roadway_route['from'] = route_info['source_port_name']
                    roadway_route['to'] = route_info['destination_port_name']
                    roadway_route['by'] = 'road'
                    roadway_route['distance'] = route_info['distance_covered']
                    roadway_route['expectedTime'] = route_info['time_required']
                    roadway_route['cost'] = route_info['cost']
                    roadway_route['carbonEmission'] = route_info['carbonEmission']
                    roadway_route['departureDate'] = route_info['Departure Date']
                    roadway_route['departureTime'] = route_info['Departure Time']
                    roadway_route['arrivalDate'] = route_info['Arrival Date']
                    roadway_route['arrivalTime'] = route_info['Arrival Time']
                    roadway_route['remarks']={
                        'ferryName':route_info['ferry_name']
                    }

                    results.append(roadway_route)
                    time_taken+=int(route_info['time_required'])
                    carbon+=int(route_info['carbon_emission'])
                    cost+=int(route_info['expected_cost'])



        inst={
            'routeId':f"route{ind}",
            'steps':results,
            'totalCarbonEmission':str(carbon)+" kgs",
            'totalTimeTaken':str(time_taken)+" hours",
            'totalCost':str(cost)+" INR",
            'expectedDelivery':current.date().strftime("%d-%m-%Y")
        }
        final_result.append(inst)
        print(f"Route {ind} is completed..")
        ind += 1
        time.sleep(20)
    output={
        'deliveryRoutes':final_result
    }
    return output


if __name__=='__main__':
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key='AIzaSyBG_cGBRTmDLav1t_6Zb7q4Hp7pnlTLlMw'
    )
    source=input('Enter source city: ')
    destination=input('Enter destination city: ')
    results=PerformRoutePlanning(model,source,destination)
    print(results)




