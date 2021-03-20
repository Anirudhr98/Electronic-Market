from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    return render_template('market.html')    

if __name__ == '__main__':
    app.run(debug=True)