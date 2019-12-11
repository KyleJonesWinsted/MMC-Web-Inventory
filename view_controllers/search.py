from flask import render_template, abort, redirect, url_for
from math import ceil
import data_controller as db
import app
from .browse import BasicRow

def search_results_view(search_string, page_number):
    matched_skus = db.count_search_results(search_string)
    number_of_results = len(matched_skus)
    if number_of_results == 1:
        items = db.get_search_results(matched_skus)
        return redirect('/item/{}'.format(items[0].sku), code=302)
    elif number_of_results == None:
        abort(400)
    elif number_of_results == 0:
        return render_template('basic_table_view.html', 
            table_header = 'No Results Found',
            page_title = '0 Search Results',
            rows = [])
    else:
        page_count = ceil(number_of_results / db.page_limit)
        items = db.get_search_results(matched_skus, page_number)
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
            rows = rows,
            total_pages = page_count,
            current_page = page_number + 1)

