from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, func, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta
import os

engine = create_engine(os.environ['DATABASE_URL'], echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Item(Base):
    __tablename__ = "items"

    sku = Column(Integer, Sequence('item_skus'), primary_key=True)
    part_no = Column(String)
    description = Column(String)
    manufacturer = Column(String(50))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='items')
    locations = relationship('LocationItem', back_populates='item', cascade="all, delete, delete-orphan")
    adjustments = relationship('Adjustment', back_populates='item')
    qty_checked_out = Column(Integer, default = 0)

    @hybrid_property
    def total_quantity(self):
        quantity = 0
        for location in self.locations:
            quantity += location.quantity
        if self.qty_checked_out != None:
            quantity += self.qty_checked_out
        return quantity

    @hybrid_property
    def is_below_minimum_qty(self):
        if self.category == None:
            return False
        return self.category.min_qty > self.total_quantity

    def __repr__(self):
        return "Item(sku: {}, part_no: {}, manufacturer: {})".format(self.sku, self.part_no, self.manufacturer)

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    items = relationship('LocationItem', back_populates='location')
    adjustments = relationship('AdjustmentLocation', back_populates='location')

    @hybrid_property
    def total_quantity(self):
        quantity = 0
        for item in self.items:
            quantity += item.quantity
        return quantity

    def __repr__(self):
        return "Location(id: {}, name: {})".format(self.id, self.name)

class Adjustment(Base):
    __tablename__ = "adjustments"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime(timezone=False), server_default=func.now())
    date = Column(Date, default=date.today)
    item_sku = Column(Integer, ForeignKey('items.sku'))
    item = relationship('Item', back_populates='adjustments')
    locations = relationship('AdjustmentLocation', back_populates='adjustment')
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee', back_populates='adjustments')
    reason_id = Column(Integer, ForeignKey('adjustments_reasons.id'))
    reason = relationship('AdjustmentReason', back_populates='adjustments')

    @hybrid_property
    def total_qty_change(self):
        quantity = 0
        for location in self.locations:
            quantity += location.new_qty - location.old_qty
        return quantity

    @hybrid_property
    def cst_datetime(self):
        return self.datetime - timedelta(hours=6)

    def __repr__(self):
        part_no = self.item.part_no if self.item != None else 'None'
        return "Adjustment(ID: {}, datetime: {}, item: {})".format(self.id, self.datetime.strftime('%D %I:%M %p'), part_no)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    min_qty = Column(Integer)
    img_url = Column(String)
    items = relationship('Item', back_populates='category')

    def __repr__(self):
        return "Category(id: {}, name: {}, min_qty: {})".format(self.id, self.name, self.min_qty)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password_hash = Column(String(128))
    credentials = Column(String(50))
    # Credentials include 'admin', 'employee', and 'demo'
    adjustments = relationship('Adjustment', back_populates='employee')
    picklists = relationship('Picklist', back_populates='employee')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "Employee(id: {}, name: {})".format(self.id, self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'credentials': self.credentials
        }

class AdjustmentReason(Base):
    __tablename__ = "adjustments_reasons"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    adjustments = relationship('Adjustment', back_populates='reason')

    def __repr__(self):
        return "AdjustmentReason(id: {}, name: {})".format(self.id, self.name)

class LocationItem(Base):
    __tablename__ = "location_items"

    id = Column(Integer, Sequence('location_item_seq'), unique=True)
    item_sku = Column(Integer, ForeignKey('items.sku'), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)
    quantity = Column(Integer)
    item = relationship('Item', back_populates='locations')
    location = relationship('Location', back_populates='items')
    picklists = relationship('PicklistItem', back_populates='location_item')

    def __repr__(self):
        location_name = self.location.name if self.location != None else 'None'
        part_no = self.item.part_no if self.item != None else 'None'
        return "LocationItem(item: {}, location: {}, quantity: {})".format(part_no, location_name, self.quantity)

class AdjustmentLocation(Base):
    __tablename__ = "adjustments_locations"

    adjustment_id = Column(Integer, ForeignKey('adjustments.id'), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)
    old_qty = Column(Integer)
    new_qty = Column(Integer)
    adjustment = relationship('Adjustment', back_populates='locations')
    location = relationship('Location', back_populates='adjustments')

    @hybrid_property
    def quantity_change(self):
        return self.new_qty - self.old_qty

    def __repr__(self):
        location_name = self.location.name if self.location != None else 'None'
        adjustment_id = self.adjustment.id if self.adjustment != None else 'None'
        return "AdjustmentLocation(adjustment_id: {}, location: {}, old_qty: {}, new_qty: {})".\
            format(adjustment_id, location_name, self.old_qty, self.new_qty)

class Picklist(Base):
    __tablename__ = "picklists"

    id = Column(Integer, primary_key=True)
    title = Column(String(140))
    status = Column(String(24))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee', back_populates='picklists')
    datetime = Column(DateTime(timezone=False), server_default=func.now())
    location_items = relationship('PicklistItem', back_populates='picklist', cascade="all, delete, delete-orphan")

    @hybrid_property
    def number_of_items(self):
        """quantity = 0
        for picklist_item in self.location_items:
            quantity += picklist_item.quantity
        return quantity"""
        return len(self.location_items)

    def __repr__(self):
        return "Picklist(title: {}, status: {})".format(self.title, self.status)

class PicklistItem(Base):
    __tablename__ = 'picklist_items'

    id = Column(Integer, Sequence('picklist_item_seq'), unique=True)
    location_item_id = Column(Integer, ForeignKey('location_items.id'), primary_key=True)
    picklist_id = Column(Integer, ForeignKey('picklists.id'), primary_key=True)
    quantity = Column(Integer)
    location_item = relationship('LocationItem', back_populates='picklists')
    picklist = relationship('Picklist', back_populates='location_items')

    def __repr__(self):
        location_item_id = self.location_item_id if self.location_item_id != None else 'None'
        picklist_id = self.picklist_id if self.picklist_id != None else 'None'
        return "PicklistItem(id: {}, location_item_id: {}, picklist_id: {}, quantity: {})".format(self.id, location_item_id, picklist_id, self.quantity)
