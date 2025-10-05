from dao.appointment_dao import AppointmentDAO
from dao.availability_dao import AvailabilityDAO
from datetime import datetime


class AppointmentError(Exception):
    pass


def parse_time_str(time_str: str):
    """Parse time in HH:MM or HH:MM:SS format into a datetime.time object."""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return datetime.strptime(time_str, "%H:%M:%S").time()


class AppointmentService:
    def __init__(self, appointment_dao: AppointmentDAO, availability_dao: AvailabilityDAO):
        self.appointment_dao = appointment_dao
        self.availability_dao = availability_dao

    def add_appointment(self, patient_id, doctor_id, appointment_date, appointment_time):
        """Add a new appointment with validation and availability check."""
        if not patient_id or not doctor_id or not appointment_date or not appointment_time:
            raise AppointmentError("All fields (patient_id, doctor_id, appointment_date, appointment_time) are required.")
        
        print(f"Service received appointment_time: {appointment_time}")
        try:
            # Validate date
            appt_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            # Normalize time
            appt_time = parse_time_str(appointment_time)
            print(f"Service normalized appointment_time: {appt_time.strftime('%H:%M')}")
        except ValueError as e:
            raise AppointmentError(f"Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time. Error: {e}")
        
        appointment_dt = datetime.combine(appt_date, appt_time)

        # Check availability in AvailabilityOfDoctors1
        availability = self.availability_dao.list_availability(doctor_id)
        is_available_slot = False
        for slot in availability:
            print(f"Slot available_date: {slot['available_date']}, start_time: {slot['start_time']}, end_time: {slot['end_time']}, is_available: {slot['is_available']}")
            slot_date = datetime.strptime(slot['available_date'], "%Y-%m-%d").date()
            slot_start = parse_time_str(slot['start_time'])
            slot_end = parse_time_str(slot['end_time'])
            slot_start_dt = datetime.combine(slot_date, slot_start)
            slot_end_dt = datetime.combine(slot_date, slot_end)

            if (
                slot['doctor_id'] == doctor_id and
                slot['is_available'] and
                appointment_dt >= slot_start_dt and
                appointment_dt < slot_end_dt
            ):
                is_available_slot = True
                break

        if not is_available_slot:
            raise AppointmentError(f"No available slot for doctor_id {doctor_id} at {appointment_date} {appointment_time}.")
        
        # Pass time in HH:MM format
        return self.appointment_dao.add_appointment(patient_id, doctor_id, appointment_date, appt_time.strftime("%H:%M"))

    def delete_appointment(self, appointment_id):
        """Delete an appointment and update availability to True."""
        if not appointment_id:
            raise AppointmentError("Appointment ID is required.")
        
        response = self.appointment_dao.list_appointments()
        appointment = next((a for a in response if a['appointment_id'] == appointment_id), None)
        if not appointment:
            raise AppointmentError(f"Appointment ID {appointment_id} not found.")
        
        appointment_dt = datetime.strptime(
            f"{appointment['appointment_date']} {appointment['appointment_time']}", "%Y-%m-%d %H:%M"
        )

        availability = self.availability_dao.list_availability(appointment['doctor_id'])
        for slot in availability:
            slot_date = datetime.strptime(slot['available_date'], "%Y-%m-%d").date()
            slot_start = parse_time_str(slot['start_time'])
            slot_end = parse_time_str(slot['end_time'])
            slot_start_dt = datetime.combine(slot_date, slot_start)
            slot_end_dt = datetime.combine(slot_date, slot_end)

            if (
                slot['doctor_id'] == appointment['doctor_id'] and
                appointment_dt >= slot_start_dt and
                appointment_dt < slot_end_dt
            ):
                self.availability_dao.update_availability(slot['availability_id'], is_available=True)
                break
        
        self.appointment_dao.delete_appointment(appointment_id)

    def list_appointments(self):
        """List all appointments."""
        return self.appointment_dao.list_appointments()

    def update_appointment(self, appointment_id, status=None):
        """Update an appointment's status with validation."""
        if not appointment_id:
            raise AppointmentError("Appointment ID is required.")
        if status and status not in ["Scheduled", "Completed", "Cancelled"]:
            raise AppointmentError("Status must be 'Scheduled', 'Completed', or 'Cancelled'.")
        return self.appointment_dao.update_appointment(appointment_id, status)