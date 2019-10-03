from data_model import session, Item, Location, Adjustment, AdjustmentLocation, LocationItem, Employee, AdjustmentReason, Category
import data_model as db
from sqlalchemy import func, and_, or_
from math import ceil
from datetime import datetime, date

page_limit = 20

# Browse page database access
def get_item_by_sku(sku: str) -> Item:
    return session.query(Item).filter(Item.sku==sku).one()

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
    return session.query(func.count(Item.sku))

def get_all_manufacturers() -> [str]:
    manufacturers = []
    for row in session.query(Item.manufacturer).group_by(Item.manufacturer).all():
        manufacturers.append(row[0].capitalize())
    manufacturers.sort()
    return manufacturers

def get_all_categories() -> [Category]:
    return session.query(Category).all()

def get_all_locations() -> [Location]:
    return session.query(Location).all()

# Adjustments page database access

def get_adjustment_by_id(adjustment_id: int) -> Adjustment:
    return session.query(Adjustment).filter(Adjustment.id==adjustment_id).one()

def get_adjustments_by_employee_id(employee_id: int, page: int = 0) -> [Adjustment]:
    return session.query(Adjustment).filter(Adjustment.employee_id==employee_id).limit(page_limit).offset(page_limit * page).all()

def count_adjustments_by_employee_id(employee_id: int) -> int:
    return session.query(func.count(Adjustment.id)).filter(Adjustment.employee_id==employee_id).scalar()

def get_adjustments_by_sku(sku: int, page: int = 0) -> [Adjustment]:
    return session.query(Adjustment).filter(Adjustment.item_sku==sku).limit(page_limit).offset(page_limit * page).all()

def count_adjustments_by_sku(sku: int) -> int:
    return session.query(func.count(Adjustment.id)).filter(Adjustment.item_sku==sku).scalar()

def get_adjustments_by_reason_id(reason_id: int, page: int = 0) -> [Adjustment]:
    return session.query(Adjustment).filter(Adjustment.reason_id==reason_id).limit(page_limit).offset(page_limit * page).all()

def count_adjustments_by_reason_id(reason_id: int) -> int:
    return session.query(func.count(Adjustment.id)).filter(Adjustment.reason_id==reason_id).scalar()

def get_adjustments_by_date(date1: date, date2: date = None, page: int = 0) -> [Adjustment]:
    if date2 == None:
        date2 = date1
    return session.query(Adjustment).\
        filter(and_(Adjustment.date>=date1, Adjustment.date<=date2)).\
        limit(page_limit).offset(page_limit * page).all()

def count_adjustments_by_date(date1: date, date2: date = None) -> int:
    if date2 == None:
        date2 == date1
    return session.query(func.count(Adjustment.id)).filter(and_(Adjustment.date>=date1, Adjustment.date<=date2)).scalar()

def get_all_employees() -> [Employee]:
    return session.query(Employee).all()

def get_all_reasons() -> [AdjustmentReason]:
    return session.query(AdjustmentReason).all()

# Authentication
def loginEmployee(employee_id: int, password: str) -> bool:
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

def adjust_quantities_for_item():
    pass

def add_location():
    pass

def delete_location():
    pass

def create_adjustment():
    pass


