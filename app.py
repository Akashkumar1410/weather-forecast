import requests
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

api_key = 'e64b608b51a997de1a5f3cb51ac15b56'

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

def get_current_weather(location):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'

    # Construct the complete URL with the location and API key
    complete_url = f"{base_url}q={location}&appid={api_key}"

    # Send a GET request to the OpenWeatherMap API
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()

        # Extract and display real-time weather data
        temperature_kelvin = data['main']['temp']
        description = data['weather'][0]['description']

        # Convert temperature to Celsius and Fahrenheit
        temperature_celsius = kelvin_to_celsius(temperature_kelvin)
        temperature_fahrenheit = kelvin_to_fahrenheit(temperature_kelvin)

        # Get the current time and format it as AM/PM
        current_time = datetime.now().strftime("%I:%M %p")

        weather_data = {
            'location': location,
            'current_time': current_time,
            'temperature_celsius': f"{temperature_celsius:.2f} °C",
            'temperature_fahrenheit': f"{temperature_fahrenheit:.2f} °F",
            'description': description,
        }

        return weather_data
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        location = request.form['location']
        weather_data = get_current_weather(location)
        if weather_data:
            return render_template('weather.html', weather_data=weather_data)
        else:
            error_message = "Error: Unable to fetch current weather data."
            return render_template('weather.html', error=error_message)

    return render_template('weather.html', weather_data=None)

if __name__ == '__main__':
    app.run(debug=True)
