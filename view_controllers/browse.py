import data_controller as db
from flask import render_template

def browse_type_view():
    return render_template('browse.html')

def category_select_view():
    return render_template('placeholder.html', page_name='category select view')

def location_select_view():
    return render_template('placeholder.html', page_name='location select view')

def manufacturer_select_view():
    return render_template('placeholder.html', page_name='manufacturer select view')

def all_items_view(page = 0):
    return render_template('placeholder.html', page_name='all items view page: {}'.format(page))

def item_detail_view(sku: int):
    return render_template('placeholder.html', page_name='item details: sku = {}'.format(sku))
