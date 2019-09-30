import data_controller as db
from flask import render_template

def setupView():
    items = db.get_all_items()
    return render_template('browse.html')