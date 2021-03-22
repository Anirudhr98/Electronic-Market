from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    from models import Item
    item = Item.query.all()
    return render_template('market.html',items = item)    

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    from forms import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        from models import User
        user_to_create = User(name = form.username.data,
                              email = form.email_address.data,
                              password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash("You have successfully created a new account ")
        return redirect(url_for('market_page'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    
    return render_template('register.html', form=form)
    
if __name__ == '__main__':
    app.run(debug=True)