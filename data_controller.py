from data_model import session, Item, Location, Adjustment, AdjustmentLocation, LocationItem, Employee, AdjustmentReason, Category, Picklist, PicklistItem
import data_model as db
from sqlalchemy import func, and_, or_
from math import ceil
from datetime import datetime, date
from flask import abort

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
    return session.query(Category).all()

def get_all_locations() -> [Location]:
    locations = session.query(Location).all()
    for i in range(len(locations)):
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
    return session.query(Employee).all()

def get_all_reasons() -> [AdjustmentReason]:
    return session.query(AdjustmentReason).all()

def count_adjustment_dates() -> int:
    return session.query(Adjustment.date).group_by(Adjustment.date).count()

def get_adjustment_dates(page: int = 0) -> [date]:
    dates = []
    for row in session.query(Adjustment.date).group_by(Adjustment.date).limit(page_limit).offset(page_limit * page).all():
        dates.append(row[0])
    dates.sort()
    return dates

# Authentication
def login_employee(employee_id: int, password: str) -> bool:
    try:
        employee: Employee = session.query(Employee).filter(Employee.id==employee_id).one()
    except:
        return False
    return employee.check_password(password)

# Search items by SKU, Part_no, or Description

def get_search_results(search_string: str, page: int = 0) -> [Item]:
    results = []
    if len(search_string) < 3:
        return None
    try:
        results.append(session.query(Item).filter(Item.sku==int(search_string)).one())
        return results
    except:
        pass
    search = "%{}%".format(search_string)
    for row in session.query(Item).\
            filter(or_(Item.part_no.like(search), Item.description.like(search))).\
            limit(page_limit).\
            offset(page_limit * page).all():
        results.append(row)
    return results


def count_search_results(search_string: str) -> int:
    count = 0
    if len(search_string) < 3:
        return None
    try:
        item = session.query(Item).filter(Item.sku==int(search_string)).one()
        return 1
    except:
        pass
    search = "%{}%".format(search_string)
    for row in session.query(Item).filter(or_(Item.part_no.like(search), Item.description.like(search))).all():
        count += 1
    return count

# Modify database

def create_new_item(part_no: str, description: str, manufacturer: str, category: Category) -> Item:
    new_item = Item(part_no=part_no, description=description, manufacturer=manufacturer, category=category)
    try:
        session.add(new_item)
        session.commit()
        return new_item
    except:
        return None

def adjust_quantities_for_item(locations, employee_id: int, reason_id: int, item_sku: int) -> str:
    # Locations argument should be a dictionary with keys 'location_id' and 'quantity'
    try:
        item = get_item_by_sku(item_sku)
        reason = session.query(AdjustmentReason).filter(AdjustmentReason.id==reason_id).one()
        employee = session.query(Employee).filter(Employee.id == employee_id).one()
        item.locations = []
        for l in locations:
            quantity = l['quantity']
            if quantity > 0:
                location = session.query(Location).filter(Location.id==int(l['location_id'])).one()
                association = LocationItem(quantity = quantity)
                association.item = item
                association.location = location
                session.add(association)
        return 'Success'
    except:
        session.rollback()
        abort(500)

def add_new_location(location_name):
    try:
        location = session.query(Location).filter(Location.name == location_name.lower()).one()
    except:
        location = Location(name = location_name.lower())
        session.add(location)
        session.commit()
    return location

def create_new_picklist(picklist_title, employee_id):
    picklist = Picklist(title = picklist_title, status = 'open')
    try:
        employee = session.query(Employee).filter(Employee.id == employee_id).one()
        picklist.employee = employee
        session.add(picklist)
        session.commit()
    except:
        session.rollback()
        abort(500)
    return picklist

def create_new_adjustment(reason_id, item_sku, employee_id, qty_changes):
    """
    locations should be dict list in form of {location_id: int, old_qty: int, new_qty: int}
    """
    try:
        employee = session.query(Employee).get(employee_id)
        item = session.query(Item).get(item_sku)
        reason = session.query(AdjustmentReason).get(reason_id)
    except:
        print('unable to get employee, reason, or item')
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
            location = session.query(Location).get(qty_change['location_id'])
        except:
            print('unable to get location {}'.format(qty_change['location_id']))
            abort(400)
        new_adj_location = AdjustmentLocation(new_qty = qty_change['new_qty'], old_qty = qty_change['old_qty'])
        new_adj_location.adjustment = new_adjustment
        new_adj_location.location = location
        try:
            session.add(new_adj_location)
        except:
            session.rollback()
            print('unable to add adj_location {}'.format(new_adj_location))
            abort(500)
    return new_adjustment.id