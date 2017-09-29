from app import app, db, lm, oid
from flask import render_template,flash, redirect,session, url_for,request,g
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User


@app.before_request
def before_request():
    print "Before_request called"
    print "current_user: "
    print current_user
    print "Current user printed abovee"
    flash("/before login hit")
    g.user = current_user

@app.route("/")
@app.route("/index")
@login_required
def index():
    print "/index hit"
    user = g.user
    flash("/index hit")
	# user = {'username':'Vimanyu'}
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template('index.html',title='Home',user=user,posts=posts)

@lm.user_loader
def load_user(id):
    print "user_load called in views.py"
    return User.query.get(int(id))

@app.route("/login",  methods=['GET', 'POST'])
@oid.loginhandler
def login():
    print "/login hit"
    flash("login hit")
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        # flash('Login requested for OpenID="%s", remember_me=%s' %(form.openid.data, str(form.remember_me.data)))
        # return redirect('/index')
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname','email'])

    return render_template('login.html', title='Sign In',form=form,providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    print "after_login hit"
    flash("/afterlogin")
    if resp.email == None or resp.email == "":
        flash("Invalid user detected. Please try again")
        return redirect(url_for('login'))

    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split("@")[0]
        user = User(nickname=nickname,email=resp.email)
        db.session.add(user)
        db.session.commit()

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me',None)
    login_user(user,remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))





