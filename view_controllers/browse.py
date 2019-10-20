import data_controller as db
import urllib.parse
from flask import render_template, abort

class BasicRow:
    def __init__(self, id, href, primary_text, secondary_text):
        self.id = id
        self.href = href
        self.primary_text = primary_text
        self.secondary_text = secondary_text

def browse_type_view():
    return render_template('browse.html')

def category_select_view():
    all_categories = db.get_all_categories()
    rows = []
    for category in all_categories:
        rows.append(BasicRow(
            id = category.id,
            href = '/browse/items?browse_type=Category&filter_id={}'.format(category.id),
            primary_text = category.name.title(),
            secondary_text = '{} {}'.format(
                len(category.items),
                'Item' if len(category.items) == 1 else 'Items'
            )
        )
        )
    return render_template('basic_table_view.html', 
        table_header = 'Select Category', 
        page_title='Categories', 
        rows = rows)

def location_select_view():
    all_locations = db.get_all_locations()
    rows = []
    for location in all_locations:
        rows.append(BasicRow(
            id = location.id,
            href = '/browse/items?browse_type=Location&filter_id={}'.format(location.id),
            primary_text = location.name.upper(),
            secondary_text = '{} {}'.format(
                len(location.items),
                'Item' if len(location.items) == 1 else 'Items'
            )
        )
        )
    return render_template('basic_table_view.html', 
        table_header = 'Select Location', 
        page_title='Locations', 
        rows = rows)

def manufacturer_select_view():
    all_manufacturers = db.get_all_manufacturers()
    rows = []
    for manufacturer in all_manufacturers:
        number_of_items = db.count_items_by_manufacturer(manufacturer)
        rows.append(BasicRow(
            id = manufacturer,
            href = '/browse/items?browse_type=Manufacturer&filter_id={}'.format(urllib.parse.quote(manufacturer)),
            primary_text = manufacturer.title(),
            secondary_text = '{} {}'.format(
                number_of_items,
                'Item' if number_of_items == 1 else 'Items'
            )
        )
        )
    return render_template('basic_table_view.html', 
        table_header = 'Select Manufacturer', 
        page_title='Manufacturers', 
        rows = rows)

def items_view(browse_type, filter_id):
    items = []
    rows = []
    if browse_type == 'Category':
        category = db.session.query(db.Category).filter(db.Category.id==filter_id).one()
        table_header = '{}s'.format(category.name.title())
        page_title = '{}s'.format(category.name.title())
        items = db.get_items_by_category_id(filter_id)
    elif browse_type == 'Location':
        location = db.session.query(db.Location).filter(db.Location.id==filter_id).one()
        table_header = 'Items in {}'.format(location.name.upper())
        page_title = location.name.upper()
        items = db.get_items_by_location_id(filter_id)
    elif browse_type == 'Manufacturer':
        table_header = 'Items from {}'.format(filter_id.title())
        page_title = filter_id.title()
        items = db.get_items_by_manufacturer(filter_id)
    elif browse_type == 'All':
        table_header = 'All Items'
        page_title = 'All Items'
        items = db.get_all_items()
    else:
        abort(400)
    for item in items:
        rows.append(BasicRow(
            id = item.sku,
            href = '/item/{}'.format(item.sku),
            primary_text = '{} {}'.format(item.manufacturer.title(), item.part_no.upper()),
            secondary_text = 'Quantity: {}'.format(item.total_quantity)
        )
        )
    return render_template('basic_table_view.html', 
        table_header = table_header, 
        page_title = page_title, 
        rows = rows)


def item_detail_view(sku: int):
    item = db.get_item_by_sku(sku)
    return render_template('item_detail_view.html', item = item)
