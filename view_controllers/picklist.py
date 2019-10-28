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

def create_new_picklist(employee_id, employee_password, picklist_title) -> int:
    if not db.login_employee(employee_id, employee_password):
        abort(401)
    picklist = db.create_new_picklist(picklist_title, employee_id)
    return picklist.id

def delete_picklist(picklist_id):
    try:
        picklist = db.session.query(db.Picklist).filter(db.Picklist.id == picklist_id).one()
        picklist.status = 'deleted'
        db.session.commit()
        return picklist.id
    except:
        db.session.rollback()
        abort(400)

def add_item_to_picklist(picklist_id, location_item_id):
    try:
        picklist = db.session.query(db.Picklist).filter(db.Picklist.id == picklist_id).one()
        location_item = db.session.query(db.LocationItem).filter(db.LocationItem.id == location_item_id).one()
    except:
        abort(400)
    for item in picklist.location_items:
        if item.location_item_id == location_item.id:
            item.quantity += 1
            db.session.commit()
            return item.id
    picklist_item = db.PicklistItem(quantity = 1)
    picklist_item.location_item = location_item
    picklist_item.picklist = picklist
    try:
        db.session.add(picklist_item)
        db.session.commit()
    except:
        db.session.rollback()
        abort(500)
    return picklist_item.id

    
