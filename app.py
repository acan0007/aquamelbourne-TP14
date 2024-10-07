from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import Config
from functools import wraps
import os
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from werkzeug.middleware.proxy_fix import ProxyFix

# Configuration settings (Initialize Flask app)
app = Flask(__name__)
app.config.from_object(Config)

# Enable CSRF Protection
csrf = CSRFProtect(app)

#Database setup
db = SQLAlchemy(app)

# setting session parameters
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are only sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent access to cookies via JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protect against CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # Set session lifetime

# Define session lifetime
@app.before_request
def make_session_permanent():
    session.permanent = True

# Authentication Handler
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Set security headers from environment variables
@app.after_request
def set_security_headers(response):
    # X-XSS-Protection: Enables the browser's built-in XSS filter
    response.headers['X-XSS-Protection'] = os.getenv('X_XSS_PROTECTION', '1; mode=block')

    # X-Content-Type-Options: Prevents browsers from interpreting files as a different MIME type
    response.headers['X-Content-Type-Options'] = os.getenv('X_CONTENT_TYPE_OPTIONS', 'nosniff')

    # X-Frame-Options: Prevents clickjacking attacks
    response.headers['X-Frame-Options'] = os.getenv('X_FRAME_OPTIONS', 'SAMEORIGIN')

    return response

# Login / authentication page endpoint route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == app.config['PASSWORD']:
            session['authenticated'] = True
            app.logger.info('CSRF token validation successful')
            return redirect(url_for('index'))
        else:
           app.logger.info('Invalid password attempt') 
           return redirect(url_for('login', error="Invalid password, please try again."))
    return render_template('login.html')

# Landing page (Home page) endpoint route
@app.route('/', methods=['GET'])
@login_required
def index():
    if not session.get('authenticated'):
       return redirect(url_for('login'))
    return render_template('index.html')

# Real-time water monitoring map endpoint route
@app.route('/index2', methods=['GET'])
@login_required
def index2():
    return render_template('index2.html')

# Articles page endpoint route
@app.route('/articles', methods=['GET'])
@login_required
def articles():
    return render_template('articles.html')

# Real-time water monitoring page endpoint route
@app.route('/projects', methods=['GET'])
@login_required
def projects():
    return render_template('projects.html')

# Placeolder
@app.route('/realmonitor', methods=['GET'])
@login_required
def realmonitor():
    return render_template('realmonitor.html')

# Placeholder
@app.route('/pollutant', methods=['GET'])
@login_required
def pollutant():
    return render_template('pollutant.html')

# Stormwater
@app.route('/stormwater', methods=['GET'])
@login_required
def stormwater():
    return render_template('stormwater.html')

# Stormwater Dashboard
@app.route('/stormwater-dashboard', methods=['GET'])
@login_required
def stormwater_dashboard():
    return render_template('stormwater-dashboard.html')

# Nitrogen
@app.route('/nitrogen', methods=['GET'])
@login_required
def nitrogen():
    return render_template('nitrogen.html')

# Nitrogen Dashboard
@app.route('/nitrogen-dashboard', methods=['GET'])
@login_required
def nitrogen_dashboard():
    return render_template('nitrogen_dashboard.html')

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Water Supply Dashboard
@app.route('/water', methods=['GET'])
def water():
    return render_template('water.html')

# Water Supply Dashboard
@app.route('/water-supply', methods=['GET'])
def water_supply():
    return render_template('water_supply.html')

@app.route('/data-table', methods=['GET'])
def data_table():
    return send_from_directory('dataset','data.xlsx')

# Function to fetch E. Coli relation from RDB
@app.route('/heatmap_data', methods=['GET'])
def heatmap_data():
    try:
        # FETCH ECOLI DATA FROM DB
        query = text('SELECT "siteId", "siteName", "date", "value", "qualifier", "level", "key" FROM ecoli')
        results = db.session.execute(query).fetchall()

        # CONVERT THE QUERY RESULTS TO A LIST OF DICT
        data = [{"siteId": row[0], "siteName": row[1], "date": row[2].isoformat(), "value": row[3], "qualifier": row[4], "level": row[5], "key": row[6]} for row in results]

        # return data as JSON
        return jsonify(data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Function to fetch Nitrogen Total relation from RDB
@app.route('/nitrogen_data', methods=['GET'])
def nitrogen_data():
    try:
        # FETCH NITROGEN DATA FROM DB
        query = text('SELECT "Site ID", "Name", "Datetime", "Value", "Unit of Measurement", "WaterQuality", "WGS84_LONG", "WGS84_LAT", "WGS84_LONG_N", "WGS84_LAT_E" FROM nitrogen_total')
        results = db.session.execute(query).fetchall()

        # CONVERT THE QUERY RESULTS TO A LIST OF DICT
        data = [{
            "Site ID": row[0], 
            "Name": row[1], 
            "Datetime": row[2].isoformat() if hasattr(row[2], 'isoformat') else row[2],  # Handle datetime formatting
            "Value": row[3], 
            "Unit of Measurement": row[4], 
            "WaterQuality": row[5], 
            "WGS84_LONG": row[6], 
            "WGS84_LAT": row[7], 
            "WGS84_LONG_N": row[8], 
            "WGS84_LAT_E": row[9]
        } for row in results]

        # Return the data as JSON
        return jsonify(data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Function to fetch Stormwater Pits relation from RDB
@app.route('/stormwater_pits_data', methods=['GET'])
def stormwater_pits_data():
    try:
        # FETCH STORMWATER PITS DATA FROM DB
        query = text('''
            SELECT "asset_number", "asset_description", "construction_material_lupvalue", 
                   "grate_length", "grate_width", "grate_material_lupvalue", 
                   "lat", "lon", "location"
            FROM stormwater_pits
        ''')
        results = db.session.execute(query).fetchall()

        # CONVERT THE QUERY RESULTS TO A LIST OF DICT
        data = [{
            "asset_number": row[0],
            "asset_description": row[1],
            "construction_material_lupvalue": row[2],
            "grate_length": row[3],
            "grate_width": row[4],
            "grate_material_lupvalue": row[5],
            "lat": row[6],
            "lon": row[7],
            "location": row[8]
        } for row in results]

        # Return the data as JSON
        return jsonify(data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
