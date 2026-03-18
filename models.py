"""
Database model: All tables as SQLAlchemy ORM classes.

User → Appointment ← Location
User → Attendance  → Appointment
Appointment → Poll → Choice → Vote ← User
"""

from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import DeclarativeBase
from dataclasses import dataclass
from datetime import datetime

# Base class: every subclass is automatically registered as a database model
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default = 'user', nullable=False)
    softdeleted = Column(Boolean, default = False, nullable=False)
    attendance = relationship('Attendance', backref='attendance_user', cascade='all, delete')
    vote = relationship('Vote', backref='vote_user', cascade='all, delete')

    # Table-wide constraints – tuple required, hence the trailing comma
    __table_args__ = (
        CheckConstraint("role IN ('admin','user')"),
    )

# Depending on meeting_type, either physical address/coordinates or virtual_location is populated
class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    meeting_type = Column(String, nullable=False)
    street = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    city = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    virtual_location = Column(String, nullable=True)
    softdeleted = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("meeting_type IN ('physical','virtual')"),
    )
@dataclass
class Appointment(Base):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_datetime = Column(DateTime, nullable=True)
    end_datetime = Column(DateTime, nullable=True)
    softdeleted = Column(Boolean, default=False, nullable=False)
    location = relationship('Location', backref='location_appointment', cascade='all, delete')
    attendance = relationship('Attendance', backref='attendance_appointment', cascade='all, delete')
    poll = relationship('Poll', backref='poll_appointment', cascade='all, delete')

# Attendance status of a user for a given appointment
class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    appointment_id = Column(Integer, ForeignKey('appointment.id', ondelete='CASCADE'), nullable=False)
    status_attend = Column(String, default = 'invited', nullable=False)
    softdeleted = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("status_attend IN ('invited','confirmed','declined')"),
    )

# Poll → Choice → Vote form the voting system of an appointment
class Poll(Base):
    __tablename__ = 'poll'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    appointment_id = Column(Integer, ForeignKey('appointment.id', ondelete='CASCADE'), nullable=False)
    description = Column(String, nullable=True)
    softdeleted = Column(Boolean, default=False, nullable=False)
    choice = relationship('Choice', backref='poll', cascade='all, delete')

class Choice(Base):
    # Answer options for a poll - users vote on these
    __tablename__ = 'choice'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    poll_id = Column(Integer, ForeignKey('poll.id', ondelete='CASCADE'), nullable=False)
    label = Column(String, nullable=False)
    softdeleted = Column(Boolean, default=False, nullable=False)
    vote = relationship('Vote', backref='choice', cascade='all, delete')

class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    choice_id = Column(Integer, ForeignKey('choice.id', ondelete='CASCADE'), nullable=False)
    can_attend = Column(Boolean, default = 0 , nullable=False)
    softdeleted = Column(Boolean, default=False, nullable=False)
