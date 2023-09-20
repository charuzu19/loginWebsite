from flask import Blueprint, render_template
from flask_login import login_required, current_user



views = Blueprint('views', __name__) #it doesnt have to be view

@views.route('/') #so i think it will run the page, like for example /home, it will run home, etc
@login_required
def home():
    return render_template("home.html")
