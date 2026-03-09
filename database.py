# Verbindung & Initialisierung
import sqlalchemy as db
print("SQLAlchemiy version:", db.__version__)

engine = db.create_engine('sqlite:///measy_database.db')
conn = engine.connect()