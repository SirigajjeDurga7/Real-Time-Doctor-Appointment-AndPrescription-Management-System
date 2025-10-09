
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

# ---------- Search Record ----------
def search_records(table_name):
    st.subheader("🔍 Search Records")

    # Define available search fields per table
    search_fields = {
        "patients1": ["patient_id", "full_name"],
        "doctors1": ["doctor_id", "full_name"],
        "availabilityofdoctors1": ["availability_id", "doctor_id"],
        "appointments1": ["appointment_id", "doctor_id", "patient_id"],
        "payments1": ["payment_id", "appointment_id", "patient_id"],
        "medical_records1": ["record_id", "doctor_id", "patient_id"]
    }

    # Show dropdown
    search_field = st.selectbox("Search by:", search_fields.get(table_name, []))
    search_value = st.text_input("Enter search value")

    if st.button("Search"):
        if not search_value.strip():
            st.warning("⚠️ Please enter a search value.")
            return

        try:
            # Determine if field is numeric
            numeric_fields = [
                "patient_id", "doctor_id", "appointment_id",
                "availability_id", "payment_id", "record_id"
            ]

            if search_field in numeric_fields and search_value.isdigit():
                response = supabase.table(table_name).select("*").eq(search_field, int(search_value)).execute()
            else:
                response = supabase.table(table_name).select("*").ilike(search_field, f"%{search_value}%").execute()

            df = pd.DataFrame(response.data)
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ℹ️ No matching records found.")
        except Exception as e:
            st.error(f"❌ Search failed: {str(e)}")


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
    st.markdown("<h2>🔑 Login / Signup</h2>", unsafe_allow_html=True)
    choice = st.radio("Select Action", ["Login", "Signup"], horizontal=True)
    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")

    if choice == "Signup":
        username = st.text_input("👤 Username")
        if st.button("Sign Up", use_container_width=True):
            if email.strip() and password.strip() and username.strip():
                try:
                    response = supabase.table("users1").insert({
                        "username": username, "email": email, "password": password
                    }).execute()
                    if response.data:
                        st.success("✅ Signup successful! Please login.")
                    else:
                        st.error("❌ Signup failed.")
                except Exception as e:
                    st.error(f"❌ Signup failed: {str(e)}")
            else:
                st.warning("⚠️ Please fill all fields.")

    elif choice == "Login":
        if st.button("Login", use_container_width=True):
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
                st.warning("⚠️ Please enter both email and password.")

# ---------- Dashboard ----------
def dashboard_page():
    st.markdown("<h2 style='color:#0056b3;'>🏥 Hospital Management Dashboard</h2>", unsafe_allow_html=True)

    tables_with_emojis = {
        "patients1": "🧍‍♂️ Patients",
        "doctors1": "🩺 Doctors",
        "availabilityofdoctors1": "📅 Availability",
        "appointments1": "⏰ Appointments",
        "payments1": "💳 Payments",
        "medical_records1": "📋 Medical Records"
    }

    selected_label = st.selectbox("📂 Choose Table to Manage", list(tables_with_emojis.values()))
    selected_table = [tbl for tbl, lbl in tables_with_emojis.items() if lbl == selected_label][0]

    st.markdown("---")
    action = st.radio("Choose an Action:", ["View Table", "Insert New Record", "Delete a Record", "Search Records"], horizontal=True)

    if action == "View Table":
        show_table(selected_table)
    elif action == "Insert New Record":
        insert_form(selected_table)
    elif action == "Delete a Record":
        delete_form(selected_table)
    elif action == "Search Records":
        search_records(selected_table)

    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.user = None
        st.rerun()

