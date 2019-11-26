from flask import Flask, render_template, render_template_string, request, escape, abort, jsonify, session, redirect, url_for, g
import view_controllers.browse
import view_controllers.search
import view_controllers.settings
import view_controllers.picklist
import view_controllers.adjustments
import data_controller as db
import os
from sqlalchemy import exc

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

os.environ['BUCKET_NAME'] = "https://kylejones-testing.s3.us-east-2.amazonaws.com/" if True else "../"
app.add_template_global(name = 'env', f=os.environ)

@app.before_request
def check_logged_in():
    if 'user' not in session and request.endpoint != 'login':
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if db.login_employee(request.form['username'], request.form['password']):
            employee = db.session.query(db.Employee).filter(db.Employee.id == request.form['username']).one()
            session['user'] = employee.serialize()
            return redirect('/')
        else:
            return render_template('login.html', first_time=False)
    return render_template('login.html', first_time=True)

def check_admin():
    if session['user']['credentials'] == 'employee':
        abort(403)

def commit_session(stop_execution: bool = True):
    if session['user']['credentials'] == 'demo':
        db.session.rollback()
        if stop_execution:
            abort(403)
    else:
        try:
            db.session.commit()
        except exc.DBAPIError as ex:
            db.session.rollback()
            print(ex.orig.pgcode)

@app.route('/logout')
def logout():
    session.clear()
    return jsonify('success'), 200

#Homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/placeholder/<string:page_name>')
def placeholder(page_name):
    return render_template('placeholder.html', page_name=page_name)

#Browse Inventory
@app.route('/browse')
def browse():
    return view_controllers.browse.browse_type_view()

@app.route('/browse/category')
def browse_by_category():
    return view_controllers.browse.category_select_view()

@app.route('/browse/location')
def browse_by_location():
    return view_controllers.browse.location_select_view()

@app.route('/browse/manufacturer')
def browse_by_manufacturer():
    return view_controllers.browse.manufacturer_select_view()

@app.route('/browse/items')
def browse_items():
    try:
        browse_type = request.args.get('browse_type')
        filter_id = request.args.get('filter_id')
    except:
        abort(400)
    page_number = request.args.get('page')
    if page_number == None:
        page_number = 0
    return view_controllers.browse.items_view(browse_type = browse_type, 
        filter_id = filter_id, 
        page_number=int(page_number))

@app.route('/item/<int:sku>')
def view_item_details(sku):
    return view_controllers.browse.item_detail_view(sku=sku)

#Adjustment History
@app.route('/adjustments')
def adjustments():
    check_admin()
    return view_controllers.adjustments.adjustments_browse_view()

@app.route('/adjustments/employees')
def adjustments_by_employee():
    check_admin()
    return view_controllers.adjustments.employee_select_view()

@app.route('/adjustments/date')
def adjustments_by_date():
    check_admin()
    return view_controllers.adjustments.date_select_view()

@app.route('/adjustments/sku')
def adjustments_by_sku():
    check_admin()
    return view_controllers.adjustments.item_select_view()

@app.route('/adjustments/reason')
def adjustments_by_reason():
    check_admin()
    return view_controllers.adjustments.reason_select_view()

@app.route('/adjustments/adjustments')
def browse_adjustments():
    check_admin()
    try:
        browse_type = request.args.get('browse_type')
        filter_id = request.args.get('filter_id')
    except:
        abort(400)
    page_number = request.args.get('page')
    if page_number == None:
        page_number = 0
    return view_controllers.adjustments.adjustments_view(browse_type, filter_id, page_number)

@app.route('/adjustment/<int:adjustment_id>')
def view_adjustment_details(adjustment_id):
    check_admin()
    return view_controllers.adjustments.adjustment_detail_view(adjustment_id)

#Manage Settings
@app.route('/settings')
def settings():
    check_admin()
    return render_template('settings.html')

