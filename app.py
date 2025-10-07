import streamlit as st
import psycopg2
import pandas as pd

# ---------- Database Connection ----------
def get_connection():
    try:
        return psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            dbname=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            port=int(st.secrets["postgres"]["port"]),
            sslmode="require"
        )
    except psycopg2.OperationalError as e:
        st.session_state.message = f"❌ Database connection failed: {str(e)}"
        st.session_state.msg_type = "error"
        st.stop()

# ---------- Insert Data ----------
def insert_data(table_name, data):
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()

    queries = {
        "Patients1": "INSERT INTO Patients1 (full_name, email, phone, age, gender, address) VALUES (%s, %s, %s, %s, %s, %s)",
        "Doctors1": "INSERT INTO Doctors1 (full_name, specialization, email, phone, experience_years) VALUES (%s, %s, %s, %s, %s)",
        "AvailabilityOfDoctors1": "INSERT INTO AvailabilityOfDoctors1 (doctor_id, available_date, start_time, end_time, is_available) VALUES (%s, %s, %s, %s, %s)",
        "Appointments1": "INSERT INTO Appointments1 (patient_id, doctor_id, appointment_date, appointment_time, status) VALUES (%s, %s, %s, %s, %s)",
        "Payments1": "INSERT INTO Payments1 (appointment_id, patient_id, amount, transaction_id, payment_status) VALUES (%s, %s, %s, %s, %s)",
        "Medical_Records1": "INSERT INTO Medical_Records1 (patient_id, doctor_id, appointment_id, diagnosis, prescription) VALUES (%s, %s, %s, %s, %s)"
    }

    try:
        cursor.execute(queries[table_name], data)
        conn.commit()
        st.session_state.message = "✅ Record inserted successfully!"
        st.session_state.msg_type = "success"
    except Exception as e:
        conn.rollback()
        st.session_state.message = f"❌ Insert failed: {str(e)}"
        st.session_state.msg_type = "error"
    finally:
        cursor.close()
        conn.close()

# ---------- Delete Record ----------
def delete_record(table_name, record_id):
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    id_column_map = {
        "Patients1": "patient_id",
        "Doctors1": "doctor_id",
        "AvailabilityOfDoctors1": "availability_id",
        "Appointments1": "appointment_id",
        "Payments1": "payment_id",
        "Medical_Records1": "record_id"
    }

    id_col = id_column_map.get(table_name)
    try:
        cur.execute(f"SELECT * FROM {table_name} WHERE {id_col} = %s", (record_id,))
        record = cur.fetchone()
        if record:
            cur.execute(f"DELETE FROM {table_name} WHERE {id_col} = %s", (record_id,))
            conn.commit()
            st.session_state.message = "✅ Record deleted successfully!"
            st.session_state.msg_type = "success"
        else:
            st.session_state.message = "❌ ID not found. Please check and try again."
            st.session_state.msg_type = "error"
    except Exception as e:
        conn.rollback()
        st.session_state.message = f"❌ Deletion failed: {str(e)}"
        st.session_state.msg_type = "error"
    finally:
        cur.close()
        conn.close()

# ---------- Show Persistent Messages ----------
def show_message_below(msg_placeholder=None):
    if "message" in st.session_state and st.session_state.message:
        msg = st.session_state.message
        msg_type = st.session_state.msg_type
        if msg_placeholder:
            if msg_type == "success":
                msg_placeholder.success(msg)
            elif msg_type == "error":
                msg_placeholder.error(msg)
            elif msg_type == "warning":
                msg_placeholder.warning(msg)
        st.session_state.message = None  # clear after showing


def show_message():
    if "message" in st.session_state and st.session_state.message:
        msg = st.session_state.message
        msg_type = st.session_state.msg_type
        if msg_type == "success":
            st.success(msg)
        elif msg_type == "error":
            st.error(msg)
        elif msg_type == "warning":
            st.warning(msg)
        st.session_state.message = None

# ---------- Home Page ----------
def home_page():
    st.markdown("<h1 style='text-align:center;color:#0078ff;'>🩺 Real-Time Doctor Appointment System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:gray;'>A smart way to manage patients, doctors, and prescriptions efficiently.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔐 Login / Sign Up", use_container_width=True):
        st.session_state.page = "auth"
        st.rerun()

