from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class DoctorDAO:
    def add_doctor(self, full_name, specialization, email, phone, experience_years):
        """Add a new doctor to the database."""
        data = {
            "full_name": full_name,
            "specialization": specialization,
            "email": email,
            "phone": phone,
            "experience_years": experience_years
        }
        response = supabase.table("doctors1").insert(data).execute()
        return response.data[0] if response.data else None

    def delete_doctor(self, doctor_id):
        """Delete a doctor from the database."""
        supabase.table("doctors1").delete().eq("doctor_id", doctor_id).execute()

    def list_doctors(self):
        """Retrieve all doctors from the database."""
        response = supabase.table("doctors1").select("*").execute()
        return response.data

    def update_doctor(self, doctor_id, phone=None, specialization=None):
        """Update a doctor's phone or specialization in the database."""
        updates = {}
        if phone is not None:
            updates["phone"] = phone
        if specialization is not None:
            updates["specialization"] = specialization
        response = supabase.table("doctors1").update(updates).eq("doctor_id", doctor_id).execute()
        return response.data[0] if response.data else None