from dao.patient_dao import PatientDAO

class PatientError(Exception):
    pass

class PatientService:
    def __init__(self, patient_dao):
        self.patient_dao = patient_dao

    def add_patient(self, full_name, email, phone, age, gender, address):
        """Add a new patient with validation."""
        if not full_name or not email:
            raise PatientError("Full name and email are required.")
        if not isinstance(age, int) or age < 0:
            raise PatientError("Age must be a positive integer.")
        return self.patient_dao.add_patient(full_name, email, phone, age, gender, address)

    def delete_patient(self, patient_id):
        """Delete a patient with validation."""
        if not patient_id:
            raise PatientError("Patient ID is required.")
        self.patient_dao.delete_patient(patient_id)

    def list_patients(self, limit=100):
        """List all patients."""
        return self.patient_dao.list_patients()

    def update_patient(self, patient_id, phone=None, address=None):
        """Update a patient's phone or address with validation."""
        if not patient_id:
            raise PatientError("Patient ID is required.")
        if not (phone or address):
            raise PatientError("At least one field (phone or address) must be provided.")
        return self.patient_dao.update_patient(patient_id, phone, address)