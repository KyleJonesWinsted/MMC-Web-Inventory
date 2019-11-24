import xlrd
import data_model as db
from random import randint
from random import seed

seed(1)

loc = ("INVENTORY TRACKER KJP REV 2.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

dictionary = {}
items = []
desc_keys = ['DESCRIPTION', 'COMMON', 'CYCLE COUNT', 'TYPE', 'DIAMETER', 'MIN', 'MAX', 'RE-GRIND', 'SUPPLIER', 'PRICE', 'OBSOLETE', 'SPARE PARTS', 'MMC PART NUMBER', 'MMC PART NUMBER2', 'MMC PART NUMBER3', 'MMC PART NUMBER4']

def create_dictionary():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols
    column_names = sheet.row_values(0)
    for i in range(1, number_of_rows):
        values = {}
        for j in range(number_of_columns):
            values[column_names[j]] = sheet.row_values(i)[j]
        dictionary[int(sheet.cell_value(i, 0))] = values
        values = {}

def create_new_items(dictionary):
    for sku, values in dictionary.items():
        description = ""
        for key2, value2 in values.items():
            if key2 in desc_keys and value2 != "":
                description += "{}: {} | ".format(key2.upper(), value2)
        new_item = db.Item(sku = int(values['SKU']), 
            part_no = values['PN'].lower(), 
            description = description, 
            manufacturer = values['MANUFACTURER'].lower() if values['MANUFACTURER'] != "" else "unknown",
            category_id = int(values['CATEGORY_ID']))
        items.append(new_item)

def import_to_inventory():
    create_dictionary()
    create_new_items(dictionary)
    for item in items:
        db.session.add(item)
    db.session.commit()

location_items = []

def create_location_items(dictionary):
    for sku, values in dictionary.items():
        if sku != 998 and values['LOCATION_ID'] != "":
            quantity = randint(0, 6)
            new_location_item = db.LocationItem(item_sku = sku, location_id = values['LOCATION_ID'], quantity = quantity)
            location_items.append(new_location_item)
            """if values['LOCATION_ID2'] != "":
                quantity2 = randint(0,10)
                new_location_item2 = db.LocationItem(item_sku = sku, location_id = values['LOCATION_ID2'], quantity = quantity2)
                db.session.add(new_location_item2)
            """