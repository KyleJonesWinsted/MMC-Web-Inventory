from data_model import session, Item, Location, Adjustment, AdjustmentLocation, LocationItem, Employee, AdjustmentReason, Category
import data_model as db

# Browse page database access
def get_item_by_sku(sku: str) -> Item:
    return session.query(Item).filter(Item.sku==sku).one()

def get_items_by_category_id(category_id: int) -> [Item]:
    return session.query(Item).filter(Item.category_id==category_id).all()

def get_items_by_manufacturer(manufacturer: str) -> [Item]:
    return session.query(Item).filter(Item.manufacturer==manufacturer).all()

def get_items_by_location_id(location_id: int) -> [Item]:
    items = []
    for row in session.query(LocationItem).filter(LocationItem.location_id==location_id):
        items.append(row.item)
    return items

def get_all_items() -> [Item]:
    return session.query(Item).all()

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