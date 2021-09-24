from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True)

                return redirect(url_for('views.index'))
            else:
                flash('Wrong password.', category='error')
        else:
            flash('This user does not exist', category='error')
    
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['cpass']
        user = User.query.filter_by(email=email).first()

        if user:
            flash('This email is already registered, try other email.', category='error')
        elif len(email) < 4:
            flash('Email must greather then 4 characters.', category='error')
        elif len(name) < 2:
            flash('First name must greather then 2 characters.', category='error')
        elif password != confirm_password:
            flash('The password does not match.', category='error')
        elif len(password) < 8:
            flash('Password must greather then 8 characters.', category='error')
        else:
            new_user = User(
                email = email,
                password = generate_password_hash(password, method='sha256'),
                name = name
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created.', category='success')

            return redirect(url_for('views.index'))

    return render_template('sign_up.html', user=current_user)