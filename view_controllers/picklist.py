import data_controller as db
import app
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

def create_new_picklist(employee_id, picklist_title) -> int:
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
            if item.quantity < location_item.quantity:
                item.quantity += 1
                db.session.commit()
                return item.id
            else:
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

def delete_picklist_item(picklist_item_id):
    try:
        picklist_item = db.session.query(db.PicklistItem).filter(db.PicklistItem.id == picklist_item_id).one()
        db.session.delete(picklist_item)
        db.session.commit()
    except:
        db.session.rollback()
        abort(400)
    
def check_out_picklist(picklist_id):
    try:
        picklist = db.session.query(db.Picklist).filter(db.Picklist.id == picklist_id).one()
        if picklist.status != "open":
            abort(400)
    except:
        abort(400)
    try:
        picklist.status = "checked_out"
        for picklist_item in picklist.location_items:
            location = picklist_item.location_item
            item = picklist_item.location_item.item
            location.quantity -= picklist_item.quantity
            item.qty_checked_out += picklist_item.quantity
        db.session.commit()
    except:
        db.session.rollback()
        abort(500)

def check_in_picklist(picklist_id, returned_item_counts):
    """
    picklist_items is dict with format { picklist_item_id: quantity_returned }
    """
    try:
        picklist = db.session.query(db.Picklist).filter(db.Picklist.id == picklist_id).one()
        if picklist.status != 'checked_out':
            abort(400)
    except:
        abort(400)
    try:
        picklist.status = 'closed'
        for picklist_item in picklist.location_items:
            qty_not_returned = picklist_item.quantity - returned_item_counts[picklist_item.id]
            old_qty = picklist_item.location_item.quantity + picklist_item.quantity
            new_qty = old_qty - qty_not_returned
            picklist_item.location_item.quantity = new_qty
            picklist_item.location_item.item.qty_checked_out -= picklist_item.quantity
            if qty_not_returned != 0:
                db.create_new_adjustment(1, 
                    picklist_item.location_item.item.sku, 
                    app.session['user'], 
                    [{'location_id': picklist_item.location_item.location.id, 
                        'old_qty': old_qty,
                        'new_qty': new_qty}])
        db.session.commit()
    except:
        db.session.rollback()
        abort(500)
