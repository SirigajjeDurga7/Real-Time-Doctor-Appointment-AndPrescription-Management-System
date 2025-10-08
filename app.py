import streamlit as st
from supabase import create_client, Client
import pandas as pd

# ---------- Connect to Supabase ----------
def init_connection():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ Supabase connection failed: {str(e)}")
        st.stop()

supabase: Client = init_connection()

# ---------- Insert Data ----------
def insert_data(table_name, data):
    try:
        response = supabase.table(table_name).insert(data).execute()
        if response.data:
            st.success("✅ Record inserted successfully!")
        else:
            st.error("❌ Insert failed.")
    except Exception as e:
        st.error(f"❌ Insert failed: {str(e)}")

# ---------- Delete Record ----------
def delete_record(table_name, record_id, id_column):
    try:
        response = supabase.table(table_name).delete().eq(id_column, record_id).execute()
        if response.data:
            st.success("✅ Record deleted successfully!")
        else:
            st.warning("⚠️ ID not found.")
    except Exception as e:
        st.error(f"❌ Deletion failed: {str(e)}")

# ---------- Show Table ----------
def show_table(table_name):
    try:
        response = supabase.table(table_name).select("*").execute()
        df = pd.DataFrame(response.data)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("ℹ️ No records found.")
    except Exception as e:
        st.error(f"❌ Failed to load table: {str(e)}")

# ---------- Home Page ----------
def home_page():
    st.markdown("<h1 style='text-align:center;color:#0078ff;'>🩺 Real-Time Doctor Appointment System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:gray;'>Smartly manage doctors, patients, and medical records.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔐 Login / Signup", use_container_width=True):
        st.session_state.page = "auth"
        st.rerun()

