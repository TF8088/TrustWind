# Trust Wind
# Made by: Tiago Farinha, Gonçalo Marinho, Bernardo Melo
# Date: 20/11/2024

import logging, os, requests, sqlite3, random, string
from flask import Flask, redirect, request, render_template, url_for, jsonify, session
from flask_mail import Mail, Message
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()

db = './private/db/db.db'
schemma = './private/db/schema.sql'
sessions_path = './private/sessions/'
email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

app = Flask(__name__, static_folder="./static")
app.url_map.strict_slashes = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_FILE_DIR'] = sessions_path 
app.config['SESSION_PERMANENT'] = False  
app.config['SESSION_USE_SIGNER'] = True  
app.config['SESSION_FILE_THRESHOLD'] = 5  
app.config['PERMANENT_SESSION_LIFETIME'] = 300

app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
Session(app)

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
    url = f"https://api.weatherapi.com/v1/current.json?key={os.getenv('API_KEY')}&q={city}&lang=en"
   
    try:
        response = requests.get(url)
        
        response.raise_for_status()
        
        data = response.json()

        res = {
            'cidade': data['location']['name'],
            'temperatura': data['current']['temp_c'],
            'icon': data['current']['condition']['icon']
        }

        return res
    except requests.exceptions.RequestException as e:
        return redirect(url_for('error', error="003"))
      
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=4))

def send_verification_email(email, verification_code):

    verification_url = f"http://localhost/verify?email={email}&verification_code={verification_code}"
    
    try:
        email_body = f"""
        <p>Dear User,</p>
        <p>Thank you for signing up. Please click the button below to verify your account:</p>
        <form action="{verification_url}" method="POST" style="margin: 20px 0;">
            <input type="hidden" name="email" value="{email}">
            <input type="hidden" name="verification_code" value="{verification_code}">
            <button type="submit" style="padding: 10px 20px; font-size: 16px; color: #ffffff; background-color: #007bff; text-decoration: none; border-radius: 5px; border: none; cursor: pointer;">Verify My Account</button>
        </form>
        <p>If the button doesn't work, please copy and paste the following link into your browser:</p>
        <p><a href="{verification_url}">{verification_url}</a></p>
        <p>Thank you,<br>The TrustWind Team</p>
        """

        msg = Message(
            subject="Verify Your Account",
            sender=os.getenv('MAIL_USERNAME'),
            recipients=[email],
            html=email_body
        )

        mail.send(msg)

    except Exception as e:
        print(f"Failed to send verification email: {e}")
        return redirect(url_for('error', error="009"))

@app.route("/get-weather")
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
         return redirect(url_for('error', error="001"))

    weather_url = f"https://api.weatherapi.com/v1/current.json?key={os.getenv('API_KEY')}&q={lat},{lon}&lang=en"

    try: 
        response = requests.get(weather_url)
        
        response.raise_for_status()

        weather_data = response.json()
        
        return jsonify(weather_data)

    except requests.exceptions.RequestException as e:
        return redirect(url_for('error', error="003"))
    
@app.route("/city")
def city():
    city = request.args.get('city')

    current_time = datetime.now().strftime('%H:%M')

    print(current_time)
    
    if not city:
        return redirect(url_for('error', error="001")) 
    
    url = f"https://api.weatherapi.com/v1/forecast.json?key={os.getenv('API_KEY')}&q={city}&lang=en"
   
    try:
        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        if 'error' in data:
            return redirect(url_for('error', error='002'))

        standardized_city = data.get('location', {}).get('name', city)

        user_ip = request.remote_addr

        connection = get_db_connection()
        connection.execute(
            "INSERT INTO city_req (cidade, ip) VALUES (?, ?)",
            (standardized_city, user_ip)
        )
        connection.commit()
        connection.close()

        user_logged_in = session.get('is_authenticated')

        return render_template(
            '/pages/city.html',
            title=os.getenv('TITLE'),
            city=standardized_city, 
            weather=data,
            current_time=current_time,
            user_logged_in=user_logged_in
        )        
    except requests.exceptions.RequestException as e:
        return redirect(url_for('error', error="003"))


@app.route("/auth")
def auth():
    return render_template('/pages/auth.html', title=os.getenv('TITLE'), email_regex = email_regex, password_regex = password_regex)

