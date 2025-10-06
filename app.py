import streamlit as st
import psycopg2
import pandas as pd

# ---------- Database Connection ----------
import streamlit as st
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"]
        sslmode="require"
    )


# ---------- Insert Data ----------
def insert_data(table_name, data):
    conn = get_connection()
    cursor = conn.cursor()

    queries = {
        "Patients1": "INSERT INTO Patients1 (full_name, email, phone, age, gender, address) VALUES (%s,%s,%s,%s,%s,%s)",
        "Doctors1": "INSERT INTO Doctors1 (full_name, specialization, email, phone, experience_years) VALUES (%s,%s,%s,%s,%s)",
        "AvailabilityOfDoctors1": "INSERT INTO AvailabilityOfDoctors1 (doctor_id, available_date, start_time, end_time, is_available) VALUES (%s,%s,%s,%s,%s)",
        "Appointments1": "INSERT INTO Appointments1 (patient_id, doctor_id, appointment_date, appointment_time, status) VALUES (%s,%s,%s,%s,%s)",
        "Payments1": "INSERT INTO Payments1 (appointment_id, patient_id, amount, transaction_id, payment_status) VALUES (%s,%s,%s,%s,%s)",
        "Medical_Records1": "INSERT INTO Medical_Records1 (patient_id, doctor_id, appointment_id, diagnosis, prescription) VALUES (%s,%s,%s,%s,%s)"
    }

    cursor.execute(queries[table_name], data)
    conn.commit()
    cursor.close()
    conn.close()


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
    choice = st.radio("Select Action", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "Signup":
        username = st.text_input("Username")
        if st.button("Sign Up"):
            if email and password and username:
                cur.execute("INSERT INTO Users1 (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
                conn.commit()
                st.success("✅ Signup successful! Please login.")
            else:
                st.warning("⚠️ Please fill in all fields.")
    elif choice == "Login":
        if st.button("Login"):
            cur.execute("SELECT * FROM Users1 WHERE email=%s AND password=%s", (email, password))
            user = cur.fetchone()
            if user:
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid credentials!")

    cur.close()
    conn.close()


# ---------- Dashboard Page ----------
def dashboard_page():
    st.markdown("<h2 style='color:#0078ff;'>🏥 Hospital Management Dashboard</h2>", unsafe_allow_html=True)

    # Sidebar with table list
    st.sidebar.header("📋 Tables Menu")

    tables_with_emojis = {
        "Patients1": "🧍‍♂️ Patients",
        "Doctors1": "🩺 Doctors",
        "AvailabilityOfDoctors1": "📅 Availability",
        "Appointments1": "⏰ Appointments",
        "Payments1": "💳 Payments",
        "Medical_Records1": "📋 Medical Records"
    }

    selected_label = st.sidebar.radio("Select a Table", list(tables_with_emojis.values()))
    selected_table = [tbl for tbl, lbl in tables_with_emojis.items() if lbl == selected_label][0]

    st.markdown("---")
    show_table(selected_table)

    # Sidebar bottom navigation buttons
    st.sidebar.markdown("---")
    if st.sidebar.button("⬅️ Go Back to Login Page"):
        st.session_state.page = "auth"
        st.rerun()

    if st.sidebar.button("🚪 Logout"):
        st.session_state.page = "home"
        st.rerun()


# ---------- Display Table and Insert Form ----------
def show_table(table_name):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    st.subheader(f"📊 Viewing {table_name.replace('1','')} Data")
    st.dataframe(df, use_container_width=True)

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
                st.success("✅ Patient added successfully!")
            else:
                st.warning("⚠️ Please fill all fields before inserting!")

    elif table_name == "Doctors1":
        full_name = st.text_input("Full Name")
        specialization = st.text_input("Specialization")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        experience = st.number_input("Experience (years)", 0)
        if st.button("Insert Doctor"):
            if all([full_name, specialization, email, phone, experience]):
                insert_data("Doctors1", (full_name, specialization, email, phone, experience))
                st.success("✅ Doctor added successfully!")
            else:
                st.warning("⚠️ Please fill all fields before inserting!")

    elif table_name == "AvailabilityOfDoctors1":
        doctor_id = st.number_input("Doctor ID", 0)
        available_date = st.date_input("Available Date")
        start_time = st.time_input("Start Time")
        end_time = st.time_input("End Time")
        is_available = st.checkbox("Available", value=True)
        if st.button("Insert Availability"):
            if doctor_id and available_date and start_time and end_time:
                insert_data("AvailabilityOfDoctors1", (doctor_id, available_date, start_time, end_time, is_available))
                st.success("✅ Availability added successfully!")
            else:
                st.warning("⚠️ Please fill all fields before inserting!")

    elif table_name == "Appointments1":
        patient_id = st.number_input("Patient ID", 0)
        doctor_id = st.number_input("Doctor ID", 0)
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.time_input("Appointment Time")
        status = st.text_input("Status", "Scheduled")
        if st.button("Insert Appointment"):
            if patient_id and doctor_id and appointment_date and appointment_time and status:
                insert_data("Appointments1", (patient_id, doctor_id, appointment_date, appointment_time, status))
                st.success("✅ Appointment added successfully!")
            else:
                st.warning("⚠️ Please fill all fields before inserting!")

    elif table_name == "Payments1":
        appointment_id = st.number_input("Appointment ID", 0)
        patient_id = st.number_input("Patient ID", 0)
        amount = st.number_input("Amount", 0.0)
        transaction_id = st.text_input("Transaction ID")
        payment_status = st.text_input("Payment Status", "Pending")
        if st.button("Insert Payment"):
            if all([appointment_id, patient_id, amount, transaction_id, payment_status]):
                insert_data("Payments1", (appointment_id, patient_id, amount, transaction_id, payment_status))
                st.success("✅ Payment added successfully!")
            else:
                st.warning("⚠️ Please fill all fields before inserting!")

    elif table_name == "Medical_Records1":
        patient_id = st.number_input("Patient ID", 0)
        doctor_id = st.number_input("Doctor ID", 0)
        appointment_id = st.number_input("Appointment ID", 0)
        diagnosis = st.text_area("Diagnosis")
        prescription = st.text_area("Prescription")
        if st.button("Insert Record"):
            if all([patient_id, doctor_id, appointment_id, diagnosis, prescription]):
                insert_data("Medical_Records1", (patient_id, doctor_id, appointment_id, diagnosis, prescription))
                st.success("✅ Record added successfully!")
            else:
                st.warning("⚠️ Please fill all fields before inserting!")

    conn.close()


# ---------- Main Controller ----------
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
