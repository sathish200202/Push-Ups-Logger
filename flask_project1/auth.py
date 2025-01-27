from flask import Blueprint, render_template, url_for, request, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods = ['POST'])
def signup_post():

    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

   
    if not name or not email or not password1 or not password2:
            print('All feilds are required')
            return redirect(url_for('auth.signup'))
        
    if password1 == password2:

            # print(name, email, password1)
            user = User.query.filter(User.email == email).first()

            if user:
                print('User already exists')
                return redirect(url_for('auth.signup'))

            try:

                #hash the password
                hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')
                new_user = User(name=name, email=email, password=hashed_password)

                db.session.add(new_user) #add new user to the session
                db.session.commit() # saving the new user to database

                return redirect(url_for('auth.login'))
            except Exception as e:
                print(f"Error in creating new user {e}")
        
    else:
            print('Passwords do not match')
            return redirect(url_for('auth.signup'))
        
    

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods = ['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    try:
        if not user or not check_password_hash(user.password, password):
            print('Invalid Credentials')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        print('Login successfully')
        #print(f"user: {user}")
        return redirect(url_for('main.profile'))
    
    except Exception as e:
        print(f'Error in login functionality {e}')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')