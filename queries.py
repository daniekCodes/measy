"""
CRUD operations for all database tables.
Validation for constrained fields (role, meeting_type, status_attend) is handled in Python before DB commit.
"""

from sqlalchemy.orm import Session
from database import engine
from models import User, Appointment, Attendance, Poll, Choice, Vote, Location
from sqlalchemy import select


def create_user(name, email, password, role='user'):
    # role: 'user' (default) or 'admin'
    with Session(engine) as session:
        new_user = User(name=name, email=email, password=password, role=role)
        session.add(new_user)
        session.commit()

def get_all_users():
    with Session(engine) as session:
        return session.query(User).all()

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

def create_location(meeting_type, latitude=None, longitude=None, street=None,
                    house_number=None, postal_code=None, city=None, virtual_location=None):
    # meeting_type: 'physical' (requires physical address/coordinates) or 'virtual' (requires virtual_location)
    # fields for the other type must be None - validated before insert
    with Session(engine) as session:
        if meeting_type == 'physical' and virtual_location is not None:
            raise ValueError("physical location does not allow virtual_location")
        if meeting_type == 'virtual' and (latitude is not None or longitude is not None
                                          or street is not None or house_number is not None
                                          or postal_code is not None or city is not None):
            raise ValueError("virtual location does not allow physical address/coordinates")
        new_location = Location(meeting_type=meeting_type, latitude=latitude, longitude=longitude,
                                street=street, house_number=house_number, postal_code=postal_code,
                                city=city, virtual_location=virtual_location)
        session.add(new_location)
        session.commit()

def get_location_by_id(id):
    with Session(engine) as session:
        location = session.get(Location, id)
        return location

def update_location(id, meeting_type=None, latitude=None, longitude=None, street=None,
                    house_number=None, postal_code=None, city=None, virtual_location=None):
    # use new meeting_type if provided, otherwise keep existing one from DB
    with Session(engine) as session:
        location = session.get(Location, id)

        # determine final meeting_type & validate
        effective_type = meeting_type if meeting_type is not None else location.meeting_type
        if effective_type == 'physical' and virtual_location is not None:
            raise ValueError("physical location does not allow virtual_location")
        if effective_type == 'virtual' and (latitude is not None or longitude is not None
                                            or street is not None or house_number is not None
                                            or postal_code is not None or city is not None):
            raise ValueError("virtual location does not allow physical address/coordinates")
        if meeting_type is not None:
            location.meeting_type = meeting_type
            if meeting_type == 'virtual':
                print("physical address/coordinates removed - virtual_location can now be set")
                location.latitude = None
                location.longitude = None
                location.street = None
                location.house_number = None
                location.postal_code = None
                location.city = None
            if meeting_type == 'physical':
                print("virtual_location removed - physical address/coordinates can now be set")
                location.virtual_location = None
        if latitude is not None:
            location.latitude = latitude
        if longitude is not None:
            location.longitude = longitude
        if street is not None:
            location.street = street
        if house_number is not None:
            location.house_number = house_number
        if postal_code is not None:
            location.postal_code = postal_code
        if city is not None:
            location.city = city
        if virtual_location is not None:
            location.virtual_location = virtual_location
        session.commit()

def delete_location(id):
    with Session(engine) as session:
        location = session.get(Location, id)
        session.delete(location)
        session.commit()

def create_appointment(title, organiser_id, location_id, description=None, start_datetime=None, end_datetime=None):
    with Session(engine) as session:
        new_appointment = Appointment(title=title, user_id=organiser_id, location_id=location_id, description=description, start_datetime=start_datetime, end_datetime=end_datetime)
        session.add(new_appointment)
        session.commit()

def get_all_appointments():
    with Session(engine) as session:
        return session.query(Appointment).all()

def get_appointment_by_id(id):
    with Session(engine) as session:
        appointment = session.get(Appointment, id)
        return appointment

def update_appointment(id, title=None, organiser_id=None, location_id=None, description=None, start_datetime=None, end_datetime=None):
    with Session(engine) as session:
        appointment = session.get(Appointment, id)
        if title is not None:
            appointment.title = title
        if organiser_id is not None:
            appointment.user_id = organiser_id
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

def get_attendances_by_user_id(user_id):
    with Session(engine) as session:
        attendances = session.query(Attendance).filter(Attendance.user_id == user_id).all()
        return attendances

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

def create_poll(appointment_id, description):
    # A poll belongs to one appointment and contains multiple choices
    with Session(engine) as session:
        new_poll = Poll(appointment_id=appointment_id, description=description)
        session.add(new_poll)
        session.commit()

def get_poll_by_id(id):
    with Session(engine) as session:
        poll = session.get(Poll, id)
        return poll

def update_poll(id, appointment_id=None, description=None):
    with Session(engine) as session:
        poll = session.get(Poll, id)
        if appointment_id is not None:
            poll.appointment_id = appointment_id
        if description is not None:
            poll.description = description
        session.commit()

def delete_poll(id):
    with Session(engine) as session:
        poll = session.get(Poll, id)
        session.delete(poll)
        session.commit()

def create_choice(poll_id, label):
    # label: the text of the answer option (e.g. 'Monday', 'Yes', 'No')
    with Session(engine) as session:
        new_choice = Choice(poll_id=poll_id, label=label)
        session.add(new_choice)
        session.commit()

def get_choice_by_id(id):
    with Session(engine) as session:
        choice = session.get(Choice, id)
        return choice

def update_choice(id, poll_id=None, label=None):
    with Session(engine) as session:
        choice = session.get(Choice, id)
        if poll_id is not None:
            choice.poll_id = poll_id
        if label is not None:
            choice.label = label
        session.commit()

def delete_choice(id):
    with Session(engine) as session:
        choice = session.get(Choice, id)
        session.delete(choice)
        session.commit()

def get_choices_by_poll_id(poll_id):
    with Session(engine) as session:
        choices = session.execute(select(Choice).where(Choice.poll_id==poll_id))
        return choices.scalars().all()


def create_vote(user_id, choice_id, can_attend=False):
    # can_attend: True = user can attend at this choice's time, False = cannot
    with Session(engine) as session:
        new_vote = Vote(user_id=user_id, choice_id=choice_id, can_attend=can_attend)
        session.add(new_vote)
        session.commit()

def get_vote_by_id(id):
    with Session(engine) as session:
        vote = session.get(Vote, id)
        return vote

def get_votes_by_choice(choice_id, can_attend=None):
    # returns all votes for a choice, optionally filtered by can_attend
    with Session(engine) as session:
        query = session.query(Vote).filter(Vote.choice_id == choice_id)
        if can_attend is not None:
            query = query.filter(Vote.can_attend == can_attend)
        return query.all()

def update_vote(id, choice_id=None, can_attend=None):
    with Session(engine) as session:
        vote = session.get(Vote, id)
        if choice_id is not None:
            vote.choice_id = choice_id
        if can_attend is not None:
            vote.can_attend = can_attend
        session.commit()

def delete_vote(id):
    with Session(engine) as session:
        vote = session.get(Vote, id)
        session.delete(vote)
        session.commit()