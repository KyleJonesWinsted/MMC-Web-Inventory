from data_model import engine, session, Item, Location, Adjustment, AdjustmentLocation, LocationItem, Employee, AdjustmentReason, Category, Picklist, PicklistItem
import data_model as db
import traceback
from sqlalchemy import func, and_, or_, text
from math import ceil
from datetime import datetime, date
from flask import abort, jsonify

page_limit = 20

# Browse page database access
def get_item_by_sku(sku: str) -> Item:
    try:
        item = session.query(Item).filter(Item.sku==sku).one()
    except:
        return None
    return item

def get_items_by_category_id(category_id: int, page:int = 0) -> [Item]:
    return session.query(Item).filter(Item.category_id==category_id).limit(page_limit).offset(page_limit * page).all()

def count_items_by_category_id(category_id: int) -> int:
    return session.query(func.count(Item.sku)).filter(Item.category_id==category_id).scalar()

def get_items_by_manufacturer(manufacturer: str, page:int = 0) -> [Item]:
    return session.query(Item).filter(Item.manufacturer==manufacturer).limit(page_limit).offset(page_limit * page).all()

def count_items_by_manufacturer(manufacturer: str) -> int:
    return session.query(func.count(Item.sku)).filter(Item.manufacturer==manufacturer).scalar()

def get_items_by_location_id(location_id: int, page:int = 0) -> [Item]:
    items = []
    query = session.query(LocationItem).filter(LocationItem.location_id==location_id).limit(page_limit).offset(page_limit * page)
    for row in query:
        items.append(row.item)
    return items

def count_items_by_location_id(location_id: int) -> int:
    return session.query(func.count(LocationItem.item_sku)).filter(LocationItem.location_id==location_id).scalar()

def get_all_items(page: int = 0) -> [Item]:
    return session.query(Item).limit(page_limit).offset(page_limit * page).all()

def count_all_items():
    return session.query(func.count(Item.sku)).scalar()

def get_all_manufacturers() -> [str]:
    manufacturers = []
    for row in session.query(Item.manufacturer).group_by(Item.manufacturer).all():
        manufacturers.append(row[0])
    manufacturers.sort()
    return manufacturers

def get_all_categories() -> [Category]:
    return session.query(Category).order_by(Category.name).all()

def count_all_locations():
    return session.query(func.count(Location.id)).scalar()

def get_all_locations(page: int = 0) -> [Location]:
    locations = session.query(Location).order_by(Location.name).limit(page_limit).offset(page_limit * page).all()
    for i in range(len(locations)-1,-1,-1):
        if locations[i].total_quantity == 0:
            locations.pop(i)
    return locations

# Adjustments page database access

def get_adjustment_by_id(adjustment_id: int) -> Adjustment:
    return session.query(Adjustment).filter(Adjustment.id==adjustment_id).one()

def get_adjustments_by_employee_id(employee_id: int, page: int = 0) -> [Adjustment]:
    return session.query(Adjustment).\
        filter(Adjustment.employee_id==employee_id).\
        order_by(Adjustment.datetime.desc()).\
        limit(page_limit).offset(page_limit * page).all()

def count_adjustments_by_employee_id(employee_id: int) -> int:
    return session.query(func.count(Adjustment.id)).filter(Adjustment.employee_id==employee_id).scalar()

def get_adjustments_by_sku(sku: int, page: int = 0) -> [Adjustment]:
    return session.query(Adjustment).\
        filter(Adjustment.item_sku==sku).\
        order_by(Adjustment.datetime.desc()).\
        limit(page_limit).offset(page_limit * page).all()

def count_adjustments_by_sku(sku: int) -> int:
    return session.query(func.count(Adjustment.id)).filter(Adjustment.item_sku==sku).scalar()

def get_adjustments_by_reason_id(reason_id: int, page: int = 0) -> [Adjustment]:
    return session.query(Adjustment).\
        filter(Adjustment.reason_id==reason_id).\
        order_by(Adjustment.datetime.desc()).\
        limit(page_limit).offset(page_limit * page).all()

def count_adjustments_by_reason_id(reason_id: int) -> int:
    return session.query(func.count(Adjustment.id)).filter(Adjustment.reason_id==reason_id).scalar()

def get_adjustments_by_date(date1: date, date2: date = None, page: int = 0) -> [Adjustment]:
    if date2 == None:
        date2 = date1
    return session.query(Adjustment).\
        filter(and_(Adjustment.date>=date1, Adjustment.date<=date2)).\
        order_by(Adjustment.datetime.desc()).\
        limit(page_limit).offset(page_limit * page).all()

def count_adjustments_by_date(date1: date, date2: date = None) -> int:
    if date2 == None:
        date2 = date1
    return session.query(func.count(Adjustment.id)).filter(and_(Adjustment.date>=date1, Adjustment.date<=date2)).scalar()

def get_all_employees() -> [Employee]:
    return session.query(Employee).filter(and_(Employee.id != 1234, Employee.id != 1111)).order_by(Employee.name).all()

def get_all_reasons() -> [AdjustmentReason]:
    return session.query(AdjustmentReason).all()

def count_adjustment_dates() -> int:
    return session.query(Adjustment.date).group_by(Adjustment.date).count()

def get_adjustment_dates(page: int = 0) -> [date]:
    dates = []
    for row in session.query(Adjustment.date).\
            group_by(Adjustment.date).\
            limit(page_limit).\
            offset(page_limit * page).all():
        dates.append(row[0])
    dates.sort(reverse=True)
    return dates