@app.route("/register", methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return redirect(url_for('error', error="006")) 
    
    try:
        connection = get_db_connection()
        
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))

        existing_user = cursor.fetchone()
        
        if existing_user:
            return redirect(url_for('error', error="007"))
        
        password_hash = generate_password_hash(password)

        verification_code = generate_verification_code()

        cursor.execute("""
            INSERT INTO users (email, password_hash, verification_code, is_verified)
            VALUES (?, ?, ?, ?)
        """, (email, password_hash, verification_code, False))
            
        connection.commit()

        send_verification_email(email, verification_code)

    except Exception as e:
        return redirect(url_for('error', error="000"))

    return redirect(url_for('auth'))    

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return redirect(url_for('error', error="006"))

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
       
        if not user:
            return redirect(url_for('error', error="008"))

        if not check_password_hash(user['password_hash'], password):
            return redirect(url_for('error', error="009"))  

        if not user['is_verified']:
            return redirect(url_for('error', error="008"))

        session['user_id'] = user['email']
        session['isAdmin'] = user['isAdmin']
        session['is_authenticated'] = True

        return redirect(url_for('index'))  

    except Exception as e:
        return redirect(url_for('error', error="000"))

@app.route('/dashboard')
def dashboard():
    if session.get('is_authenticated') and session.get('user_id'):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Contagem de usuários
            cursor.execute('SELECT COUNT(*) AS user_count FROM users')
            user_count = cursor.fetchone()["user_count"]

            # Contagem de requisições por cidades
            cursor.execute('SELECT COUNT(*) AS city_req_count FROM city_req')
            city_req_count = cursor.fetchone()["city_req_count"]

            most_searched_cities = connection.execute(
                """
                SELECT cidade, COUNT(cidade) as total_searches
                FROM city_req
                GROUP BY cidade
                ORDER BY total_searches ASC
                """
            ).fetchall()

            cities = [row[0] for row in most_searched_cities]  # Nomes das cidades
            request_counts = [row[1] for row in most_searched_cities]  # Contagem de requisições

            print(cities)
            
            connection.close()

            session_dir = app.config['SESSION_FILE_DIR']
            session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']
            active_sessions = 0

            now = datetime.now()

            if os.path.exists(session_dir):
                for session_file in os.listdir(session_dir):
                    session_path = os.path.join(session_dir, session_file)
                    if os.path.isfile(session_path):
                        last_modified = datetime.fromtimestamp(os.path.getmtime(session_path))
                        if now - last_modified <= timedelta(seconds=session_lifetime):
                            active_sessions += 1

            # Renderizar o dashboard
            return render_template(
                '/pages/dashboard.html',
                title=os.getenv('TITLE'),
                user_logged_in=True,
                isAdmin=session.get('isAdmin'),
                user_count=user_count,
                city_req_count=city_req_count,
                active_sessions=active_sessions,
                cities=cities,
                request_counts=request_counts
            )

        except Exception as e:
            # Log de erro detalhado para facilitar o diagnóstico
            logging.error(f"Erro no endpoint '/dashboard': {e}", exc_info=True)
            return redirect(url_for('error', error="000"))
    else:
        return redirect(url_for('auth'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('auth'))

@app.route("/verify", methods=['GET'])
def verify():
    email = request.args.get('email')
    verification_code = request.args.get('verification_code')
    
    print(email, verification_code)

    if not email or not verification_code:
        return redirect(url_for('error', error="003"))
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        
        user = cursor.fetchone()

        if not user:
            return redirect(url_for('error', error="008"))

        if user['verification_code'] != verification_code:
            return redirect(url_for('error', error= "009"))

        cursor.execute("UPDATE users SET is_verified = 1 WHERE email = ?", (email,))
        connection.commit()

        return render_template('/pages/verify.html', title=os.getenv('TITLE'))
    
    except Exception as e:
        return redirect(url_for('error', error="000"))

@app.route("/error")
def error():
    error_code = request.args.get('error') 

    switcher = {
        '000': 'An error occurred. Please try again later.',
        '001': 'You need to enter the name of a city.',
        '002': 'The city entered could not be found.',
        '003': 'Internal server error. Please try again later.',
        '004': 'Latitude and longitude are required.',
        '005': 'Error fetching weather data.',
        '006': 'Email and password are required.',
        '007': 'Email already registered.',
        '008': 'Email not verified.',
        '009': 'Email Incorrect password.',
        '010': 'Email not valid.'
    }

    error_message = {
        'error_message': switcher.get(error_code),
        'error_code': error_code
    }

    user_logged_in = session.get('is_authenticated')

    return render_template('/pages/error.html', title=os.getenv('TITLE'), error=error_message, user_logged_in=user_logged_in)

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

    user_logged_in = session.get('is_authenticated')

    return render_template('/pages/index.html', title=os.getenv('TITLE'), cities=cities_data , city_shearch=top_cities, user_logged_in=user_logged_in)