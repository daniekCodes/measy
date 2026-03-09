# Verbindung & Initialisierung
import sqlalchemy as db
from models import Base

print("SQLAlchemiy version:", db.__version__)

engine = db.create_engine('sqlite:///measy_database.db')
conn = engine.connect()

Base.metadata.create_all(engine)