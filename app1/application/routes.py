from application.models import Users, Prizes
# import render_template function from the flask module
from flask import render_template, redirect, url_for, request
# import the app object from the ./application/__init__.py
from application import app, db, bcrypt
# import PostForm from application.forms
from application.forms import StatsForm, RegistrationForm, LoginForm, PlayerForm, UpdateForm, UpdatePlayer
# import from Flask_login module
from flask_login import login_user, current_user, logout_user, login_required
# import further forms functionality
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm


# define routes for / & /home, this function will be called when these are accessed
# General site information accessable to everyone
#========== Home Page ============
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

#========== About Page ============
@app.route('/about')
def about():
    return render_template('about.html', title='About')


#========= Adding Stats =====================
@app.route('/addstats', methods=['GET', 'POST'])
@login_required 
def addstats():

    form = StatsForm()
    if form.validate_on_submit():
        statsData = Stats(goals = form.goals.data,assists = form.assists.data,chances =form.chances.data,shots =form.shots.data,minutes =form.minutes.data,date =form.date.data, stat=form.player_id.data)
        db.session.add(statsData)
        db.session.commit()
        return redirect(url_for('addstats'))

    else:
        print(form.errors)

    return render_template('playerstats.html', title='Add Stats', form=form)

#========= View Stats =======================
@app.route('/view')
@login_required
def view():
    statdata = db.session.query(Players, Stats).select_from(db.join(Stats, Players)).filter(Stats.player_id == Players.player_id)\
        .filter(Players.id == current_user.id).all()
    return render_template('view.html', title='View Stats', stats=statdata)

#========= remove stats =====================
@app.route('/deletestats/<stat_id>')
@login_required
def deletestats(stat_id):
    db.session.query(Stats).filter_by(stat_id = stat_id).delete(synchronize_session=False)
    db.session.commit()
    return redirect(url_for('view'))



########### User Management ##################
#========== User Registration Page ===========
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(first_name=form.first_name.data,last_name=form.last_name.data,email=form.email.data, password=hash_pw)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#========== User Login  ======================
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

#========= User Logout =======================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#========= Manage User Account ===============
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name        
        form.email.data = current_user.email        
    return render_template('account.html', title='Account', form=form)

#========= Delete User Account ================
@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
    user = current_user.id
    account = Users.query.filter_by(id=user).first()
    players = Players.query.filter_by(id=user)
    for player in players :
        stats = db.session.query(Stats).select_from(Stats).filter_by( player_id = player.player_id).all()  
        for stat in stats :
            db.session.delete(stat)
        db.session.delete(player)
    logout_user()
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('register'))