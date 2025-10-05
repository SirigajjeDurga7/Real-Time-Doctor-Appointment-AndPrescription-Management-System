from dao.doctor_dao import DoctorDAO

class DoctorError(Exception):
    pass

class DoctorService:
    def __init__(self, doctor_dao):
        self.doctor_dao = doctor_dao

    def add_doctor(self, full_name, specialization, email, phone, experience_years):
        """Add a new doctor with validation."""
        if not full_name or not email:
            raise DoctorError("Full name and email are required.")
        if not isinstance(experience_years, int) or experience_years < 0:
            raise DoctorError("Experience years must be a positive integer.")
        return self.doctor_dao.add_doctor(full_name, specialization, email, phone, experience_years)

    def delete_doctor(self, doctor_id):
        """Delete a doctor with validation."""
        if not doctor_id:
            raise DoctorError("Doctor ID is required.")
        self.doctor_dao.delete_doctor(doctor_id)

    def list_doctors(self, limit=100):
        """List all doctors."""
        return self.doctor_dao.list_doctors()

    def update_doctor(self, doctor_id, phone=None, specialization=None):
        """Update a doctor's phone or specialization with validation."""
        if not doctor_id:
            raise DoctorError("Doctor ID is required.")
        if not (phone or specialization):
            raise DoctorError("At least one field (phone or specialization) must be provided.")
        return self.doctor_dao.update_doctor(doctor_id, phone, specialization)