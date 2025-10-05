from dao.payment_dao import PaymentDAO
from datetime import datetime

class PaymentError(Exception):
    pass

class PaymentService:
    def __init__(self, payment_dao: PaymentDAO):
        self.payment_dao = payment_dao

    def add_payment(self, appointment_id, patient_id, amount, transaction_id=None):
        """Add a new payment with validation."""
        if not all([appointment_id, patient_id, amount]):
            raise PaymentError("appointment_id, patient_id, and amount are required.")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise PaymentError("Amount must be a positive number.")
        return self.payment_dao.add_payment(appointment_id, patient_id, amount, transaction_id)

    def delete_payment(self, payment_id):
        """Delete a payment."""
        if not payment_id:
            raise PaymentError("Payment ID is required.")
        self.payment_dao.delete_payment(payment_id)

    def list_payments(self):
        """List all payments."""
        return self.payment_dao.list_payments()

    def update_payment(self, payment_id, payment_status=None):
        """Update a payment's status with validation."""
        if not payment_id:
            raise PaymentError("Payment ID is required.")
        if payment_status and payment_status not in ["Pending", "Completed", "Failed"]:
            raise PaymentError("Status must be 'Pending', 'Completed', or 'Failed'.")
        return self.payment_dao.update_payment(payment_id, payment_status)