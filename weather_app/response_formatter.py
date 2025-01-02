DIRECTIONS = {
    "N": "North",
    "E": "East",
    "S": "South",
    "W": "West",

    }

def format_response(data: dict) -> dict:
    formatted_data = {
        "location": data['location']['name'],
        "region": data['location']['region'],
        "time": data['location']['localtime'],
        "timezone": data['location']['tz_id'],
        "latitude": data['location']['lat'],
        "longitude": data['location']['lon'],
        "temperature_c": data['current']['temp_c'],
        "temperature_f": data['current']['temp_f'],
        "condition": data['current']['condition']['text'],
        "icon": data['current']['condition']['icon'],
        "feels_like_c": data['current']['feelslike_c'],
        "feels_like_f": data['current']['feelslike_f'],
        "wind_kph": data['current']['wind_kph'],
        "wind_mph": data['current']['wind_mph'],
        "wind_direction": " ".join([DIRECTIONS[direction] for direction in list((data['current']['wind_dir']))]),
        "humidity": data['current']['humidity'],    
        "cloud": data['current']['cloud'],
        "precip_mm": data['current']['precip_mm'],
        "pressure_mb": data['current']['pressure_mb'],
        "uv": data['current']['uv'],
        "visibility_km": data['current']['vis_km'],
        "visibility_miles": data['current']['vis_miles'],
        "last_updated": data['current']['last_updated'],
        "heat_index_c": data['current']['heatindex_c'],
        "heat_index_f": data['current']['heatindex_f'],
        "gust_kph": data['current']['gust_kph'],
        "gust_mph": data['current']['gust_mph'],

    }
    return formatted_data