# ---------- Authentication Page ----------
def auth_page():
    st.title("🔑 Login / Signup")
    show_message()

    choice = st.radio("Select Action", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    if choice == "Signup":
        username = st.text_input("Username")
        if st.button("Sign Up"):
            if email and password and username:
                try:
                    cur.execute("INSERT INTO Users1 (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
                    conn.commit()
                    st.session_state.message = "✅ Signup successful! Please login."
                    st.session_state.msg_type = "success"
                    st.rerun()
                except Exception as e:
                    st.session_state.message = f"❌ Signup failed: {str(e)}"
                    st.session_state.msg_type = "error"
                    st.rerun()
            else:
                st.warning("⚠️ Please fill in all fields.")
    elif choice == "Login":
        if st.button("Login"):
            cur.execute("SELECT * FROM Users1 WHERE email=%s AND password=%s", (email, password))
            user = cur.fetchone()
            if user:
                st.session_state.page = "dashboard"
                st.session_state.message = None
                st.rerun()
            else:
                st.session_state.message = "❌ Invalid credentials!"
                st.session_state.msg_type = "error"
                st.rerun()

    cur.close()
    conn.close()

# ---------- Dashboard Page ----------
def dashboard_page():
    st.markdown("<h2 style='color:#0078ff;'>🏥 Hospital Management Dashboard</h2>", unsafe_allow_html=True)
    show_message()

    tables_with_emojis = {
        "Patients1": "🧍‍♂️ Patients",
        "Doctors1": "🩺 Doctors",
        "AvailabilityOfDoctors1": "📅 Availability",
        "Appointments1": "⏰ Appointments",
        "Payments1": "💳 Payments",
        "Medical_Records1": "📋 Medical Records"
    }

    st.subheader("📋 Select a Table to Manage:")
    selected_label = st.selectbox("Choose Table", list(tables_with_emojis.values()))
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
        st.session_state.message = None
        st.rerun()

# ---------- View Table ----------
def show_table(table_name):
    conn = get_connection()
    if conn is None:
        return
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Failed to load table: {str(e)}")
    finally:
        conn.close()

# ---------- Insert Form ----------
def insert_form(table_name):
    st.markdown("### ➕ Insert New Record")
    if table_name == "Patients1":
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        age = st.number_input("Age", 0)
        gender = st.text_input("Gender")
        address = st.text_area("Address")
        if st.button("Insert Patient"):
            if all([full_name, email, phone, age, gender, address]):
                insert_data("Patients1", (full_name, email, phone, age, gender, address))
                st.rerun()
            else:
                st.warning("⚠️ Please fill all fields.")

    elif table_name == "Doctors1":
        full_name = st.text_input("Full Name")
        specialization = st.text_input("Specialization")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        experience = st.number_input("Experience (years)", 0)
        if st.button("Insert Doctor"):
            if all([full_name, specialization, email, phone, experience]):
                insert_data("Doctors1", (full_name, specialization, email, phone, experience))
                st.rerun()
            else:
                st.warning("⚠️ Please fill all fields.")

    elif table_name == "AvailabilityOfDoctors1":
        doctor_id = st.number_input("Doctor ID", 0)
        available_date = st.date_input("Available Date")
        start_time = st.time_input("Start Time")
        end_time = st.time_input("End Time")
        is_available = st.checkbox("Available", value=True)
        if st.button("Insert Availability"):
            if doctor_id and available_date and start_time and end_time:
                insert_data("AvailabilityOfDoctors1", (doctor_id, available_date, start_time, end_time, is_available))
                st.rerun()
            else:
                st.warning("⚠️ Please fill all fields.")

    elif table_name == "Appointments1":
        patient_id = st.number_input("Patient ID", 0)
        doctor_id = st.number_input("Doctor ID", 0)
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.time_input("Appointment Time")
        status = st.text_input("Status", "Scheduled")
        if st.button("Insert Appointment"):
            if patient_id and doctor_id and appointment_date and appointment_time and status:
                insert_data("Appointments1", (patient_id, doctor_id, appointment_date, appointment_time, status))
                st.rerun()
            else:
                st.warning("⚠️ Please fill all fields.")

    elif table_name == "Payments1":
        appointment_id = st.number_input("Appointment ID", 0)
        patient_id = st.number_input("Patient ID", 0)
        amount = st.number_input("Amount", 0.0)
        transaction_id = st.text_input("Transaction ID")
        payment_status = st.text_input("Payment Status", "Pending")
        if st.button("Insert Payment"):
            if all([appointment_id, patient_id, amount, transaction_id, payment_status]):
                insert_data("Payments1", (appointment_id, patient_id, amount, transaction_id, payment_status))
                st.rerun()
            else:
                st.warning("⚠️ Please fill all fields.")

    elif table_name == "Medical_Records1":
        patient_id = st.number_input("Patient ID", 0)
        doctor_id = st.number_input("Doctor ID", 0)
        appointment_id = st.number_input("Appointment ID", 0)
        diagnosis = st.text_area("Diagnosis")
        prescription = st.text_area("Prescription")
        if st.button("Insert Record"):
            if all([patient_id, doctor_id, appointment_id, diagnosis, prescription]):
                insert_data("Medical_Records1", (patient_id, doctor_id, appointment_id, diagnosis, prescription))
                st.rerun()
            else:
                st.warning("⚠️ Please fill all fields.")

# ---------- Delete Form ----------
def delete_form(table_name):
    st.markdown("### ❌ Delete Record by ID")
    record_id = st.number_input("Enter Record ID to Delete", 0)

    delete_btn = st.button("Delete Record")

    # Message placeholder BELOW button
    msg_placeholder = st.empty()

    if delete_btn:
        if record_id > 0:
            delete_record(table_name, record_id)
            show_message_below(msg_placeholder)
        else:
            msg_placeholder.warning("⚠️ Please enter a valid ID.")

# ---------- Main Controller ----------
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "message" not in st.session_state:
        st.session_state.message = None
        st.session_state.msg_type = None

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "auth":
        auth_page()
    elif st.session_state.page == "dashboard":
        dashboard_page()

if __name__ == "__main__":
    main()
