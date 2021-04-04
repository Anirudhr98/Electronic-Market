from flask import Flask, render_template, redirect, url_for, flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user,logout_user, login_required, current_user
login_manager = LoginManager()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    from models import Item
    from forms import PurchaseItemForm, SellItemForm
    purchaseitemform = PurchaseItemForm()
    sellitemform = SellItemForm()
    if request.method == "POST":
        #Purchasing Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
       
       #Selling Item Logic 
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name = sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} for {s_item_object.price}", category='success')
            else:
                flash(f"Unfortunately, you can't sell {s_item_object.name}!", category='danger')
       
        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner = current_user.id)
        return render_template('market.html', items=items, purchaseitemform=purchaseitemform, owned_items = owned_items, sellitemform =sellitemform)


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


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    from forms import LoginForm
    from models import User
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("You have been logged in successfully")
            return redirect(url_for('market_page'))
        else:
            flash("Username and Password are not matched..!!")    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('market_page'))   
     

if __name__ == '__main__':
    app.run(debug=True)