@app.route('/settings/create_new_item', methods = ['GET', 'POST'])
def create_new_item():
    check_admin()
    if request.method == 'GET':
        categories = db.get_all_categories()
        return render_template('create_new_item.html', categories = categories)
    try:
        part_no = request.form.get("part_no").lower()
        manufacturer = request.form.get("manufacturer").lower()
        description = request.form.get("description")
        category_id = request.form.get("category")
    except:
        abort(400)
    new_item = db.create_new_item(part_no, description, manufacturer, category_id)
    commit_session(stop_execution=True)
    return redirect("/settings/adjust_stock?item_sku={}".format(new_item.sku))

@app.route('/settings/modify_item_details', methods=['GET', 'POST'])
def modify_item_details():
    check_admin()
    if request.method == 'GET':
        try:
            item_sku = request.args.get('item_sku')
            item = db.session.query(db.Item).filter(db.Item.sku == item_sku).one()
        except:
            abort(400)
        categories = db.get_all_categories()
        return render_template('modify_item_details.html', item = item, categories = categories)
    try:
        item_sku = request.form.get("item_sku")
        part_no = request.form.get("part_no").lower()
        manufacturer = request.form.get("manufacturer").lower()
        description = request.form.get("description")
        category_id = request.form.get("category")
    except:
        abort(400)
    item = db.modify_item_details(item_sku, part_no, manufacturer, description, category_id)
    commit_session(stop_execution=False)
    return redirect(url_for('view_item_details', sku = item_sku))
    
    



@app.route('/settings/adjust_stock', methods=['GET', 'POST'])
def adjust_stock_for_item():
    if request.method == 'GET':
        check_admin()
        try:
            item_sku = request.args.get('item_sku')
        except:
            abort(400)
        return view_controllers.settings.adjust_stock_for_item_view(item_sku = item_sku)
    try:
        item_sku = request.form.get("item-sku")
        reason_id = request.form.get("reason")
        location_ids = request.form.getlist("location-id")
        quantities = request.form.getlist("quantity")
        qty_checked_out = request.form.get("checked-out")
        employee_id = session['user']['id']
    except:
        abort(400)
    locations = {}
    for i in range(len(location_ids)):
        locations[int(location_ids[i])] = int(quantities[i])
    locations['checked-out'] = int(qty_checked_out)
    db.adjust_quantities_for_item(locations, employee_id, reason_id, item_sku)
    commit_session(stop_execution = False)
    return redirect(url_for('view_item_details', sku = item_sku))

#Picklists
@app.route('/picklists')
def picklists():
    return view_controllers.picklist.picklist_list_view()

@app.route('/checkin_picklist', methods=['GET', 'POST'])
def checkin_picklist():
    if request.method == 'GET':
        try:
            picklist_id = request.args.get('picklist_id')
            picklist = db.session.query(db.Picklist).filter(db.Picklist.id==picklist_id).one()
        except:
            abort(400)
        return render_template('picklist_checkin.html', picklist = picklist)
    try:
        picklist_id = escape(request.form.get('picklist_id'))
        picklist_item_ids = request.form.getlist('picklist_item_id')
        returned_qtys = request.form.getlist('returned_qty')
    except:
        abort(400)
    returned_item_counts = {}
    for i in range(len(picklist_item_ids)):
        returned_item_counts[int(picklist_item_ids[i])] = int(returned_qtys[i])
    view_controllers.picklist.check_in_picklist(picklist_id, returned_item_counts)
    commit_session(stop_execution = False)
    return redirect('/picklists')

#Search Inventory
@app.route('/search')
def search():
    try:
        search_string = str(request.args.get('input'))
        if search_string == None or search_string == "" or search_string == "None":
            abort(400)
    except:
        abort(400)
    page_number = request.args.get('page')
    if page_number == None:
        page_number = 0
    return view_controllers.search.search_results_view(search_string, int(page_number))

#API
@app.route('/api/adjust_quantity', methods=['POST'])
def adjust_quantity():
    """ JQuery request should look like this
    $.post('/api/adjust_quantity', JSON.stringify({
    "locations": [
        {"location_id": 1, "quantity": 9},
        {"location_id": 2, "quantity": 1}
    ],
    "reason_id": 1,
    "item_sku": 1000
    }));
    """
    check_admin()
    try:
        json = request.get_json(force=True)
        locations = json['locations']
        employee_id = session['user']['id']
        item_sku = json['item_sku']
        reason_id = json['reason_id']
    except:
        abort(400)
    result = db.adjust_quantities_for_item(locations, employee_id, employee_password, reason_id, item_sku)
    if result == 'Success':
        commit_session(stop_execution = True)
    return jsonify(result), 200

