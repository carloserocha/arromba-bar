from flask import Flask, request, render_template, make_response, jsonify
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__, 
    template_folder='shopping', 
    static_folder='static', 
    static_url_path='')

app.config['MONGO_URI'] = 'mongodb://localhost:27017/bar'

client_db = PyMongo(app)

client_db = client_db.db


@app.route('/')
def indexPage():
    products = [ product for product in client_db.Product.find({ 'status': True }) ]
    return render_template('index.html.jinja', products=products)

@app.route('/checkout', methods=['POST'])
def checkoutPage():
    return render_template('checkout.html')

@app.route('/process/order', methods=['POST'])
def processOrder():
    data = request.get_json()
    
    member = client_db.Member.find_one({ 'client_id': data['member'] })
    buy_products = data['buy']

    total_value = 0
    for product in buy_products:
        total_value += product['qty'] * product['price']

    order_id = [
            doc['order_id'] for doc in 
                client_db.Order.find().limit(1).sort('created_at', -1)
        ] or [10001]
    
    order_id = order_id[0] + 1
    
    order = {
        'order_id': order_id,
        'client_id': member['client_id'],
        'created_at': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'total_value': total_value,
        'products': buy_products
    }

    client_db.Order.insert_one({
        'order_id': order_id,
        'client_id': member['client_id'],
        'created_at': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'total_value': total_value,
        'products': buy_products
    })

    return make_response (jsonify(order), 201)

app.run(debug=True)