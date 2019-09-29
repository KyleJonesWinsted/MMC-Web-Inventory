from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('postgres://localhost/mmc_web_inventory', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Item(Base):
    __tablename__ = "items"

    sku = Column(Integer, Sequence('item_skus'), primary_key=True)
    part_no = Column(String(50))
    description = Column(String)
    manufacturer = Column(String(50))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='items')
    locations = relationship('LocationItem', back_populates='item', cascade="all, delete, delete-orphan")
    adjustments = relationship('Adjustment', back_populates='item')

    @hybrid_property
    def total_quantity(self):
        quantity = 0
        for location in self.locations:
            quantity += location.quantity
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

    def __repr__(self):
        return "Location(id: {}, name: {})".format(self.id, self.name)

class Adjustment(Base):
    __tablename__ = "adjustments"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime(timezone=False), server_default=func.now())
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

    def __repr__(self):
        return "Adjustment(ID: {}, datetime: {}, item: {})".format(self.id, self.datetime, self.item.part_no)

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
    adjustments = relationship('Adjustment', back_populates='employee')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "Employee(id: {}, name: {})".format(self.id, self.name)

class AdjustmentReason(Base):
    __tablename__ = "adjustments_reasons"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    adjustments = relationship('Adjustment', back_populates='reason')

    def __repr__(self):
        return "AdjustmentReason(id: {}, name: {})".format(self.id, self.name)

class LocationItem(Base):
    __tablename__ = "location_items"

    item_sku = Column(Integer, ForeignKey('items.sku'), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)
    quantity = Column(Integer)
    item = relationship('Item', back_populates='locations')
    location = relationship('Location', back_populates='items')

    def __repr__(self):
        return "LocationItem(item: {}, location: {}, quantity: {})".format(self.item.part_no, self.location.name, self.quantity)

class AdjustmentLocation(Base):
    __tablename__ = "adjustments_locations"

    adjustment_id = Column(Integer, ForeignKey('adjustments.id'), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)
    old_qty = Column(Integer)
    new_qty = Column(Integer)
    adjustment = relationship('Adjustment', back_populates='locations')
    location = relationship('Location', back_populates='adjustments')

    def __repr__(self):
        return "AdjustmentLocation(adjustment_id: {}, location: {}, old_qty: {}, new_qty: {})".\
            format(self.adjustment_id, self.location.name, self.old_qty, self.new_qty)

