import requests

def get_weather_data():
    api_url = "https://api.open-meteo.com/v1/forecast?latitude=49.1399&longitude=9.2205&hourly=temperature_2m,precipitation,wind_speed_10m&forecast_days=3"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Wirft eine HTTPError-Exception für fehlgeschlagene Anfragen
        json_data = response.json()

        transformed_data = []

        for i in range(len(json_data["hourly"]["time"])):
            entry = {
                "time": json_data["hourly"]["time"][i],
                "temperature": json_data["hourly"]["temperature_2m"][i],
                "rain_amount": json_data["hourly"]["precipitation"][i],
                "wind_speed": json_data["hourly"]["wind_speed_10m"][i]
            }
            transformed_data.append(entry)

        return transformed_data

    except requests.exceptions.RequestException as err:
        print(f"Fehler beim Abrufen der Daten von der API: {err}")
        return None