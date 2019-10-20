import data_controller as db
from flask import render_template, abort

def adjust_stock_for_item_view(item_sku: int):
    try:
        item = db.get_item_by_sku(item_sku)
        reasons = db.get_all_reasons()
    except:
        abort(400)
    return render_template('adjust_stock_for_item.html', item = item, reasons = reasons)