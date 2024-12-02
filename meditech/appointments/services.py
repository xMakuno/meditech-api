from meditech.appointments.models import Appointment

def get_appointments():
    return Appointment.query.all()