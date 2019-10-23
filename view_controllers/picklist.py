import data_controller as db
from flask import render_template, abort

def picklist_view(picklist_id):
    try:
        picklist = db.session.query(db.Picklist).filter(db.Picklist.id==picklist_id).one()
    except:
        abort(404)
    return render_template('picklist.html', picklist = picklist)

def no_picklist_view():
    return render_template('no_picklist.html')

def picklist_list_view():
    try:
        open_picklists = db.session.query(db.Picklist).filter(db.Picklist.status == 'open').all()
        checkout_picklists = db.session.query(db.Picklist).filter(db.Picklist.status == 'checked_out').all()
    except:
        abort(500)
    return render_template('picklist_list.html', open_picklists = open_picklists, checkout_picklists=checkout_picklists)