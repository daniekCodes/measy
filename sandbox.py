import queries
from queries import update_location

location = queries.get_location_by_id(1)
print('Id:', location.id, 'Type:', location.meeting_type, 'location:', location.virtual_location)

update_location(1, meeting_type='physical', longitude=1234569877)
location = queries.get_location_by_id(1)
print('Id:', location.id, 'Type:', location.meeting_type, 'location:', location.virtual_location, location.longitude)

update_location(1, meeting_type='virtual')
location = queries.get_location_by_id(1)
print('Id:', location.id, 'Type:', location.meeting_type, 'location:', location.virtual_location, location.longitude)

update_location(1, meeting_type='physical', virtual_location='test')
location = queries.get_location_by_id(1)
print('Id:', location.id, 'Type:', location.meeting_type, 'location:', location.virtual_location, location.longitude)
