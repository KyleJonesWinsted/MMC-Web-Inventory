from data_model import session, Item, Location, Adjustment, AdjustmentLocation, LocationItem, Employee, AdjustmentReason, Category
import data_model as db

page_limit = 20

# Browse page database access
def get_item_by_sku(sku: str) -> Item:
    return session.query(Item).filter(Item.sku==sku).one()

def get_items_by_category_id(category_id: int, page:int = 0) -> [Item]:
    return session.query(Item).filter(Item.category_id==category_id).limit(page_limit).offset(page_limit * page).all()

def get_items_by_manufacturer(manufacturer: str, page:int = 0) -> [Item]:
    return session.query(Item).filter(Item.manufacturer==manufacturer).limit(page_limit).offset(page_limit * page).all()

def get_items_by_location_id(location_id: int, page:int = 0) -> [Item]:
    items = []
    query = session.query(LocationItem).filter(LocationItem.location_id==location_id).limit(page_limit).offset(page_limit * page)
    for row in query:
        items.append(row.item)
    return items

def get_all_items(page: int = 0) -> [Item]:
    return session.query(Item).limit(page_limit).offset(page_limit * page).all()

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



# Authentication
def loginEmployee(employee_id: int, password: str) -> bool:
    try:
        employee: Employee = session.query(Employee).filter(Employee.id==employee_id).one()
    except:
        return False
    return employee.check_password(password)