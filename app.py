import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_weather(zipcode):
    api_key = '03d39d0a4844727881ad16a48828f5f0'
    url = f'http://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

@app.route('/<zipcode>', methods=['GET'])
def weather(zipcode):

    # Get the weather data for the provided zip code
    weather_data = get_weather(zipcode)

    if 'cod' in weather_data and weather_data['cod'] == '404':
        return jsonify({'error': 'Weather data not found'}), 404

    # Extract relevant weather information
    temperature = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']

    # Prepare the response
    response_data = {
        'zip_code': zipcode,
        'temperature': temperature,
        'description': description
    }

    # Return the weather data as JSON
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=8000)