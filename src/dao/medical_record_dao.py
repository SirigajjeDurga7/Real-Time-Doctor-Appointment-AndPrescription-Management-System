from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class MedicalRecordDAO:
    def add_medical_record(self, patient_id, doctor_id, appointment_id, diagnosis, prescription):
        """Add a new medical record to the database."""
        data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_id": appointment_id,
            "diagnosis": diagnosis,
            "prescription": prescription
        }
        response = supabase.table("medical_records1").insert(data).execute()
        return response.data[0] if response.data else None

    def delete_medical_record(self, record_id):
        """Delete a medical record from the database."""
        supabase.table("medical_records1").delete().eq("record_id", record_id).execute()

    def list_medical_records(self):
        """Retrieve all medical records from the database."""
        response = supabase.table("medical_records1").select("*").execute()
        return response.data

    def update_medical_record(self, record_id, diagnosis=None, prescription=None):
        """Update a medical record's diagnosis or prescription."""
        updates = {}
        if diagnosis is not None:
            updates["diagnosis"] = diagnosis
        if prescription is not None:
            updates["prescription"] = prescription
        if not updates:
            return None
        response = supabase.table("medical_records1").update(updates).eq("record_id", record_id).execute()
        return response.data[0] if response.data else None