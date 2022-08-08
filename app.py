import string
import json
import requests
from flask import Flask, request, redirect, render_template, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)

api_key = "a7d7eb5bf1ec72f321958ed911cbd1da"

def get_weather_city(city):
    # reference https://openweathermap.org/current#name
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}"
    response = requests.get(url).json()
    return response

def get_weather_coord(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={api_key}"
    response = requests.get(url).json()
    return response

def reverse_geocoding(lat, lon):
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit={1}&appid={api_key}"
    response = requests.get(url).json()
    return response

@app.route('/', methods = ["POST", "GET"])
def index():
    if request.method == "GET":
        cities = City.query.all()
        weather_data = []
        for city in cities:
            print(city.name)
            r = get_weather_city(city.name)
            weather = {
                'city' : r['name'],
                'country' : r['sys']['country'],
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon']
            }
            weather_data.append(weather)
        return render_template('index.html', weather_data = weather_data)

    if request.method == "POST":
        if request.form.get("city"):
            city = request.form.get("city")
            city = city.lower()
            city = string.capwords(city)

        elif request.form.get("random_city"):
            r = requests.get("http://127.0.0.1:5001")
            city = r.text

        if city:
            r = get_weather_city(city)
            new_city_obj = City(name=city)
            db.session.add(new_city_obj)
            db.session.commit()
            weather = {
                'city' : r['name'],
                'country' : r['sys']['country'],
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon']
            }
            return redirect(url_for('index'))
            #return render_template('weather.html', weather = weather)
        
@app.route('/geolocation', methods = ["POST"])
def geolocation():
    if request.method == "POST":
        geo_data = request.get_json()
        lat = geo_data['location']['lat']
        lon = geo_data['location']['lng']
        r = reverse_geocoding(lat, lon)
        city = r[0]['name']
        if city:
            new_city_obj = City(name=city)
            db.session.add(new_city_obj)
            db.session.commit()
        return redirect(url_for('index'))

@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/instructions')
def insturctions():
    return render_template('instructions.html')

# Listener
if __name__ == "__main__":
    app.run(debug=True)