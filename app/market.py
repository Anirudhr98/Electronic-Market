from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user
login_manager = LoginManager()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

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
        hashed_password = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        user_to_create = User(name = form.username.data,
                              email = form.email_address.data,
                              password = hashed_password)
        db.session.add(user_to_create)
        db.session.commit()
        flash("You have successfully created a new account ")
        return redirect(url_for('market_page'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    from forms import LoginForm
    from models import User
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(name = form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
        attempted_password = form.password.data
        ):
            login_user(attempted_user)
            flash("You have been loged in successfully")
            return redirect(url_for('market_page'))
        else:
            flash("Username and Password are not matched..!!")    
    return render_template('login.html', form=form)
     
if __name__ == '__main__':
    app.run(debug=True)