# ---------- Auth Page ----------
def auth_page():
    st.title("🔑 Login / Signup")

    choice = st.radio("Select Action", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        username = st.text_input("Username")
        if st.button("Sign Up"):
            if email.strip() and password.strip() and username.strip():
                try:
                    response = supabase.table("users1").insert({
                        "username": username,
                        "email": email,
                        "password": password
                    }).execute()
                    if response.data:
                        st.success("✅ Signup successful! Please login.")
                    else:
                        st.error("❌ Signup failed.")
                except Exception as e:
                    st.error(f"❌ Signup failed: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all fields.")

    elif choice == "Login":
        if st.button("Login"):
            if email.strip() and password.strip():
                try:
                    response = supabase.table("users1").select("*").eq("email", email).eq("password", password).execute()
                    if response.data:
                        st.session_state.page = "dashboard"
                        st.session_state.user = response.data[0]
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
                except Exception as e:
                    st.error(f"❌ Login failed: {str(e)}")
            else:
                st.warning("⚠️ Please enter email and password.")

# ---------- Dashboard ----------
def dashboard_page():
    st.markdown("<h2 style='color:#0078ff;'>🏥 Hospital Management Dashboard</h2>", unsafe_allow_html=True)

    tables_with_emojis = {
        "patients1": "🧍‍♂️ Patients",
        "doctors1": "🩺 Doctors",
        "availabilityofdoctors1": "📅 Availability",
        "appointments1": "⏰ Appointments",
        "payments1": "💳 Payments",
        "medical_records1": "📋 Medical Records"
    }

    selected_label = st.selectbox("📋 Choose Table to Manage", list(tables_with_emojis.values()))
    selected_table = [tbl for tbl, lbl in tables_with_emojis.items() if lbl == selected_label][0]

    st.markdown("---")
    action = st.radio("Choose an Action", ["View Table", "Insert New Record", "Delete a Record"])

    if action == "View Table":
        show_table(selected_table)
    elif action == "Insert New Record":
        insert_form(selected_table)
    elif action == "Delete a Record":
        delete_form(selected_table)

    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.page = "home"
        st.session_state.user = None
        st.rerun()

# ---------- Insert Form with Validation ----------
def insert_form(table_name):
    st.subheader("➕ Insert New Record")

    if table_name == "patients1":
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        age = st.number_input("Age", 0)
        gender = st.text_input("Gender")
        address = st.text_area("Address")
        if st.button("Insert Patient"):
            if all([full_name.strip(), email.strip(), phone.strip(), age > 0, gender.strip(), address.strip()]):
                insert_data("patients1", {"full_name": full_name, "email": email, "phone": phone, "age": age, "gender": gender, "address": address})
            else:
                st.warning("⚠️ Please fill all fields correctly.")

    elif table_name == "doctors1":
        full_name = st.text_input("Full Name")
        specialization = st.text_input("Specialization")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        experience = st.number_input("Experience (years)", 0)
        if st.button("Insert Doctor"):
            if all([full_name.strip(), specialization.strip(), email.strip(), phone.strip(), experience > 0]):
                insert_data("doctors1", {"full_name": full_name, "specialization": specialization, "email": email, "phone": phone, "experience_years": experience})
            else:
                st.warning("⚠️ Please fill all fields correctly.")

    elif table_name == "availabilityofdoctors1":
        doctor_id = st.number_input("Doctor ID", 0)
        available_date = st.date_input("Available Date")
        start_time = st.time_input("Start Time")
        end_time = st.time_input("End Time")
        is_available = st.checkbox("Available", value=True)
        if st.button("Insert Availability"):
            if doctor_id > 0 and available_date and start_time and end_time:
                insert_data("availabilityofdoctors1", {
                    "doctor_id": doctor_id,
                    "available_date": str(available_date),
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "is_available": is_available
                })
            else:
                st.warning("⚠️ Please fill all fields correctly.")

    elif table_name == "appointments1":
        patient_id = st.number_input("Patient ID", 0)
        doctor_id = st.number_input("Doctor ID", 0)
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.time_input("Appointment Time")
        status = st.text_input("Status", "Scheduled")
        if st.button("Insert Appointment"):
            if patient_id > 0 and doctor_id > 0 and appointment_date and appointment_time and status.strip():
                insert_data("appointments1", {
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "appointment_date": str(appointment_date),
                    "appointment_time": str(appointment_time),
                    "status": status
                })
            else:
                st.warning("⚠️ Please fill all fields correctly.")

    elif table_name == "payments1":
        appointment_id = st.number_input("Appointment ID", 0)
        patient_id = st.number_input("Patient ID", 0)
        amount = st.number_input("Amount", 0.0)
        transaction_id = st.text_input("Transaction ID")
        payment_status = st.text_input("Payment Status", "Pending")
        if st.button("Insert Payment"):
            if appointment_id > 0 and patient_id > 0 and amount > 0 and transaction_id.strip() and payment_status.strip():
                insert_data("payments1", {
                    "appointment_id": appointment_id,
                    "patient_id": patient_id,
                    "amount": amount,
                    "transaction_id": transaction_id,
                    "payment_status": payment_status
                })
            else:
                st.warning("⚠️ Please fill all fields correctly.")

    elif table_name == "medical_records1":
        patient_id = st.number_input("Patient ID", 0)
        doctor_id = st.number_input("Doctor ID", 0)
        appointment_id = st.number_input("Appointment ID", 0)
        diagnosis = st.text_area("Diagnosis")
        prescription = st.text_area("Prescription")
        if st.button("Insert Record"):
            if patient_id > 0 and doctor_id > 0 and appointment_id > 0 and diagnosis.strip() and prescription.strip():
                insert_data("medical_records1", {
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "appointment_id": appointment_id,
                    "diagnosis": diagnosis,
                    "prescription": prescription
                })
            else:
                st.warning("⚠️ Please fill all fields correctly.")

# ---------- Delete Form ----------
def delete_form(table_name):
    st.subheader("❌ Delete Record")
    record_id = st.number_input("Enter Record ID", 0)

    id_map = {
        "patients1": "patient_id",
        "doctors1": "doctor_id",
        "availabilityofdoctors1": "availability_id",
        "appointments1": "appointment_id",
        "payments1": "payment_id",
        "medical_records1": "record_id"
    }

    if st.button("Delete"):
        if record_id > 0:
            delete_record(table_name, record_id, id_map.get(table_name))
        else:
            st.warning("⚠️ Please enter a valid ID.")

# ---------- Main ----------
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "auth":
        auth_page()
    elif st.session_state.page == "dashboard":
        dashboard_page()

if __name__ == "__main__":
    main()
