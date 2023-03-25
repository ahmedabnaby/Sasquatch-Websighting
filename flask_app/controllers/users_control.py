from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import sighting, user
from flask_app.controllers import sighting_control

@app.route('/')
def login_registration():
    return render_template('login.html')

@app.route('/process', methods=['POST'])
def process_registration():
    if user.User.register(request.form):
        return redirect('/dashboard')
    return redirect('/')

@app.route('/dashboard')
def home():
    if "user_id" not in session:
        return redirect('/')
    user_info = user.User.get_user_id({'id' : session['user_id']})
    sighting_list = sighting.Sighting.get_all_sightings()
    return render_template('dashboard.html', user = user_info, sightings = sighting_list)

@app.route('/login', methods=['POST'])
def login():
    if user.User.login(request.form):
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

