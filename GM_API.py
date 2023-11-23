import requests
import Config

url = "https://places.googleapis.com/v1/places:searchNearby"



# Replace 'YOUR_API_KEY' with your actual Google Cloud Platform API key

def get_maps_data(category):
    match category:
        case 'essen':
            types = ["bakery", "bar", "cafe", "coffee_shop", "ice_cream_shop", "restaurant"]
            icon = "restaurant"
        case 'einzelhandel':
            types = ["gift_shop", "market", "shopping_mall", "store", "supermarket", "wholesaler"]
            icon = "grocery"
        case 'parken':
            types = ["park_and_ride", "parking"]
            icon = "car"
        case 'tanken':
            types = ["electric_vehicle_charging_station", "gas_station"]
            icon = "fuel"
        case 'dienstleistungsgeschäfte':
            types = ["barber_shop", "beauty_salon", "florist", "laundry", "travel_agency", "library", "city_hall", "police", "post_office", "gym"]
            icon = "museum"
        case _:
            types = ["city_hall"]
            icon = "theatre"

    for type in types:
        #print(type)
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": Config.googleMaps_api_key,
            "X-Goog-FieldMask": "places.displayName,places.rating,places.displayName,places.location,places.displayName,places.accessibilityOptions,places.rating,places.restroom,places.servesBeer,places.priceLevel", 
        }

        data = {
            "includedTypes": [type],
            #"maxResultCount": 10,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": Config.latitude,
                        "longitude": Config.longitude,
                    },
                    "radius": 700.0,
                }
            }
        }

        # Make a POST request
        response = requests.post(url, json=data, headers=headers)
        
        #print(response.json())

        if response.status_code == 200:
            #relevante Daten in einfaches Format
            places_raw = response.json()
            #print(places_raw["places"])
            places = []
            for place in places_raw["places"]:
                places.append({
                    'name':place["displayName"]["text"],
                    'lat':place["location"]["latitude"],
                    'lon':place["location"]["longitude"],
                    'icon': icon,
                    'accessibilityOptions': place["accessibilityOptions"] if 'accessibilityOptions' in place else 'Null',                   
#                    'rating': place["rating"] if 'rating' in place else 'Null',
#                    'restroom': place["restroom"] if 'restroom' in place else 'Null',
#                    'servesBeer': place["servesBeer"] if 'servesBeer' in place else 'Null',
#                    'priceLevel': place["priceLevel"] if 'priceLevel' in place else 'Null',                  
                })
        else:
            print(f"Fehler beim Abrufen der Daten von typ{type}. Statuscode: {response.status_code}")
            return None
    return places


    

'''
curl -X POST -d '{
"includedTypes": ["restaurant"],
"maxResultCount": 1,
"locationRestriction": {
"circle": {
    "center": {
    "latitude": 49.141869,
    "longitude": 9.220195},
    "radius": 700.0
}
}
}' \
-H 'Content-Type: application/json' -H "X-Goog-Api-Key: AIzaSyBFcv9kbim4CNCkI-TRDi5PXBHxL3k8DkE" \
-H "X-Goog-FieldMask: places.displayName,places.accessibilityOptions,places.rating,places.restroom,places.servesBeer,places.priceLevel" \
https://places.googleapis.com/v1/places:searchNearby
        
'''