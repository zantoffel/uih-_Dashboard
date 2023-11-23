import requests
import Config

def get_haltestellen_data():
    api_url = "https://apis.deutschebahn.com/db-api-marketplace/apis/ris-stations/v1/stop-places/by-position?latitude="+str(Config.latitude)+"&longitude="+str(Config.longitude)+"&radius=2000"
    headers = {
        "Accept" : "application/vnd.de.db.ris+json",
        "DB-Client-Id" : "a06e195b15bd6c5e98fc5b02e4ddb7cd",
        "DB-Api-Key": "78d1d1575e7e265f30d9dda7ebaaa51b"
    }

    # API-Anfrage senden
    response = requests.get(api_url, headers=headers)

    # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
    if response.status_code == 200:
        haltestellen_data_raw = response.json()

        #relevante Daten in einfaches Format
        haltestellen_data = []
        for haltestelle in haltestellen_data_raw["stopPlaces"]:
            match haltestelle["availableTransports"]:
                case ['BUS']:
                    icon = "bus"
                case ['CITY_TRAIN']:
                    icon = "rail-light"
                case _:
                    icon = "cross"

            haltestellen_data.append({
                'name':haltestelle["names"]["DE"]["nameLong"],
                'lat':haltestelle["position"]["latitude"],
                'lon':haltestelle["position"]["longitude"],
                'icon': icon,
                'evaNumber':haltestelle["evaNumber"],
            })
        return haltestellen_data
    
    else:
        print(f"Fehler beim Abrufen der Daten. Statuscode: {response.status_code}")
        return None