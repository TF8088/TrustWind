# Trust Wind
# Made by: Tiago Farinha, Gonçalo Marinho, Bernardo Melo
# Date: 20/11/2024

import logging, os, requests, sqlite3

from flask import Flask, redirect, request, render_template, send_file, url_for, jsonify
from dotenv import load_dotenv

load_dotenv()

db = './private/db/db.db'
schemma = './private/db/schema.sql'

app = Flask(__name__, static_folder="./static")
app.url_map.strict_slashes = False

app.config['TEMPLATES_AUTO_RELOAD'] = True

logging.basicConfig(level=logging.DEBUG)

def executar_script(script_file, database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    with open(script_file, 'r') as script:
        cursor.executescript(script.read())
    conn.commit()
    conn.close()

# executar_script(schemma, db)

def get_db_connection():
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    return connection


def get_random_cities(num_cities):
    connection = get_db_connection()
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cities ORDER BY RANDOM() LIMIT ?", (num_cities,))
        return cursor.fetchall()

def fetch_weather_data(city):
    url = f"https://api.weatherapi.com/v1/current.json?key={os.getenv('API_KEY')}&q={city}&lang=pt"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        res = {
            'cidade': data['location']['name'],
            'temperatura': data['current']['temp_c'],
            'icon': data['current']['condition']['icon']
        }

        return res
    else:
        return {'erro': 'Não foi possível obter os dados'}

@app.route("/get-weather")
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    
    print(lat, lon)

    if not lat or not lon:
        return jsonify({"error": "Latitude e longitude são obrigatórios."}), 400

    weather_url = f"https://api.weatherapi.com/v1/current.json?key={os.getenv('API_KEY')}&q={lat},{lon}&lang=pt"

    response = requests.get(weather_url)

    if response.status_code == 200:
        weather_data = response.json()
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Erro ao buscar dados do clima."}), response.status_code

@app.route("/city")
def city():
    city = request.args.get('city')

    if not city:
        return redirect(url_for('error', error="001")) 
    
    url = f"https://api.weatherapi.com/v1/current.json?key={os.getenv('API_KEY')}&q={city}&lang=pt"
    
    try:
        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        if 'error' in data:
            return redirect(url_for('error', error='002'))

        user_ip = request.remote_addr

        connection = get_db_connection()
        connection.execute(
            "INSERT INTO city_req (cidade, ip) VALUES (?, ?)",
            (city, user_ip)
        )
        connection.commit()
        connection.close()

        return render_template(
            '/pages/city.html',
            title=os.getenv('TITLE'),
            city=city,
            weather=data
        )        
    except requests.exceptions.RequestException as e:
        return redirect(url_for('error', error="003"))
        
@app.route("/error")
def error():
    error_code = request.args.get('error') 

    switcher = {
        '001': 'You need to enter the name of a city.',
        '002': 'The city entered could not be found.',
        '003': 'Internal server error. Please try again later.',
    }

    error_message = {
        'error_message': switcher.get(error_code),
        'error_code': error_code
    }

    return render_template('/pages/error.html', title=os.getenv('TITLE'), error=error_message)

@app.route("/")
def index():
    
    random_cities = get_random_cities(3)
    cities_data = []
    for city in random_cities:
        city_data = fetch_weather_data(city['name'])
        cities_data.append(city_data)


    connection = get_db_connection()
    most_searched_cities = connection.execute(
        """
        SELECT cidade, COUNT(cidade) as total_searches
        FROM city_req
        GROUP BY cidade
        ORDER BY total_searches DESC
        LIMIT 3
        """
    ).fetchall()
    connection.close()

    top_cities = []

    for city in most_searched_cities:
        city_name = city['cidade']
        total_searches = city['total_searches']
        
        top_cities.append({
            'cidade': city_name,
            'pesquisas': total_searches
        })

    return render_template('/pages/index.html', title=os.getenv('TITLE'), cities=cities_data , city_shearch=top_cities)