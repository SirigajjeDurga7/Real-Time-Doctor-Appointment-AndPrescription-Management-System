from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class PaymentDAO:
    def add_payment(self, appointment_id, patient_id, amount, transaction_id=None):
        """Add a new payment to the database."""
        data = {
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "amount": float(amount),  # Ensure amount is a float
            "transaction_id": transaction_id,
            "payment_status": "Pending"
        }
        response = supabase.table("payments1").insert(data).execute()
        return response.data[0] if response.data else None

    def delete_payment(self, payment_id):
        """Delete a payment from the database."""
        supabase.table("payments1").delete().eq("payment_id", payment_id).execute()

    def list_payments(self):
        """Retrieve all payments from the database."""
        response = supabase.table("payments1").select("*").execute()
        return response.data

    def update_payment(self, payment_id, payment_status=None):
        """Update a payment's status."""
        updates = {}
        if payment_status and payment_status in ["Pending", "Completed", "Failed"]:
            updates["payment_status"] = payment_status
        response = supabase.table("payments1").update(updates).eq("payment_id", payment_id).execute()
        return response.data[0] if response.data else None