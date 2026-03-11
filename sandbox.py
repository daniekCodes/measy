"""
Integration tests for all queries.py functions.
Tests are executed in dependency order: User → Location → Appointment → Attendance → Poll → Choice → Vote
Each table is tested with create, read, update and edge cases.
"""

import queries

print('--- User ---')
#queries.create_user('Ina', 'ina@test.de', 'passwort')
user_by_id = queries.get_user_by_id(1)
user_by_mail = queries.get_user_by_email('ina@test.de')
print('user_by_id.name:', user_by_id.name)
print('user_by_mail.role:', user_by_mail.role)
queries.update_user(1, role= 'test')
user_by_id = queries.get_user_by_id(1)
print('user-role after invalid update:', user_by_id.role)
#user_by_id = queries.get_user_by_id(8)
#queries.delete_user(1)

print('--- LOCATION ---')
#queries.create_location('physical', street='Hauptstrasse', house_number='1', postal_code='10115', city='Berlin')
#queries.create_location('virtual', virtual_location='zoom.com')
location = queries.get_location_by_id(1)
print('location.meeting_type:', location.meeting_type)
print('location.city:', location.city)
#queries.update_location(1, city='München')
location = queries.get_location_by_id(1)
print('location.city after update:', location.city)
queries.update_location(1, meeting_type='virtual', virtual_location='zoom.com')

print('--- APPOINTMENT ---')
#queries.create_appointment('Teammeeting', organiser_id=1, location_id=1, description='Erstes Meeting')
appointment = queries.get_appointment_by_id(1)
print('appointment.title:', appointment.title)
queries.update_appointment(1, title='Teammeeting Updated')
appointment = queries.get_appointment_by_id(1)
print('appointment.title after update:', appointment.title)

print('--- ATTENDANCE ---')
#queries.create_attendance(user_id=1, appointment_id=1)
attendance = queries.get_attendance_by_id(1)
print('attendance.status_attend:', attendance.status_attend)
queries.update_attendance(1, status_attend='confirmed')
attendance = queries.get_attendance_by_id(1)
print('attendance.status after update:', attendance.status_attend)
queries.update_attendance(1, status_attend='invalid')
attendance = queries.get_attendance_by_id(1)
print('attendance.status after invalid update:', attendance.status_attend)

print('--- POLL ---')
#queries.create_poll(appointment_id=1, description='Wann treffen wir uns?')
poll = queries.get_poll_by_id(1)
print('poll.description:', poll.description)

print('--- CHOICE ---')
#queries.create_choice(poll_id=1, label='Montag')
#queries.create_choice(poll_id=1, label='Dienstag')
choice = queries.get_choice_by_id(1)
print('choice.label:', choice.label)

print('--- VOTE ---')
#queries.create_vote(user_id=1, choice_id=1, can_attend=True)
vote = queries.get_vote_by_id(1)
print('vote.can_attend:', vote.can_attend)
votes = queries.get_votes_by_choice(choice_id=1, can_attend=True)
print('votes for choice 1 can_attend=True:', len(votes))





