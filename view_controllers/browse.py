import data_controller as db
from flask import render_template

def browse_type_view():
    return render_template('browse.html')

def category_select_view():
    all_categories = db.get_all_categories()
    rows = []
    for category in all_categories:
        rows.append(
            {
                'id': category.id, 
                'primary-text': category.name.title(), 
                'secondary-text': len(category.items)
            }
        )
    return render_template('basic_table_view.html', browse_type='Category', rows = rows)

def location_select_view():
    all_locations = db.get_all_locations()
    rows = []
    for location in all_locations:
        rows.append(
            {
                'id': location.id,
                'primary-text': location.name.upper(),
                'secondary-text': len(location.items)
            }
        )
    return render_template('basic_table_view.html', browse_type='Location', rows = rows)

def manufacturer_select_view():
    all_manufacturers = db.get_all_manufacturers()
    rows = []
    for manufacturer in all_manufacturers:
        number_of_items = db.count_items_by_manufacturer(manufacturer)
        rows.append(
            {
                'id': manufacturer,
                'primary-text': manufacturer.title(),
                'secondary-text': number_of_items
            }
        )
    return render_template('basic_table_view.html', browse_type = 'Manufacturer', rows = rows)

def all_items_view(page = 0):
    return render_template('placeholder.html', page_name='all items view page: {}'.format(page))

def item_detail_view(sku: int):
    return render_template('placeholder.html', page_name='item details: sku = {}'.format(sku))
