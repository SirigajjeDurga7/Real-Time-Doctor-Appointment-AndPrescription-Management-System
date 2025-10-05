from dao.availability_dao import AvailabilityDAO

class AvailabilityError(Exception):
    pass

class AvailabilityService:
    def __init__(self, availability_dao):
        self.availability_dao = availability_dao

    def add_availability(self, doctor_id, available_date, start_time, end_time):
        """Add a new availability slot with validation."""
        if not doctor_id or not available_date or not start_time or not end_time:
            raise AvailabilityError("All fields (doctor_id, available_date, start_time, end_time) are required.")
        if start_time >= end_time:
            raise AvailabilityError("Start time must be before end time.")
        return self.availability_dao.add_availability(doctor_id, available_date, start_time, end_time)

    def delete_availability(self, availability_id):
        """Delete an availability slot with validation."""
        if not availability_id:
            raise AvailabilityError("Availability ID is required.")
        self.availability_dao.delete_availability(availability_id)

    def list_availability(self, doctor_id=None):
        """List all availability slots or those for a specific doctor."""
        return self.availability_dao.list_availability(doctor_id)
    
    def update_availability(self, availability_id, is_available=None, start_time=None, end_time=None, available_date=None):
        if not availability_id:
            raise AvailabilityError("Availability ID is required.")
        if start_time and end_time and start_time >= end_time:
            raise AvailabilityError("Start time must be before end_time.")
        if available_date:
            from datetime import datetime
            try:
                datetime.strptime(available_date, "%Y-%m-%d")
            except ValueError:
                raise AvailabilityError("Invalid date format. Use YYYY-MM-DD.")   
        return self.availability_dao.update_availability(
        availability_id, is_available, start_time, end_time, available_date
    )
