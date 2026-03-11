import queries
from queries import create_appointment, get_appointment_by_id

#create_appointment('Essen beim Griechen', 1, 1, 'Zum leckeren Griechen')
appointment = get_appointment_by_id(1)
print(appointment.title, appointment.description)


