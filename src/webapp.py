from flask import Flask, request, render_template

app = Flask(__name__, template_folder='shopping', static_folder='src')

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/checkout')
def checkoutPage():
    return render_template('checkout.html')

@app.route('/process/order', methods=['POST'])
def processOrder():
    return 'Hello World'

app.run(debug=True)