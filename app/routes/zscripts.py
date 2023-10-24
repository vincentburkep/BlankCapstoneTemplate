from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.classes.data import Role
import datetime as dt

@app.route('/listroles')
def listroles():
    roles = Role.objects()
    for role in roles:
        flash(role.name)
    return render_template('index.html')

@app.route('/makeroles')
def makeroles():
    studentRole = Role(name="student").save()
    teacherRole = Role(name="teacher").save()
    adminRole = Role(name="admin").save()
    return render_template('index.html')