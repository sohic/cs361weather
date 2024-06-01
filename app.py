import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_coord(zipcode):
    api_key = '03d39d0a4844727881ad16a48828f5f0'
    url = f'https://api.openweathermap.org/geo/1.0/zip?zip={zipcode}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def get_current(zipcode, lat, lon):
    api_key = '03d39d0a4844727881ad16a48828f5f0'
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,alerts&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        current = data["current"]
        response_data = {
            'temperature': current["temp"],
            'description': current["weather"][0]["description"],
            'timezone': data["timezone"],
            'zipcode': zipcode
        }
        
    else:
        response_data = {
        'error': "unknown error"
    }
    return response_data

@app.route('/<zipcode>', methods=['GET'])
def weather(zipcode):

    coord_data = get_coord(zipcode)

    if 'cod' in coord_data and coord_data['cod'] == '400':
        return jsonify({'error': 'Invalid Zip Code'}), 400
    
    if 'cod' in coord_data and coord_data['cod'] == '404':
        return jsonify({'error': 'Coordinates not found'}), 404

    # Extract relevant weather information
    lat = coord_data['lat']
    lon = coord_data['lon']
    response_data = get_current(zipcode, lat, lon)
    

    # Return the weather data as JSON
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=8000)