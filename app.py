from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import Config
from functools import wraps

# Configuration settings
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'secret_aquamelb_h3h3#'
db = SQLAlchemy(app)

PASSWORD = '5ecr3t_aquamelb#'

# Create test database to check whether PostgreSQL is running
class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(120), nullable=False)

# Authentication Handler
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Add test data into the test database
@app.route('/data', methods=['POST'])
def add_data():
    data = request.json['data']
    new_entry = TestModel(data=data)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Data added!"})

@app.route('/data', methods=['GET'])
def get_data():
    all_data = TestModel.query.all()
    result = [{"id": entry.id, "data": entry.data} for entry in all_data]
    return jsonify(result)

# Login / authentication page endpoint route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login', error="Invalid password, please try again."))
    return send_from_directory('static', 'login.html')

# Landing page (Home page) endpoint route
@app.route('/', methods=['GET'])
@login_required
def index():
    if not session.get('authenticated'):
       return redirect(url_for('login'))
    return send_from_directory('static', 'index.html')

# Real-time water monitoring map endpoint route
@app.route('/index2', methods=['GET'])
@login_required
def index2():
    return send_from_directory('static', 'index2.html')

# Articles page endpoint route
@app.route('/articles', methods=['GET'])
@login_required
def articles():
    return send_from_directory('static', 'articles.html')

# Real-time water monitoring page endpoint route
@app.route('/projects', methods=['GET'])
@login_required
def projects():
    return send_from_directory('static', 'projects.html')

# Placeolder
@app.route('/realmonitor', methods=['GET'])
@login_required
def realmonitor():
    return send_from_directory('static', 'realmonitor.html')

# Placeholder
@app.route('/pollutant', methods=['GET'])
def pollutant():
    return send_from_directory('static', 'pollutant.html')

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

# Function to fetch pollutant data from RDB
@app.route('/pollutant_data', methods=['GET'])
def pollutant_data():
    try:
        # FETCH DATA FROM DB FOR PATTERSON RIVER
        query = text('''
            SELECT "site_name_short", "date", "N_TOTAL", "N_NH3", "N_NO2", "N_NO3", "DO_mg", "Temp"
            FROM site_name
            WHERE "site_name_short" = :site_name
        ''')
        results = db.session.execute(query, {'site_name': 'Patterson River'}).fetchall()

        # CONVERT THE QUERY RESULTS TO A LIST OF DICT
        data = [{"site_name_short": row[0], "date": row[1].isoformat(), "N_TOTAL": row[2], "N_NH3": row[3], "N_NO2": row[4], "N_NO3": row[5], "DO_mg": row[6], "Temp": row[7]} for row in results]

        # RETURN DATA AS JSON
        return jsonify(data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
