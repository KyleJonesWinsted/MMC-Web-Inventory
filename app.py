from flask import Flask, render_template, request, abort, jsonify, session
import view_controllers.browse
import view_controllers.search
import data_controller as db
import os
app = Flask(__name__)
app.secret_key = os.urandom(64)

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
    return view_controllers.browse.items_view(browse_type = browse_type, filter_id = filter_id)

@app.route('/item/<int:sku>')
def view_item_details(sku):
    return view_controllers.browse.item_detail_view(sku=sku)
    
#Adjustment History
@app.route('/adjustments')
def adjustments():
    return render_template('adjustments.html')

#Manage Settings
@app.route('/settings')
def settings():
    return render_template('settings.html')

#Search Inventory
@app.route('/search')
def search():
    try:
        search_string = str(request.args.get('input'))
        if search_string == None or search_string == "" or search_string == "None":
            abort(400)
    except:
        abort(400)
    return view_controllers.search.search_results_view(search_string)

#API
@app.route('/api/adjust_quantity', methods=['POST'])
def adjust_quantity():
    """ JQuery request should look like this
    $.post('/api/adjust_quantity', JSON.stringify({
    "locations": [
        {"location_id": 1, "quantity": 9},
        {"location_id": 2, "quantity": 1}
    ],
    "employee_id": 2718,
    "employee_password": "008172",
    "reason_id": 1,
    "item_sku": 1000
    }), function(data) { console.log(data)});
    """
    try:
        json = request.get_json(force=True)
        locations = json['locations']
        employee_id = json['employee_id']
        employee_password = json['employee_password']
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

@app.route('/api/create_new_cart')
def create_new_cart():
    try:
        session['cart_id'] = request.args.get('cart_title')
    except:
        abort(400)
    return jsonify(session['cart_id']), 200

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