# Authentication
def login_employee(employee_id: int, password: str) -> bool:
    try:
        employee: Employee = session.query(Employee).filter(Employee.id==employee_id).one()
    except:
        return False
    return employee.check_password(password)

# Search items by SKU, Part_no, or Description

def get_search_results(matched_skus, page: int = 0) -> [Item]:
    results = []
    page_start = page * page_limit
    for sku in matched_skus[page_start: page_start + page_limit]:
        item = session.query(Item).filter(Item.sku == sku).one()
        results.append(item)
    return results


def count_search_results(search_string: str) -> int:
    count = 0
    try:
        item = session.query(Item).filter(Item.sku==int(search_string)).one()
        return 1
    except:
        pass
    search_terms = search_string.split()
    for i in range(len(search_terms) - 1, -1, -1):
        if len(search_terms[i]) < 3:
            search_terms.pop(i)
    sql = "SELECT sku FROM items WHERE "
    for i in range(len(search_terms)):
        term = search_terms[i]
        search = "%{}%".format(term)
        sql += "(part_no LIKE '{}' OR description ILIKE '{}') ".format(search, search)
        if i < len(search_terms) - 1:
            sql += "AND "
    con = engine.connect()
    rows = con.execute(text(sql))
    fetched_results = rows.fetchall()
    con.close()
    matched_skus = []
    for result in fetched_results:
        matched_skus.append(result[0])
    return matched_skus

# Modify database

def create_new_item(part_no: str, description: str, manufacturer: str, category_id: int) -> Item:
    try:
        category = session.query(Category).filter(Category.id == category_id).one()
    except:
        traceback.print_exc()
        abort(400)
    new_item = Item(part_no=part_no.lower(), description=description, manufacturer=manufacturer.lower(), category_id=category_id)
    try:
        session.add(new_item)
        return new_item
    except:
        traceback.print_exc()
        abort(500)

def modify_item_details(item_sku, part_no, manufacturer, description, category_id):
    try:
        item = session.query(Item).filter(Item.sku == item_sku).one()
    except:
        abort(400)
    item.part_no = part_no
    item.description = description
    item.manufacturer = manufacturer
    item.category_id = category_id
    return item

def adjust_quantities_for_item(locations, employee_id: int, reason_id: int, item_sku: int) -> str:
    # Locations argument should be a dictionary with format {'location_id': 'quantity'}
    try:
        item = get_item_by_sku(item_sku)
        reason = session.query(AdjustmentReason).filter(AdjustmentReason.id==reason_id).one()
        employee = session.query(Employee).filter(Employee.id == employee_id).one()
        qty_changes = []
        for location_item in item.locations:
            old_qty = location_item.quantity
            new_qty = locations[location_item.id]
            qty_changes.append({
                'location_id': location_item.location.id,
                'old_qty': old_qty,
                'new_qty': new_qty
            })
            location_item.quantity = new_qty
        item.qty_checked_out = locations['checked-out']
        create_new_adjustment(reason.id, item.sku, employee.id, qty_changes)
        return 'Success'
    except Exception as e:
        traceback.print_exc()
        session.rollback()
        abort(500)

def add_new_location(location_name, item_sku):
    try:
        item = session.query(Item).get(item_sku)
    except:
        abort(400)
    try:
        location = session.query(Location).filter(Location.name == location_name.upper()).one()
    except:
        location = Location(name = location_name.upper())
        session.add(location)
    for location_item in item.locations:
        if location_item.location.id == location.id:
            return location_item.id
    location_item = LocationItem(quantity = 0)
    session.add(location_item)
    location_item.location = location
    location_item.item = item
    return location_item.id

def delete_location_item(location_item_id):
    try:
        location_item = session.query(LocationItem).filter(LocationItem.id == location_item_id).one()
    except:
        abort(400)
    if location_item.quantity != 0 or location_item.picklists != []:
        return 409
    session.delete(location_item)
    return 200

def create_new_picklist(picklist_title, employee_id):
    picklist = Picklist(title = picklist_title, status = 'open')
    try:
        employee = session.query(Employee).filter(Employee.id == employee_id).one()
        picklist.employee = employee
        session.add(picklist)
    except:
        session.rollback()
        abort(500)
    return picklist

def create_new_adjustment(reason_id, item_sku, employee_id, qty_changes):
    """
    qty_changes should be dict list in form of {location_id: int, old_qty: int, new_qty: int}
    """
    try:
        employee = session.query(Employee).get(employee_id)
        item = session.query(Item).get(item_sku)
        reason = session.query(AdjustmentReason).get(reason_id)
    except:
        abort(400)
    new_adjustment = Adjustment()
    new_adjustment.employee = employee
    new_adjustment.item = item
    new_adjustment.reason = reason
    try:
        session.add(new_adjustment)
    except:
        session.rollback()
        abort(500)
    for qty_change in qty_changes:
        try:
            location = session.query(Location).filter(Location.id == qty_change['location_id']).one()
        except:
            abort(400)
        new_adj_location = AdjustmentLocation(new_qty = qty_change['new_qty'], old_qty = qty_change['old_qty'])
        new_adj_location.adjustment = new_adjustment
        new_adj_location.location = location
        try:
            session.add(new_adj_location)
        except:
            session.rollback()
            abort(500)
    return new_adjustment.id

def create_new_employee(id, name, credentials, password):
    valid_credentials = ['admin', 'employee', 'demo']
    if credentials not in valid_credentials:
        return "Invalid credentials entered"
    new_employee = Employee(id = id, name = name.lower(), credentials = credentials)
    new_employee.set_password(password)
    session.add(new_employee)
    return new_employee