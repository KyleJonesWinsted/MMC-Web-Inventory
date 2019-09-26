from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgres://localhost/mmc_web_inventory', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

