# Trust Wind
# Made by: Tiago Farinha, Gonçalo Marinho, Bernardo Melo
# Date: 20/11/2024

import logging, os, requests, sqlite3

from flask import Flask, redirect, request, render_template, send_file
from dotenv import load_dotenv

load_dotenv()

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

# executar_script('./private/db/schema.sql', './private/db/db.db')

def get_db_connection():
    connection = sqlite3.connect('./private/db/db.db')
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


@app.route("/city")
def city():
    city = request.args.get('city')

    print(city)

    # TODO 

    return render_template('/pages/city.html', title=os.getenv('TITLE'), city=city)


@app.route("/")
def index():
    random_cities = get_random_cities(3)
    cities_data = []
    for city in random_cities:
        city_data = fetch_weather_data(city['name'])
        cities_data.append(city_data)

    return render_template('/pages/index_.html', title=os.getenv('TITLE'), cities=cities_data)