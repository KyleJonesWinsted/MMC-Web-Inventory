from flask import Flask, render_template, render_template_string, request, escape, abort, jsonify, session, redirect, url_for, g
import view_controllers.browse
import view_controllers.search
import view_controllers.settings
import view_controllers.picklist
import view_controllers.adjustments
import data_controller as db
import os
app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.before_request
def check_logged_in():
    if 'user' not in session and request.endpoint != 'login':
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if db.login_employee(request.form['username'], request.form['password']):
            employee = db.session.query(db.Employee).filter(db.Employee.id == request.form['username']).one()
            session['user'] = employee.id
            session['username'] = employee.name.title()
            return redirect('/')
        else:
            return render_template('login.html', first_time=False)
    return render_template('login.html', first_time=True)

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
    return view_controllers.adjustments.adjustments_browse_view()

@app.route('/adjustments/employees')
def adjustments_by_employee():
    return view_controllers.adjustments.employee_select_view()

@app.route('/adjustments/date')
def adjustments_by_date():
    return view_controllers.adjustments.date_select_view()

@app.route('/adjustments/sku')
def adjustments_by_sku():
    return view_controllers.adjustments.item_select_view()

@app.route('/adjustments/reason')
def adjustments_by_reason():
    return view_controllers.adjustments.reason_select_view()

@app.route('/adjustments/adjustments')
def browse_adjustments():
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
    return view_controllers.adjustments.adjustment_detail_view(adjustment_id)
#Manage Settings
@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/settings/adjust_stock')
def adjust_stock_for_item():
    try:
        item_sku = request.args.get('item_sku')
    except:
        abort(400)
    return view_controllers.settings.adjust_stock_for_item_view(item_sku = item_sku)

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
    try:
        json = request.get_json(force=True)
        locations = json['locations']
        employee_id = session['user']
        item_sku = json['item_sku']
        reason_id = json['reason_id']
    except:
        abort(400)
    result = db.adjust_quantities_for_item(locations, employee_id, employee_password, reason_id, item_sku)
    if result == 'Success':
        db.session.commit()
    return jsonify(result), 200

@app.route('/api/new_location')
def add_new_location():
    try:
        location_name = request.args.get('location_name')
    except:
        abort(400)
    location = db.add_new_location(location_name.lower())
    json = {
        'location_id': location.id,
        'location_name': location.name.lower()
    }
    return jsonify(json), 200

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
        employee_id = session['user']
    except:
        abort(400)
    picklist_id = view_controllers.picklist.create_new_picklist(employee_id, picklist_title)
    session['picklist_id'] = picklist_id
    return jsonify(picklist_id), 200

@app.route('/api/delete_picklist')
def delete_picklist():
    try:
        picklist_id = request.args.get('picklist_id')
    except:
        abort(400)
    return_id = view_controllers.picklist.delete_picklist(picklist_id)
    session.pop('picklist_id')
    return jsonify(return_id), 200

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
    return jsonify(picklist_item_id), 200

@app.route('/api/delete_picklist_item')
def delete_picklist_item():
    try:
        picklist_item_id = request.args.get('picklist_item_id')
    except:
        abort(400)
    return_id = view_controllers.picklist.delete_picklist_item(picklist_item_id)
    return jsonify(return_id), 200

@app.route('/api/checkout_picklist')
def checkout_picklist():
    try:
        picklist_id = session['picklist_id']
    except:
        abort(400)
    view_controllers.picklist.check_out_picklist(picklist_id)
    session.pop('picklist_id')
    return jsonify("Success"), 200

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

if __name__ == '__main__':
    app.run(debug=True)
