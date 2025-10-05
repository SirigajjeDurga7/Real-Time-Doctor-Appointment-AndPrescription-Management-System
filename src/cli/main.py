import json
import sys
import os
from datetime import datetime
import time  # Added for real-time-like delay

# Adjust the path to go up to src and then access dao and service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dao.patient_dao import PatientDAO
from dao.doctor_dao import DoctorDAO
from dao.availability_dao import AvailabilityDAO
from dao.appointment_dao import AppointmentDAO
from dao.payment_dao import PaymentDAO
from dao.medical_record_dao import MedicalRecordDAO
from service.patient_service import PatientService, PatientError
from service.doctor_service import DoctorService, DoctorError
from service.availability_service import AvailabilityService, AvailabilityError
from service.appointment_service import AppointmentService, AppointmentError
from service.payment_service import PaymentService, PaymentError
from service.medical_record_service import MedicalRecordService, MedicalRecordError

class PatientCLI:
    def __init__(self):
        self.patient_service = PatientService(PatientDAO())
        self.doctor_service = DoctorService(DoctorDAO())
        self.availability_service = AvailabilityService(AvailabilityDAO())
        self.appointment_service = AppointmentService(AppointmentDAO(), AvailabilityDAO())
        self.payment_service = PaymentService(PaymentDAO())
        self.medical_record_service = MedicalRecordService(MedicalRecordDAO())

    # -------- Patient operations --------
    def add_patient(self):
        try:
            full_name = input("Full Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            age = int(input("Age: "))
            gender = input("Gender: ")
            address = input("Address: ")
            patient = self.patient_service.add_patient(
                full_name=full_name,
                email=email,
                phone=phone,
                age=age,
                gender=gender,
                address=address
            )
            print("Patient added successfully:")
            print(json.dumps(patient, indent=2, default=str))
        except PatientError as e:
            print(f"Patient error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def list_patients(self):
        patients = self.patient_service.list_patients(limit=100)
        print(json.dumps(patients, indent=2, default=str))

    def update_patient(self):
        try:
            patient_id = int(input("Patient ID to update: "))
            phone = input("New Phone (leave blank to skip): ")
            address = input("New Address (leave blank to skip): ")
            if not phone and not address:
                print("Error: You must provide at least one field to update")
                return
            updated = self.patient_service.update_patient(
                patient_id=patient_id,
                phone=phone or None,
                address=address or None
            )
            print("Patient updated successfully:")
            print(json.dumps(updated, indent=2, default=str))
        except PatientError as e:
            print(f"Patient error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_patient(self):
        try:
            patient_id = int(input("Patient ID to delete: "))
            deleted = self.patient_service.delete_patient(patient_id)
            print("Patient deleted successfully:")
            print(json.dumps(deleted, indent=2, default=str))
        except PatientError as e:
            print(f"Patient error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # -------- Doctor operations --------
    def add_doctor(self):
        try:
            full_name = input("Full Name: ")
            specialization = input("Specialization: ")
            email = input("Email: ")
            phone = input("Phone: ")
            experience_years = int(input("Experience Years: "))
            doctor = self.doctor_service.add_doctor(
                full_name=full_name,
                specialization=specialization,
                email=email,
                phone=phone,
                experience_years=experience_years
            )
            print("Doctor added successfully:")
            print(json.dumps(doctor, indent=2, default=str))
        except DoctorError as e:
            print(f"Doctor error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def list_doctors(self):
        doctors = self.doctor_service.list_doctors(limit=100)
        print(json.dumps(doctors, indent=2, default=str))

    def update_doctor(self):
        try:
            doctor_id = int(input("Doctor ID to update: "))
            phone = input("New Phone (leave blank to skip): ")
            specialization = input("New Specialization (leave blank to skip): ")
            if not phone and not specialization:
                print("Error: You must provide at least one field to update")
                return
            updated = self.doctor_service.update_doctor(
                doctor_id=doctor_id,
                phone=phone or None,
                specialization=specialization or None
            )
            print("Doctor updated successfully:")
            print(json.dumps(updated, indent=2, default=str))
        except DoctorError as e:
            print(f"Doctor error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_doctor(self):
        try:
            doctor_id = int(input("Doctor ID to delete: "))
            deleted = self.doctor_service.delete_doctor(doctor_id)
            print("Doctor deleted successfully:")
            print(json.dumps(deleted, indent=2, default=str))
        except DoctorError as e:
            print(f"Doctor error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # -------- Availability operations --------
    def add_availability(self):
        try:
            doctor_id = int(input("Doctor ID: "))
            available_date = input("Available Date (YYYY-MM-DD): ")
            start_time = input("Start Time (HH:MM): ")
            end_time = input("End Time (HH:MM): ")
            datetime.strptime(available_date, "%Y-%m-%d")  # Validate date format
            datetime.strptime(start_time, "%H:%M")  # Validate time format
            datetime.strptime(end_time, "%H:%M")  # Validate time format
            availability = self.availability_service.add_availability(
                doctor_id=doctor_id,
                available_date=available_date,
                start_time=start_time,
                end_time=end_time
            )
            print("Availability added successfully:")
            print(json.dumps(availability, indent=2, default=str))
        except AvailabilityError as e:
            print(f"Availability error: {e}")
        except ValueError as e:
            print(f"Invalid date/time format error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def list_availability(self):
        try:
            doctor_id = input("Doctor ID (leave blank for all): ")
            doctor_id = int(doctor_id) if doctor_id else None
            availabilities = self.availability_service.list_availability(doctor_id)
            print(json.dumps(availabilities, indent=2, default=str))
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def update_availability(self):
        try:
            availability_id = int(input("Availability ID to update: "))
            is_available = input("Is Available (True/False, leave blank to skip): ")
            is_available = {"true": True, "false": False}.get(is_available.lower(), None) if is_available else None
            start_time = input("New Start Time (HH:MM, leave blank to skip): ")
            end_time = input("New End Time (HH:MM, leave blank to skip): ")
            if start_time:
                datetime.strptime(start_time, "%H:%M")
            if end_time:
                datetime.strptime(end_time, "%H:%M")
            updated = self.availability_service.update_availability(
                availability_id=availability_id,
                is_available=is_available,
                start_time=start_time or None,
                end_time=end_time or None
            )
            print("Availability updated successfully:")
            print(json.dumps(updated, indent=2, default=str))
        except AvailabilityError as e:
            print(f"Availability error: {e}")
        except ValueError as e:
            print(f"Invalid date/time format error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_availability(self):
        try:
            availability_id = int(input("Availability ID to delete: "))
            self.availability_service.delete_availability(availability_id)
            print("Availability deleted successfully.")
        except AvailabilityError as e:
            print(f"Availability error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # -------- Appointment operations --------
    def add_appointment(self):
        try:
            patient_id = int(input("Patient ID: "))
            doctor_id = int(input("Doctor ID: "))
            appointment_date = input("Appointment Date (YYYY-MM-DD): ")
            appointment_time = input("Appointment Time (HH:MM): ")
            # Debug: Print raw input
            print(f"Raw appointment_time: {appointment_time}")
            # Ensure strict HH:MM format and handle potential extra data
            try:
                datetime.strptime(appointment_date, "%Y-%m-%d")
                # Parse time and strip any seconds if present
                time_obj = datetime.strptime(appointment_time, "%H:%M")
                appointment_time = time_obj.strftime("%H:%M")  # Normalize to HH:MM
                # Debug: Print normalized time
                print(f"Normalized appointment_time: {appointment_time}")
            except ValueError as e:
                raise ValueError(f"Invalid date/time format. Use YYYY-MM-DD for date and HH:MM for time. Error: {e}")
            # Explicitly pass the normalized value
            appointment = self.appointment_service.add_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time  # Ensure this is the normalized string
            )
            print("Appointment added successfully:")
            print(json.dumps(appointment, indent=2, default=str))
        except AppointmentError as e:
            print(f"Appointment error: {e}")
        except ValueError as e:
            print(f"Invalid date/time format error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def list_appointments(self):
        while True:
            appointments = self.appointment_service.list_appointments()
            print("\n--- Current Appointments (Refreshing every 5 seconds) ---")
            print(json.dumps(appointments, indent=2, default=str))
            time.sleep(5)  # Refresh every 5 seconds
            print("\nPress 'q' to quit viewing, or any other key to continue...")
            if input().lower() == 'q':
                break
    def update_appointment(self):
        try:
            appointment_id = int(input("Appointment ID to update: "))
            status = input("New Status (Scheduled/Completed/Cancelled, leave blank to skip): ")
            status = status if status in ["Scheduled", "Completed", "Cancelled"] else None
            date_input = input("New Appointment Date (YYYY-MM-DD, leave blank to skip): ")
            appointment_date = date_input if date_input else None
            updated = self.appointment_service.update_appointment(
            appointment_id=appointment_id,
            status=status,
            appointment_date=appointment_date  # pass the new date
            )
            print("Appointment updated successfully:")
            print(json.dumps(updated, indent=2, default=str))
        except AppointmentError as e:
            print(f"Appointment error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")



    def delete_appointment(self):
        try:
            appointment_id = int(input("Appointment ID to delete: "))
            self.appointment_service.delete_appointment(appointment_id)
            print("Appointment deleted successfully.")
        except AppointmentError as e:
            print(f"Appointment error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # -------- Payment operations --------
    def add_payment(self):
        try:
            appointment_id = int(input("Appointment ID: "))
            patient_id = int(input("Patient ID: "))
            amount = float(input("Amount: "))
            transaction_id = input("Transaction ID (leave blank to skip): ") or None
            payment = self.payment_service.add_payment(
                appointment_id=appointment_id,
                patient_id=patient_id,
                amount=amount,
                transaction_id=transaction_id
            )
            print("Payment added successfully:")
            print(json.dumps(payment, indent=2, default=str))
        except PaymentError as e:
            print(f"Payment error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def list_payments(self):
        payments = self.payment_service.list_payments()
        print(json.dumps(payments, indent=2, default=str))

    def update_payment(self):
        try:
            payment_id = int(input("Payment ID to update: "))
            payment_status = input("New Status (Pending/Completed/Failed, leave blank to skip): ")
            payment_status = payment_status if payment_status in ["Pending", "Completed", "Failed"] else None
            updated = self.payment_service.update_payment(
                payment_id=payment_id,
                payment_status=payment_status
            )
            print("Payment updated successfully:")
            print(json.dumps(updated, indent=2, default=str))
        except PaymentError as e:
            print(f"Payment error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_payment(self):
        try:
            payment_id = int(input("Payment ID to delete: "))
            self.payment_service.delete_payment(payment_id)
            print("Payment deleted successfully.")
        except PaymentError as e:
            print(f"Payment error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # -------- Medical Record operations --------
    def add_medical_record(self):
        try:
            patient_id = int(input("Patient ID: "))
            doctor_id = int(input("Doctor ID: "))
            appointment_id = int(input("Appointment ID: "))
            diagnosis = input("Diagnosis: ")
            prescription = input("Prescription: ")
            medical_record = self.medical_record_service.add_medical_record(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_id=appointment_id,
                diagnosis=diagnosis,
                prescription=prescription
            )
            print("Medical record added successfully:")
            print(json.dumps(medical_record, indent=2, default=str))
        except MedicalRecordError as e:
            print(f"Medical record error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def list_medical_records(self):
        medical_records = self.medical_record_service.list_medical_records()
        print(json.dumps(medical_records, indent=2, default=str))

    def update_medical_record(self):
        try:
            record_id = int(input("Record ID to update: "))
            diagnosis = input("New Diagnosis (leave blank to skip): ") or None
            prescription = input("New Prescription (leave blank to skip): ") or None
            if not diagnosis and not prescription:
                print("Error: You must provide at least one field to update")
                return
            updated = self.medical_record_service.update_medical_record(
                record_id=record_id,
                diagnosis=diagnosis,
                prescription=prescription
            )
            print("Medical record updated successfully:")
            print(json.dumps(updated, indent=2, default=str))
        except MedicalRecordError as e:
            print(f"Medical record error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_medical_record(self):
        try:
            record_id = int(input("Record ID to delete: "))
            self.medical_record_service.delete_medical_record(record_id)
            print("Medical record deleted successfully.")
        except MedicalRecordError as e:
            print(f"Medical record error: {e}")
        except ValueError as e:
            print(f"Invalid input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # -------- Menu runner --------
    def run(self):
        while True:
            print("\n--- Main Management Menu ---")
            print("1. Patient Operations")
            print("2. Doctor Operations")
            print("3. Availability Operations")
            print("4. Appointment Operations")
            print("5. Payment Operations")
            print("6. Medical Record Operations")
            print("7. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                while True:
                    print("\n--- Patient Operations Menu ---")
                    print("1. Add Patient")
                    print("2. List Patients")
                    print("3. Update Patient")
                    print("4. Delete Patient")
                    print("5. Back to Main Menu")
                    sub_choice = input("Select an option: ")
                    if sub_choice == "1":
                        self.add_patient()
                    elif sub_choice == "2":
                        self.list_patients()
                    elif sub_choice == "3":
                        self.update_patient()
                    elif sub_choice == "4":
                        self.delete_patient()
                    elif sub_choice == "5":
                        break
                    else:
                        print("Invalid option. Please try again.")
            elif choice == "2":
                while True:
                    print("\n--- Doctor Operations Menu ---")
                    print("1. Add Doctor")
                    print("2. List Doctors")
                    print("3. Update Doctor")
                    print("4. Delete Doctor")
                    print("5. Back to Main Menu")
                    sub_choice = input("Select an option: ")
                    if sub_choice == "1":
                        self.add_doctor()
                    elif sub_choice == "2":
                        self.list_doctors()
                    elif sub_choice == "3":
                        self.update_doctor()
                    elif sub_choice == "4":
                        self.delete_doctor()
                    elif sub_choice == "5":
                        break
                    else:
                        print("Invalid option. Please try again.")
            elif choice == "3":
                while True:
                    print("\n--- Availability Operations Menu ---")
                    print("1. Add Availability")
                    print("2. List Availability")
                    print("3. Update Availability")
                    print("4. Delete Availability")
                    print("5. Back to Main Menu")
                    sub_choice = input("Select an option: ")
                    if sub_choice == "1":
                        self.add_availability()
                    elif sub_choice == "2":
                        self.list_availability()
                    elif sub_choice == "3":
                        self.update_availability()
                    elif sub_choice == "4":
                        self.delete_availability()
                    elif sub_choice == "5":
                        break
                    else:
                        print("Invalid option. Please try again.")
            elif choice == "4":
                while True:
                    print("\n--- Appointment Operations Menu ---")
                    print("1. Add Appointment")
                    print("2. List Appointments (Real-time view)")
                    print("3. Update Appointment")
                    print("4. Delete Appointment")
                    print("5. Back to Main Menu")
                    sub_choice = input("Select an option: ")
                    if sub_choice == "1":
                        self.add_appointment()
                    elif sub_choice == "2":
                        self.list_appointments()
                    elif sub_choice == "3":
                        self.update_appointment()
                    elif sub_choice == "4":
                        self.delete_appointment()
                    elif sub_choice == "5":
                        break
                    else:
                        print("Invalid option. Please try again.")
            elif choice == "5":
                while True:
                    print("\n--- Payment Operations Menu ---")
                    print("1. Add Payment")
                    print("2. List Payments")
                    print("3. Update Payment")
                    print("4. Delete Payment")
                    print("5. Back to Main Menu")
                    sub_choice = input("Select an option: ")
                    if sub_choice == "1":
                        self.add_payment()
                    elif sub_choice == "2":
                        self.list_payments()
                    elif sub_choice == "3":
                        self.update_payment()
                    elif sub_choice == "4":
                        self.delete_payment()
                    elif sub_choice == "5":
                        break
                    else:
                        print("Invalid option. Please try again.")
            elif choice == "6":
                while True:
                    print("\n--- Medical Record Operations Menu ---")
                    print("1. Add Medical Record")
                    print("2. List Medical Records")
                    print("3. Update Medical Record")
                    print("4. Delete Medical Record")
                    print("5. Back to Main Menu")
                    sub_choice = input("Select an option: ")
                    if sub_choice == "1":
                        self.add_medical_record()
                    elif sub_choice == "2":
                        self.list_medical_records()
                    elif sub_choice == "3":
                        self.update_medical_record()
                    elif sub_choice == "4":
                        self.delete_medical_record()
                    elif sub_choice == "5":
                        break
                    else:
                        print("Invalid option. Please try again.")
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    cli = PatientCLI()
    cli.run()