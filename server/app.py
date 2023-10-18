#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
# GET /bakeries: returns an array of JSON objects for all bakeries in the database.
def bakeries():
    bakeries_list = [bakery.to_dict() for bakery in Bakery.query.all()]

    response = make_response(
        jsonify(bakeries_list),
        200
    )
    
    return response

@app.route('/bakeries/<int:id>')
# GET /bakeries/<int:id>: returns a single bakery as JSON with its baked goods nested in an array. Use the id from the URL to look up the correct bakery.
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first().to_dict()

    response = make_response(
        jsonify(bakery),
        200
    )    
    return response

@app.route('/baked_goods/by_price')
# GET /baked_goods/by_price: returns an array of baked goods as JSON, sorted by price in descending order. (HINT: how can you use SQLAlchemy to sort the baked goods in a particular order?)
def baked_goods_by_price():
    baked_goods = [baked_good.to_dict() for baked_good in BakedGood.query.order_by(db.desc('price')).all()]
    
    response = make_response(
        jsonify(baked_goods),
        200
    )

    return response

@app.route('/baked_goods/most_expensive')
# GET /baked_goods/most_expensive: returns the single most expensive baked good as JSON. (HINT: how can you use SQLAlchemy to sort the baked goods in a particular order and limit the number of results?)
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(db.desc('price')).first().to_dict()

    response = make_response(
        jsonify(most_expensive),
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