@app.route('/api/new_location')
def add_new_location():
    check_admin()
    try:
        location_name = request.args.get('location_name')
        item_sku = int(request.args.get('item_sku'))
    except:
        abort(400)
    location_item_id = db.add_new_location(location_name.upper(), item_sku)
    commit_session(stop_execution = True)
    return jsonify(location_item_id), 200

@app.route('/api/delete_location_item')
def delete_location_item():
    check_admin()
    try:
        location_item_id = request.args.get('location_item_id')
    except:
        abort(400)
    result = db.delete_location_item(location_item_id)
    if result == 409:
        abort(409)
    commit_session(stop_execution = False)
    return jsonify("deleted"), 200
    

@app.route('/api/set_picklist_id')
def create_new_cart():
    try:
        session['picklist_id'] = request.args.get('picklist_id')
    except:
        abort(400)
    return jsonify(session['picklist_id']), 200

@app.route('/api/get_item')
def get_item_by_sku():
    try:
        item_sku = request.args.get('item_sku')
    except:
        abort(400)
    item = db.get_item_by_sku(int(item_sku))
    if item == None:
        return jsonify(item), 404
    else:
        return jsonify(item.__repr__()), 200

@app.route('/api/get_picklist')
def get_picklist_by_id():
    try:
        picklist_id = session['picklist_id']
    except:
        return view_controllers.picklist.no_picklist_view(), 200
    return view_controllers.picklist.picklist_view(picklist_id), 200

@app.route('/api/create_new_picklist')
def create_new_picklist():
    try:
        picklist_title = escape(request.args.get('picklist_title'))
        employee_id = session['user']['id']
    except:
        abort(400)
    picklist = view_controllers.picklist.create_new_picklist(employee_id, picklist_title)
    commit_session(stop_execution = True)
    session['picklist_id'] = picklist.id
    return jsonify(picklist.id), 200

@app.route('/api/delete_picklist')
def delete_picklist():
    try:
        picklist_id = request.args.get('picklist_id')
    except:
        abort(400)
    view_controllers.picklist.delete_picklist(picklist_id)
    commit_session(stop_execution = False)
    if 'picklist_id' in session:
        session.pop('picklist_id')
    return jsonify("Deleted"), 200

@app.route('/api/save_picklist')
def save_picklist():
    session.pop('picklist_id')
    return jsonify('Success'), 200

@app.route('/api/add_item_to_picklist')
def add_item_to_picklist():
    try:
        location_item_id = request.args.get('location_item_id')
        picklist_id = session['picklist_id']
    except:
        abort(400)
    picklist_item_id = view_controllers.picklist.add_item_to_picklist(picklist_id, location_item_id)
    commit_session(stop_execution = False)
    return jsonify(picklist_item_id), 200

@app.route('/api/delete_picklist_item')
def delete_picklist_item():
    try:
        picklist_item_id = request.args.get('picklist_item_id')
    except:
        abort(400)
    return_id = view_controllers.picklist.delete_picklist_item(picklist_item_id)
    commit_session(stop_execution = False)
    return jsonify(return_id), 200

@app.route('/api/checkout_picklist')
def checkout_picklist():
    try:
        picklist_id = session['picklist_id']
    except:
        abort(400)
    view_controllers.picklist.check_out_picklist(picklist_id)
    session.pop('picklist_id')
    commit_session(stop_execution = False)
    return jsonify("Success"), 200

@app.route('/api/get_id')
def get_id():
    try:
        search_string = request.args.get('search_string')
        object_type = request.args.get('object_type')
    except:
        abort(400)
    result_id = view_controllers.browse.get_object_id(search_string.lower(), object_type)
    return jsonify(result_id), 200

#Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True)
