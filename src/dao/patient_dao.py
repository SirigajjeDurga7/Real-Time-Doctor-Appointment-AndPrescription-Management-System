from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class PatientDAO:
    def add_patient(self, full_name, email, phone, age, gender, address):
        """Add a new patient to the database."""
        data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "age": age,
            "gender": gender,
            "address": address
        }
        response = supabase.table("patients1").insert(data).execute()
        return response.data[0] if response.data else None

    def delete_patient(self, patient_id):
        """Delete a patient from the database."""
        supabase.table("patients1").delete().eq("patient_id", patient_id).execute()

    def list_patients(self):
        """Retrieve all patients from the database."""
        response = supabase.table("patients1").select("*").execute()
        return response.data

    def update_patient(self, patient_id, phone=None, address=None):
        """Update a patient's phone or address in the database."""
        updates = {}
        if phone is not None:
            updates["phone"] = phone
        if address is not None:
            updates["address"] = address
        response = supabase.table("patients1").update(updates).eq("patient_id", patient_id).execute()
        return response.data[0] if response.data else None