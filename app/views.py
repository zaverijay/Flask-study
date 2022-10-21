from flask import Flask, make_response, request, render_template, url_for, redirect, flash
from app.forms import LoginForm, RegistrationForm
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from app.models import UserInfo

@app.route('/')
@login_required
def index():
    name = current_user.username
    return render_template('index.html', name=name)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_password = generate_password_hash(form.password.data, method="sha256")

        username = form.username.data
        password = form.password.data
        email = form.email.data

        new_user = UserInfo(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data} !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(username = form.username.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    flash("You have logged in successfully", "success")
                else:
                    flash("Invalid credentials !", "danger")

        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

# @app.route('/user/<name>')
# def User(name):
#     return f'<h1> Hello Mr. { name } </h1>'

@app.route('/set')
def setCookie():
    response = make_response("I have set the cookie")
    response.set_cookie("myapp", "Flask Web Development")
    return response

@app.route('/get')
def getCookie():
    myapp = request.cookies.get("myapp")
    return "My cookie content is" + str(myapp)