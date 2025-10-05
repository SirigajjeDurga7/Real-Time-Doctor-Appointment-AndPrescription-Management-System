from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class AppointmentDAO:
    def add_appointment(self, patient_id, doctor_id, appointment_date, appointment_time):
        """Add a new appointment to the database."""
        data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time,
            "status": "Scheduled"
        }
        response = supabase.table("appointments1").insert(data).execute()
        return response.data[0] if response.data else None

    def delete_appointment(self, appointment_id):
        """Delete an appointment from the database."""
        supabase.table("appointments1").delete().eq("appointment_id", appointment_id).execute()

    def list_appointments(self):
        """Retrieve all appointments from the database."""
        response = supabase.table("appointments1").select("*").execute()
        return response.data

    def update_appointment(self, appointment_id, status=None):
        """Update an appointment's status."""
        updates = {}
        if status is not None:
            updates["status"] = status
        response = supabase.table("appointments1").update(updates).eq("appointment_id", appointment_id).execute()
        return response.data[0] if response.data else None