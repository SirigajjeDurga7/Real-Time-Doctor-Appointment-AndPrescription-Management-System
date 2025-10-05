from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class AvailabilityDAO:
    def add_availability(self, doctor_id, available_date, start_time, end_time):
        """Add a new availability slot for a doctor."""
        data = {
            "doctor_id": doctor_id,
            "available_date": available_date,
            "start_time": start_time,
            "end_time": end_time,
            "is_available": True
        }
        response = supabase.table("availabilityofdoctors1").insert(data).execute()
        return response.data[0] if response.data else None

    def delete_availability(self, availability_id):
        """Delete an availability slot."""
        supabase.table("availabilityofdoctors1").delete().eq("availability_id", availability_id).execute()

    def list_availability(self, doctor_id=None):
        """Retrieve all availability slots or those for a specific doctor."""
        query = supabase.table("availabilityofdoctors1").select("*")
        if doctor_id:
            query = query.eq("doctor_id", doctor_id)
        response = query.execute()
        return response.data

    def update_availability(self, availability_id, is_available=None, start_time=None, end_time=None, appointment_date=None):
        updates = {}
        if is_available is not None:
            updates["is_available"] = is_available
        if start_time is not None:
            updates["start_time"] = start_time
        if end_time is not None:
            updates["end_time"] = end_time
        if appointment_date is not None:
            updates["appointment_date"] = appointment_date  # Add this line
        response = supabase.table("availabilityofdoctors1").update(updates).eq("availability_id", availability_id).execute()
        return response.data[0] if response.data else None
