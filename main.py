#
#   Trust Wind
#   Made by: Tiago Farinha, Gonçalo Marinho, Bernardo Melo
#   Date: 20/11/2024
#

import logging, os, requests, json, random

from flask import Flask, redirect, request, render_template, send_file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="./static")
app.url_map.strict_slashes = False

app.config['TEMPLATES_AUTO_RELOAD'] = True

logging.basicConfig(level=logging.DEBUG)

def get_random_cities(num_cities):
    with open('cyties.json', 'r') as f:
        cities = json.load(f)
    return random.sample(cities, num_cities)

def get_data(city):
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

    return render_template('/pages/city.html', title=os.getenv('TITLE'), city=city)

@app.route("/")
def index():
    random_cities = get_random_cities(3)

    city1 = get_data(random_cities[0])  # This line should be indented at the same level as the following lines
    city2 = get_data(random_cities[1])
    city3 = get_data(random_cities[2])

    return render_template('/pages/index.html', title=os.getenv('TITLE'),
                           city_box1=city1['cidade'], 
                           temp_box1=city1['temperatura'], 
                           icon_box1=city1['icon'],

                           city_box2=city2['cidade'], 
                           temp_box2=city2['temperatura'], 
                           icon_box2=city2['icon'],
                           
                           city_box3=city3['cidade'], 
                           temp_box3=city3['temperatura'], 
                           icon_box3=city3['icon'],
                           )
