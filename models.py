# Alle Tabellen als SQLAlchemy-Klassen

# Datentypen und Tabellenregeln (Constraints) für Spalten.
# Explizite Variante, um sqlalchemy.Integer etc. zu vermeiden
from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey, DateTime, Float, Boolean
# Basisklasse, von der alle Tabellen-Klassen erben
from sqlalchemy.orm import DeclarativeBase

#Instanz der Basisklasse -> Vererbung
class Base(DeclarativeBase):
    pass

# Reihenfolge der Klassen kann relevant sein, daher auf die Reihenfolge der Referenzen achten.

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    email_address = Column(String, unique=True , nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default = 'user', nullable=False)

    # __table_args__ definiert Regeln für die gesamte Tabelle (z.B. CHECK-Constraints)
    # CheckConstraint prüft ob der Wert einer Spalte nur bestimmte Werte annehmen darf
    __table_args__ = (
        CheckConstraint("role IN ('admin','user')"),  # Komma, da dies ein Tupel ist
    )

class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    meeting_type = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    virtual_location = Column(String, nullable=True)

    __table_args__ = (
        CheckConstraint("meeting_type IN ('physical','virtual')"),
    )

class Appointment(Base):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_datetime = Column(DateTime, nullable=True)
    end_datetime = Column(DateTime, nullable=True)

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    appointment_id = Column(Integer, ForeignKey('appointment.id'), nullable=False)
    status_attend = Column(String, default = 'invited', nullable=False)

    __table_args__ = (
        CheckConstraint("status_attend IN ('invited','confirmed','declined')"),
    )

class Poll(Base):
    __tablename__ = 'poll'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    appointment_id = Column(Integer, ForeignKey('appointment.id'), nullable=False)
    description = Column(String, nullable=True)

class Choice(Base):
    __tablename__ = 'choice'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    poll_id = Column(Integer, ForeignKey('poll.id'), nullable=False)
    label = Column(String, nullable=False)

class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    choice_id = Column(Integer, ForeignKey('choice.id'), nullable=False)
    can_attend = Column(Boolean, default = 0 , nullable=False)