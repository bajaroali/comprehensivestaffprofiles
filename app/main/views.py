from flask import render_template, flash
from flask_login import login_required
from app.main import main

@main.route('/')
@login_required
def index():
    return render_template('main/index.html')