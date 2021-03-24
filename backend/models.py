# from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, DateTime
from sqlalchemy import *
from datetime import datetime

try:
    from .config import DB_URI
except:
    from config import DB_URI

metadata = MetaData()

# example of a DB Table
cars = Table('cars', metadata,
    Column('Id', Integer, primary_key=True),
    Column('Title', String(120)),
    Column('Brand_id', Integer, ForeignKey("brands.Brand_id")),
    Column('Model_id', Integer, ForeignKey("models.Model_id")),
    Column('DrivedDistance', Integer),
    Column('Price', Integer),
    Column('Fuel', String(20)),
    Column('DateCreated', DateTime, default=datetime.utcnow)
)

brands = Table('brands', metadata,
    Column('Brand_id', Integer, primary_key=True),
    Column('Brand', String(20)),
)

models = Table('models', metadata,
    Column('Model_id', Integer, primary_key=True),
    Column('Model', String(20)),
)



# methods which should be called on the init of the database
engine = create_engine(DB_URI)
metadata.create_all(engine)
