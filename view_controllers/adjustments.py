import data_controller as db
from flask import render_template, abort
from math import ceil
from view_controllers.browse import BasicRow
from datetime import date

def adjustments_browse_view():
    return render_template('adjustments.html')

def employee_select_view():
    employees = db.get_all_employees()
    rows = []
    for employee in employees:
        rows.append(BasicRow(
            id = employee.id,
            href = "/adjustments/adjustments?browse_type=employee&filter_id={}".format(employee.id),
            primary_text = employee.name.title(),
            secondary_text = "ID: {}".format(employee.id)
        ))
    return render_template('basic_table_view.html',
        table_header = "Select Employee",
        page_title = "Employees",
        rows = rows)

def item_select_view(page_number = 0):
    page_count = ceil(db.count_all_items() / db.page_limit)
    rows = []
    items = db.get_all_items(page_number)
    for item in items:
        rows.append(BasicRow(
            id = item.sku,
            href = '/adjustments/adjustments?browse_type=item&filter_id={}'.format(item.sku),
            primary_text = "{} {}".format(item.manufacturer.title(), item.part_no.upper()),
            secondary_text = "SKU: {}".format(item.sku)
        ))
    return render_template('basic_table_view.html',
        table_header = "Select Item",
        page_title = "Items",
        rows = rows,
        current_page = page_number + 1,
        total_pages = page_count)

def date_select_view(page_number = 0):
    page_count = ceil(db.count_adjustment_dates() / db.page_limit)
    rows = []
    dates = db.get_adjustment_dates(page_number)
    for date in dates:
        rows.append(BasicRow(
            id = date,
            href = '/adjustments/adjustments?browse_type=date&filter_id={}'.format(date),
            primary_text = date.strftime("%a, %b %e %Y"),
            secondary_text = "",
        ))
    return render_template('basic_table_view.html',
        table_header = "Select Date",
        page_title = "Dates",
        rows = rows,
        current_page = page_number + 1,
        total_pages = page_count)

def reason_select_view():
    reasons = db.get_all_reasons()
    rows = []
    for reason in reasons:
        rows.append(BasicRow(
            id = reason.id,
            href = '/adjustments/adjustments?browse_type=reason&filter_id={}'.format(reason.id),
            primary_text = reason.name.title(),
            secondary_text = ""
        ))
    return render_template('basic_table_view.html',
        table_header = "Select Reason",
        page_title = "Reasons",
        rows = rows)

def adjustments_view(browse_type, filter_id, page_number = 0):
    adjustments = []
    rows = []
    if browse_type == 'employee':
        employee = db.session.query(db.Employee).filter(db.Employee.id == filter_id).one()
        table_header = "Adjustments by {}".format(employee.name.title())
        page_title = employee.name.title()
        adjustment_count = db.count_adjustments_by_employee_id(filter_id)
        adjustments = db.get_adjustments_by_employee_id(filter_id, page_number)
    elif browse_type == 'date':
        filter_date = date(int(filter_id[0:4]), int(filter_id[5:7]), int(filter_id[8:]))
        print(filter_date)
        table_header = "Adjustments on {}".format(filter_date.strftime("%a, %b %e %Y"))
        page_title = filter_date.strftime("%a, %b %e %Y")
        adjustment_count = db.count_adjustments_by_date(filter_date)
        adjustments = db.get_adjustments_by_date(filter_date, None, page_number)
    elif browse_type == 'item':
        item = db.get_item_by_sku(filter_id)
        table_header = "Adjustments to {}".format(item.part_no.upper())
        page_title = item.part_no.upper()
        adjustment_count = db.count_adjustments_by_sku(filter_id)
        adjustments = db.get_adjustments_by_sku(filter_id, page_number)
    elif browse_type == 'reason':
        reason = db.session.query(db.AdjustmentReason).filter(db.AdjustmentReason.id == filter_id).one()
        table_header = "Adjustments for {}".format(reason.name.title())
        page_title = reason.name.upper()
        adjustment_count = db.count_adjustments_by_reason_id(filter_id)
        adjustments = db.get_adjustments_by_reason_id(filter_id, page_number)
    else:
        abort(400)
    page_count = ceil(adjustment_count / db.page_limit)
    for adjustment in adjustments:
        rows.append(BasicRow(
            id = adjustment.id,
            href = '/adjustment/{}'.format(adjustment.id),
            primary_text = "{} - {}".format(adjustment.item.part_no.upper(), adjustment.datetime.strftime("%m/%d/%y %I:%M %p")),
            secondary_text = "Qty Change: {}".format(adjustment.total_qty_change)
        ))
    return render_template('basic_table_view.html',
        table_header = table_header,
        page_title = page_title,
        rows = rows,
        current_page = page_number + 1,
        total_pages = page_count)

def adjustment_detail_view(adjustment_id):
    adjustment = db.get_adjustment_by_id(adjustment_id)
    return render_template('adjustment_detail_view.html', adjustment = adjustment)