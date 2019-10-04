from flask import Flask, render_template, request
import view_controllers.browse
app = Flask(__name__)

#Homepage
@app.route('/')
def index():
    return render_template('homepage.html')

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

@app.route('/browse/all_items')
def browse_all_items():
    try:
        page_number = int(request.args.get('page'))
    except:
        page_number = None
    return view_controllers.browse.all_items_view(page=page_number)
    
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
@app.route('/search/<search_string>')
def search(search_string=""):
    return render_template('search.html', search_string=search_string)

if __name__ == '__main__':
    app.run(debug=True)
