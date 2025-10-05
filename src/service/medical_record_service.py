from dao.medical_record_dao import MedicalRecordDAO
from datetime import datetime

class MedicalRecordError(Exception):
    pass

class MedicalRecordService:
    def __init__(self, medical_record_dao: MedicalRecordDAO):
        self.medical_record_dao = medical_record_dao

    def add_medical_record(self, patient_id, doctor_id, appointment_id, diagnosis, prescription):
        """Add a new medical record with validation."""
        if not all([patient_id, doctor_id, appointment_id, diagnosis, prescription]):
            raise MedicalRecordError("All fields (patient_id, doctor_id, appointment_id, diagnosis, prescription) are required.")
        return self.medical_record_dao.add_medical_record(patient_id, doctor_id, appointment_id, diagnosis, prescription)

    def delete_medical_record(self, record_id):
        """Delete a medical record."""
        if not record_id:
            raise MedicalRecordError("Record ID is required.")
        self.medical_record_dao.delete_medical_record(record_id)

    def list_medical_records(self):
        """List all medical records."""
        return self.medical_record_dao.list_medical_records()

    def update_medical_record(self, record_id, diagnosis=None, prescription=None):
        """Update a medical record's diagnosis or prescription with validation."""
        if not record_id:
            raise MedicalRecordError("Record ID is required.")
        if not any([diagnosis, prescription]):
            raise MedicalRecordError("At least one field (diagnosis or prescription) must be provided to update.")
        return self.medical_record_dao.update_medical_record(record_id, diagnosis, prescription)