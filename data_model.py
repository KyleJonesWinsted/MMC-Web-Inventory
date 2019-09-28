from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('postgres://localhost/mmc_web_inventory', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Item(Base):
    __tablename__ = "items"

    # CUSTOM SEQUENCE sku = Column(Integer, primary_key=True)
    part_no = Column(String(50))
    description = Column(String)
    manufacturer = Column(String(50))

    def __repr__(self):
        return "Item(sku: {}, part_no: {}, manufacturer: {})".format(self.sku, self.part_no, self.manufacturer)

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __repr__(self):
        return "Location(id: {}, name: {})".format(self.id, self.name)

class Adjustment(Base):
    __tablename__ = "adjustments"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime(timezone=False), server_default=func.now())

    def __repr__(self):
        return "Adjustment(ID: {}, datetime: {})".format(self.id, self.datetime)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    min_qty = Column(Integer)
    img_url = Column(String)

    def __repr__(self):
        return "Category(id: {}, name: {}, min_qty: {})".format(self.id, self.name, self.min_qty)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password_hash = Column(String(128))

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

    def __repr__(self):
        return "AdjustmentReason(id: {}, name: {})".format(self.id, self.name)

class LocationItem(Base):
    __tablename__ = "location_items"


class AdjustmentLocation(Base):
    __tablename__ = "adjustments_locations"

