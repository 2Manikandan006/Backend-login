from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!", category='success')
                login_user(user, remember = True)   #??
                return redirect(url_for('Views.home'))  
            else:
                flash("Incorrect Password!", category='error')
        else:
            flash("Email does not exist!", category='error')

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required    #???
def logout():
    flash("Loged out successfully!", category='success')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        FirstName = request.form.get('FirstName')
        LastName = request.form.get('LastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email already exists!", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category='error')
        elif len(FirstName) < 2:
            flash("First name must be greater than 1 character.", category='error')
        elif len(LastName) < 1:
            flash("Last name must be greater than 1 character.", category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters! ", category='error')
        else:
            new_user = User(email = email, 
                            FirstName = FirstName, 
                            LastName = LastName, 
                            password = generate_password_hash(password1, method='pbkdf2:sha256'))
            print(f"Password generated: {new_user.password}")
            db.session.add(new_user)     # new user creating
            try:
                db.session.commit()         # commiting the new user
                login_user(user, remember = True)   #??
                flash("Account created successfuly!", category='success')
                return redirect(url_for('Views.home'))
            except Exception as e:
                flash(f"An error is occured: {e}", category='error')
                db.session.rollback

    return render_template("signup.html", user = current_user)