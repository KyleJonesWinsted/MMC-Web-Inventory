import data_controller as db
from flask import render_template, abort

def picklist_view(picklist_id):
    return render_template('picklist.html')