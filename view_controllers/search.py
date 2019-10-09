from flask import render_template, abort
import data_controller as db
import app
from .browse import BasicRow

def search_results_view(search_string):
    number_of_results = db.count_search_results(search_string)
    if number_of_results == 1:
        items = db.get_search_results(search_string)
        return app.view_item_details(items[0].sku)
    elif number_of_results == None:
        abort(400)
    elif number_of_results == 0:
        return render_template('basic_table_view.html', 
            table_header = 'No Results Found',
            page_title = '0 Search Results',
            rows = [])
    else:
        items = db.get_search_results(search_string)
        rows = []
        for item in items:
            rows.append(
                BasicRow(
                    id = item.sku,
                    href = '/item/{}'.format(item.sku),
                    primary_text = '{} - {}'.format(item.manufacturer.title(), item.part_no.upper()),
                    secondary_text = 'Quantity: {}'.format(item.total_quantity)
                )
            )
        return render_template('basic_table_view.html',
            table_header = 'Results for "{}"'.format(search_string),
            page_title = '{} Search Results'.format(number_of_results),
            rows = rows)

