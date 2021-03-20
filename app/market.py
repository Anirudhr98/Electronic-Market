from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    from models import Item
    item = Item.query.all()
    return render_template('market.html',items = item)    

if __name__ == '__main__':
    app.run(debug=True)