# ----------------------------------------------------------
# ➕ Insert Forms with Validation
# ----------------------------------------------------------
def insert_form(table_name):
    st.subheader("➕ Add New Record")

    def check_required(fields):
        return all(str(v).strip() for v in fields)

    if table_name == "patients1":
        full_name = st.text_input("👤 Full Name")
        email = st.text_input("📧 Email")
        phone = st.text_input("📞 Phone")
        age = st.number_input("🎂 Age", 0)
        gender = st.text_input("⚧ Gender")
        address = st.text_area("🏠 Address")

        if st.button("💾 Insert Patient"):
            if check_required([full_name, email, phone, gender, address]) and age > 0:
                insert_data("patients1", {"full_name": full_name, "email": email, "phone": phone,
                                          "age": age, "gender": gender, "address": address})
            else:
                st.warning("⚠️ Please fill in all fields correctly.")

    elif table_name == "doctors1":
        full_name = st.text_input("👨‍⚕️ Full Name")
        specialization = st.text_input("🧠 Specialization")
        email = st.text_input("📧 Email")
        phone = st.text_input("📞 Phone")
        experience = st.number_input("💼 Experience (years)", 0)
        if st.button("💾 Insert Doctor"):
            if check_required([full_name, specialization, email, phone]) and experience > 0:
                insert_data("doctors1", {"full_name": full_name, "specialization": specialization,
                                         "email": email, "phone": phone, "experience_years": experience})
            else:
                st.warning("⚠️ Please fill all fields correctly.")

    elif table_name == "availabilityofdoctors1":
        doctor_id = st.number_input("🩺 Doctor ID", 0)
        available_date = st.date_input("📅 Available Date")
        start_time = st.time_input("🕓 Start Time")
        end_time = st.time_input("🕒 End Time")
        is_available = st.checkbox("✅ Available", value=True)

        if st.button("💾 Insert Availability"):
            if doctor_id > 0:
                insert_data("availabilityofdoctors1", {
                    "doctor_id": doctor_id, "available_date": str(available_date),
                    "start_time": str(start_time), "end_time": str(end_time),
                    "is_available": is_available
                })
            else:
                st.warning("⚠️ Doctor ID is required.")

    elif table_name == "appointments1":
        patient_id = st.number_input("🧍‍♂️ Patient ID", 0)
        doctor_id = st.number_input("🩺 Doctor ID", 0)
        appointment_date = st.date_input("📆 Appointment Date")
        appointment_time = st.time_input("⏰ Appointment Time")
        status = st.text_input("📌 Status", "Scheduled")

        if st.button("💾 Insert Appointment"):
            if patient_id > 0 and doctor_id > 0:
                insert_data("appointments1", {"patient_id": patient_id, "doctor_id": doctor_id,
                                              "appointment_date": str(appointment_date),
                                              "appointment_time": str(appointment_time),
                                              "status": status})
            else:
                st.warning("⚠️ Please enter valid Patient and Doctor IDs.")

    elif table_name == "payments1":
        appointment_id = st.number_input("⏱️ Appointment ID", 0)
        patient_id = st.number_input("🧍‍♂️ Patient ID", 0)
        amount = st.number_input("💰 Amount", 0.0)
        transaction_id = st.text_input("💳 Transaction ID")
        payment_status = st.text_input("📊 Payment Status", "Pending")

        if st.button("💾 Insert Payment"):
            if appointment_id > 0 and patient_id > 0 and amount > 0 and transaction_id.strip():
                insert_data("payments1", {"appointment_id": appointment_id, "patient_id": patient_id,
                                          "amount": amount, "transaction_id": transaction_id,
                                          "payment_status": payment_status})
            else:
                st.warning("⚠️ Please fill all fields correctly.")

    elif table_name == "medical_records1":
        patient_id = st.number_input("🧍‍♂️ Patient ID", 0)
        doctor_id = st.number_input("🩺 Doctor ID", 0)
        appointment_id = st.number_input("⏰ Appointment ID", 0)
        diagnosis = st.text_area("🧾 Diagnosis")
        prescription = st.text_area("💊 Prescription")

        if st.button("💾 Insert Medical Record"):
            if all([patient_id > 0, doctor_id > 0, appointment_id > 0, diagnosis.strip(), prescription.strip()]):
                insert_data("medical_records1", {"patient_id": patient_id, "doctor_id": doctor_id,
                                                 "appointment_id": appointment_id, "diagnosis": diagnosis,
                                                 "prescription": prescription})
            else:
                st.warning("⚠️ Please fill all fields correctly.")


# ---------- Search Form ----------
def search_form(table_name):
    st.subheader("🔍 Search Records")

    if table_name == "patients1":
        option = st.selectbox("Search by:", ["Patient ID", "Full Name"])
        query = st.text_input("Enter search value")
        if st.button("Search"):
            if query.strip():
                if option == "Patient ID":
                    search_record(table_name, "patient_id", query)
                else:
                    search_record(table_name, "full_name", query)
            else:
                st.warning("⚠️ Please enter a value to search.")

    elif table_name == "doctors1":
        option = st.selectbox("Search by:", ["Doctor ID", "Full Name"])
        query = st.text_input("Enter search value")
        if st.button("Search"):
            if query.strip():
                if option == "Doctor ID":
                    search_record(table_name, "doctor_id", query)
                else:
                    search_record(table_name, "full_name", query)
            else:
                st.warning("⚠️ Please enter a value to search.")

    elif table_name == "availabilityofdoctors1":
        option = st.selectbox("Search by:", ["Availability ID", "Doctor ID"])
        query = st.text_input("Enter search value")
        if st.button("Search"):
            if query.strip():
                if option == "Availability ID":
                    search_record(table_name, "availability_id", query)
                else:
                    search_record(table_name, "doctor_id", query)
            else:
                st.warning("⚠️ Please enter a value to search.")

    elif table_name == "appointments1":
        option = st.selectbox("Search by:", ["Appointment ID", "Doctor ID", "Patient ID"])
        query = st.text_input("Enter search value")
        if st.button("Search"):
            if query.strip():
                col_map = {
                    "Appointment ID": "appointment_id",
                    "Doctor ID": "doctor_id",
                    "Patient ID": "patient_id"
                }
                search_record(table_name, col_map[option], query)
            else:
                st.warning("⚠️ Please enter a value to search.")

    elif table_name == "payments1":
        option = st.selectbox("Search by:", ["Payment ID", "Appointment ID", "Patient ID"])
        query = st.text_input("Enter search value")
        if st.button("Search"):
            if query.strip():
                col_map = {
                    "Payment ID": "payment_id",
                    "Appointment ID": "appointment_id",
                    "Patient ID": "patient_id"
                }
                search_record(table_name, col_map[option], query)
            else:
                st.warning("⚠️ Please enter a value to search.")

    elif table_name == "medical_records1":
        option = st.selectbox("Search by:", ["Record ID", "Doctor ID", "Patient ID"])
        query = st.text_input("Enter search value")
        if st.button("Search"):
            if query.strip():
                col_map = {
                    "Record ID": "record_id",
                    "Doctor ID": "doctor_id",
                    "Patient ID": "patient_id"
                }
                search_record(table_name, col_map[option], query)
            else:
                st.warning("⚠️ Please enter a value to search.")



# ---------- Delete Form ----------
def delete_form(table_name):
    st.markdown("<h3 style='color:#ff4b4b;'>❌ Delete Record</h3>", unsafe_allow_html=True)
    record_id = st.number_input("Enter Record ID", 0)
    id_map = {
        "patients1": "patient_id",
        "doctors1": "doctor_id",
        "availabilityofdoctors1": "availability_id",
        "appointments1": "appointment_id",
        "payments1": "payment_id",
        "medical_records1": "record_id"
    }
    if st.button("🗑️ Delete Record"):
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

