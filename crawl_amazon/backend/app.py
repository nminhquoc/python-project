import subprocess
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'

db = SQLAlchemy(app)


class ProductResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    img = db.Column(db.String())
    url = db.Column(db.String())
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    search_text = db.Column(db.String())
    source = db.Column(db.String())

    def __init__(self, name, img, url, price, search_text, source):
        self.name = name
        self.img = img
        self.url = url
        self.price = price
        self.search_text = search_text
        self.source = source


class TrackProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    tracked = db.Column(db.Boolean, default=True)

    def __init__(self, name, tracked=True):
        self.name = name
        self.tracked = tracked


@app.route('/result', methods=['POST'])
def submit_results():
    results = request.json.get('data')
    search_text = request.json.get("search_text")
    source = request.json.get("source")

    for result in results:
        product_result = ProductResult(
            name=result['name'],
            url=result['url'],
            img=result["img"],
            price=result['price'],
            search_text=search_text,
            source=source
        )
        db.session.add(product_result)

    db.session.commit()
    response = {'message': 'Received data successfully'}
    return jsonify(response), 200


@app.route('/unique_search_texts', methods=['GET'])
def get_unique_search_texts():
    unique_search_texts = db.session.query(
        ProductResult.search_text).distinct().all()
    unique_search_texts = [text[0] for text in unique_search_texts]
    return jsonify(unique_search_texts)


@app.route('/result')
def get_product_result():
    search_text = request.args.get('search_text')
    results = ProductResult.query.filter_by(search_text=search_text).order_by(
        ProductResult.created_at.desc()).all()

    product_dict = {}
    for result in results:
        url = result.url
        if url not in product_dict:
            product_dict[url] = {
                'name': result.name,
                'img': result.img,
                'url': result.url,
                'price': result.price,
                'created_at': result.created_at,
                'source': result.source,
                'price_history': []
            }
        product_dict[url]['price_history'].append({
            'price': result.price,
            'date': result.created_at
        })

    formatted_result = list(product_dict.values())

    return jsonify(formatted_result)


@app.route('/all-result', methods=['GET'])
def get_result():
    results = ProductResult.query.all()
    product_result = []
    for result in results:
        product_result.append({
            'name': result.name,
            'img': result.img,
            'url': result.url,
            'price': result.price,
            'created_at': result.created_at,
            'search_text': result.search_text,
            'source': result.source
        })

    return jsonify(product_result)


@app.route('/start-scaper', methods=['POST'])
def start_scaper():
    url = request.json.get('url')
    search_text = request.json.get('search_text')

    command = f"python ./scraper/__init__.py {url} \"{search_text}\" /result"
    subprocess.Popen(command, shell=True)

    return jsonify({'message': 'Scraper started successfully'}), 200


