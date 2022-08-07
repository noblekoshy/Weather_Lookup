import requests
from flask import Flask, request, redirect, render_template, url_for, flash, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# open weather API key
api_key = "a7d7eb5bf1ec72f321958ed911cbd1da"

def get_weather_city(city):
    # reference https://openweathermap.org/current#name
    # note: lookup by city name will be deprecated soon. Look into geocoding API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}"
    # return response, json method to convert json data to python format data
    response = requests.get(url).json()
    return response

def get_weather_coord(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={api_key}"
    # return response, json method to convert json data to python format data
    response = requests.get(url).json()
    return response

def reverse_geocoding(lat, lon):
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit={1}&appid={api_key}"
    # return response, json method to convert json data to python format data
    response = requests.get(url).json()
    return response

@app.route('/', methods = ["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        if request.form.get("city"):
            city = request.form.get("city")
            r = get_weather_city(city)
            # dict of select weather data
            weather = {
                'city' : r['name'],
                'country' : r['sys']['country'],
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon']
            }
            return render_template('weather.html', weather = weather)

        if request.form.get("random_city"):
            r = requests.get("http://127.0.0.1:5001")
            return render_template('index.html', random_city=r.text)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/instructions')
def insturctions():
    return render_template('instructions.html')

@app.route('/geo', methods= ['GET', 'POST'])
def geo():
    if request.method == "GET":
        return render_template('geo.html')
    if request.method == "POST":
        geo_data = request.get_json()
        #return jsonify(data)
        if geo_data:
            lat = geo_data['location']['lat']
            lon = geo_data['location']['lng']
            r = get_weather_coord(lat, lon)
            # dict of select weather data
            weather = {
                'city' : r['name'],
                'country' : r['sys']['country'],
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon']
            }
            print(weather)
            # TODO not displaying the weather page, due to POST on geo/ ? how does regular weather work? 
            # TODO try just getting the city name by reverse geocoding, wouldnt work for Rosvile MN vs CA
            return render_template('weather.html', weather = weather)
    
# Listener
if __name__ == "__main__":
    app.run(debug=True)