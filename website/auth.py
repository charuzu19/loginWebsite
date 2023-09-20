from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user, current_user




auth = Blueprint('auth', __name__) #it doesnt have to be view

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password =request.form.get('password')
        
        user = User.query.filter_by(email=email).first() #find specific query, first is return the first result 
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='sucess')
                login_user(user, remember=True) #so only after we logged in we can access pages
                return redirect (url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exists', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #we cannot access logout unless we are logged in 
def logout ():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must have more than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must have more than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Passwords must at least have 7 characters.', category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account successfully created!', category='success')
                return redirect(url_for('views.home'))
            except IntegrityError:
                db.session.rollback()
                flash('Email address is already in use.', category='error')
    return render_template("sign_up.html", user = current_user)