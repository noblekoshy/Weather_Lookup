import requests
from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# open weather API key
api_key = "a7d7eb5bf1ec72f321958ed911cbd1da"

def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={api_key}"
    # return response, json method to convert json data to python format data
    response = requests.get(url).json()
    return response

@app.route('/', methods = ["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        city = request.form.get("city")
        r = get_weather(city)
        weather_data = {
            'city' : r['name'],
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        return weather_data

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/instructions')
def insturctions():
    return render_template('instructions.html')
    
# Listener
if __name__ == "__main__":
    app.run(debug=True)