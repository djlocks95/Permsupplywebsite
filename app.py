from flask import Flask, render_template, url_for, redirect, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'some_secret_key'

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_clothing_store.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()
@app.route('/')
def intro():
    home_url = url_for('home')
    return render_template('intro.html', home_url=home_url)

@app.route('/home')
def home():
    # Initialize the cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
    return render_template('index.html', cart=session['cart'])


@app.route('/add_to_cart')
def add_to_cart():
    item = {
        'name': 'Dog Sweat Suit',
        'price': 200,
        'image': url_for('static', filename='images/IMG_2025.jpg')
    }
    session['cart'].append(item)
    session.modified = True
    return redirect(url_for('home'))


@app.route('/cart')
def cart():
    return render_template('cart.html', cart=session['cart'])

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/remove_from_cart/<int:item_index>')
def remove_from_cart(item_index):
    if 0 <= item_index < len(session['cart']):
        session['cart'].pop(item_index)
        session.modified = True
    return redirect(url_for('cart'))


# Your other routes...



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
