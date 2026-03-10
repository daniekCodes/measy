"""
CRUD operations for all database tables.
Validation for constrained fields (role, meeting_type, status_attend) is handled in Python before DB commit.
"""

from sqlalchemy.orm import Session
from database import engine
from models import User, Location, Appointment, Attendance, Poll, Choice, Vote

def create_user(name, email, password, role='user'):
    # role: 'user' (default) or 'admin'
    with Session(engine) as session:
        new_user = User(name=name, email=email, password=password, role=role)
        session.add(new_user)
        session.commit()

def get_user_by_id(id):
    with Session(engine) as session:
        user = session.get(User, id)
        return user

def get_user_by_email(email):
    # Query user table for matching email, return first result or None
    with Session(engine) as session:
        user = session.query(User).filter(User.email == email).first()
        return user

def update_user(id, name=None, email=None, password=None, role=None):
    with Session(engine) as session:
        user = session.get(User, id)
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if password is not None:
            user.password = password
        if role is not None:
            if role == 'user' or role == 'admin':
                user.role = role
            else:
                print(f"Invalid role '{role}' - role remains '{user.role}'")
        session.commit()

def delete_user(id):
    with Session(engine) as session:
        user = session.get(User, id)
        session.delete(user)
        session.commit()

def create_location(meeting_type, latitude=None, longitude=None, virtual_location=None):
    # meeting_type: 'physical' (requires lat/long) or 'virtual' (requires virtual_location)
    # fields for the other type must be None - validated before insert
    with Session(engine) as session:
        if meeting_type == 'physical' and virtual_location is not None:
            raise ValueError("physical location does not allow virtual_location")
        if meeting_type == 'virtual' and (latitude is not None or longitude is not None):
            raise ValueError("virtual location does not allow latitude and longitude")
        new_location = Location(meeting_type=meeting_type, latitude=latitude, longitude=longitude, virtual_location=virtual_location)
        session.add(new_location)
        session.commit()

def get_location_by_id(id):
    with Session(engine) as session:
        location = session.get(Location, id)
        return location

def update_location(id, meeting_type=None, latitude=None, longitude=None, virtual_location=None):
    # use new meeting_type if provided, otherwise keep existing one from DB
    with Session(engine) as session:
        location = session.get(Location, id)

        # determine final meeting_type & validate
        effective_type = meeting_type if meeting_type is not None else location.meeting_type
        if effective_type == 'physical' and virtual_location is not None:
            raise ValueError("physical location does not allow virtual_location")
        if effective_type == 'virtual' and (latitude is not None or longitude is not None):
            raise ValueError("virtual location does not allow latitude and longitude")

        if meeting_type is not None:
            location.meeting_type = meeting_type
            if meeting_type == 'virtual':
                print("latitude and longitude removed - virtual_location can now be set")
                location.latitude = None
                location.longitude = None
            if meeting_type == 'physical':
                print("virtual_location removed - latitude and longitude can now be set")
                location.virtual_location = None
        if latitude is not None:
            location.latitude = latitude
        if longitude is not None:
            location.longitude = longitude
        if virtual_location is not None:
            if meeting_type == 'physical' and virtual_location is not None:
                raise ValueError("physical location does not allow virtual_location")
            location.virtual_location = virtual_location
        session.commit()

def delete_location(id):
    with Session(engine) as session:
        location = session.get(Location, id)
        session.delete(location)
        session.commit()

def create_appointment(title, user_id, location_id, description=None, start_datetime=None, end_datetime=None):
    with Session(engine) as session:
        new_appointment = Appointment(title=title, user_id=user_id, location_id=location_id, description=description, start_datetime=start_datetime, end_datetime=end_datetime)
        session.add(new_appointment)
        session.commit()

def get_appointment_by_id(id):
    with Session(engine) as session:
        appointment = session.get(Appointment, id)
        return appointment

def update_appointment(id, title=None, user_id=None, location_id=None, description=None, start_datetime=None, end_datetime=None):
    with Session(engine) as session:
        appointment = session.get(Appointment, id)
        if title is not None:
            appointment.title = title
        if user_id is not None:
            appointment.user_id = user_id
        if location_id is not None:
            appointment.location_id = location_id
        if description is not None:
            appointment.description = description
        if start_datetime is not None:
            appointment.start_datetime = start_datetime
        if end_datetime is not None:
            appointment.end_datetime = end_datetime
        session.commit()

def delete_appointment(id):
    with Session(engine) as session:
        appointment = session.get(Appointment, id)
        session.delete(appointment)
        session.commit()

def create_attendance(user_id, appointment_id, status_attend='invited'):
    # status_attend: 'invited' (default), 'confirmed', 'declined' - set by user response
    with Session(engine) as session:
        new_attendance = Attendance(user_id=user_id, appointment_id=appointment_id, status_attend=status_attend)
        session.add(new_attendance)
        session.commit()

def get_attendance_by_id(id):
    with Session(engine) as session:
        attendance = session.get(Attendance, id)
        return attendance

def get_attendance_by_status(appointment_id, status):
    with Session(engine) as session:
        attendance = session.query(Attendance).filter(Attendance.appointment_id == appointment_id, Attendance.status_attend == status).all()
        return attendance

def update_attendance(id, appointment_id=None, status_attend=None):
    with Session(engine) as session:
        attendance = session.get(Attendance, id)
        if appointment_id is not None:
            attendance.appointment_id = appointment_id
        if status_attend is not None:
            if status_attend == 'confirmed' or status_attend == 'declined':
                attendance.status_attend = status_attend
            else:
                print(f"Invalid status_attend '{status_attend}' - status_attend remains '{attendance.status_attend}'")
        session.commit()

# Attendance records are never deleted - users can only decline via update_attendance


