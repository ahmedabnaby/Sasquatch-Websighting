from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import sighting, user
from flask_app.controllers import users_control


@app.route('/new/sighting')
def sighting_form():
    if "user_id" not in session:
        return redirect('/')
    user_info = user.User.get_user_id({'id' : session['user_id']})
    return render_template('new.html', user = user_info)

@app.route('/sighting/add', methods=['POST'])
def new_sighting():
    if "user_id" not in session:
        return redirect('/')
    data = {
        'location' : request.form['location'],
        'what_happened' : request.form['what_happened'],
        'date_seen' : request.form['date_seen'],
        'num_seen' : request.form['num_seen'],
        'user_id' : session['user_id']
    }
    if sighting.Sighting.add_sighting(data):
        return redirect('/dashboard')
    return redirect('/new/sighting')

@app.route('/show/<int:id>')
def show_sighting(id):
    if "user_id" not in session:
        return redirect('/')
    sighting_info = sighting.Sighting.get_sighting_id({'id':id})
    user_info = user.User.get_user_id({'id' : session['user_id']})
    return render_template('show.html', sighting = sighting_info, user = user_info)

@app.route('/skeptic/<int:id>')
def add_skeptic(id):
    data = {
        'user_id' : session['user_id'],
        'sighting_id' : id
    }
    user.User.skeptic(data)
    return redirect(f'/show/{id}')

@app.route('/believe/<int:id>')
def believe(id):
    data = {
        'user_id' : session['user_id'],
        'sighting_id' : id
    }
    user.User.believe(data)
    return redirect(f'/show/{id}')

@app.route('/edit/<int:id>')
def edit_sighting(id):
    if "user_id" not in session:
        return redirect('/')
    sighting_info = sighting.Sighting.get_sighting_id({'id':id})
    user_info = user.User.get_user_id({'id' : session['user_id']})
    return render_template('edit.html', sighting = sighting_info, user = user_info)

@app.route('/update/<int:id>', methods=['POST'])
def update_sighting(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id' : id,
        'location' : request.form['location'],
        'what_happened' : request.form['what_happened'],
        'date_seen' : request.form['date_seen'],
        'num_seen' : request.form['num_seen'],
    }
    if sighting.Sighting.update_sighting(data):
        return redirect('/dashboard')
    return redirect(f'/edit/{id}')

@app.route('/delete/<int:id>')
def delete_sighting(id):
    sighting.Sighting.delete_sighting({'id':id})
    return redirect('/dashboard')

