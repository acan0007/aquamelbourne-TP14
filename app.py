from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Configuration settings
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(120), nullable=False)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
