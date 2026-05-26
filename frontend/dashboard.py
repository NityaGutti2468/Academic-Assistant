import streamlit as st
import requests
import pandas as pd

API_BASE = "http://127.0.0.1:5000"

st.set_page_config(page_title="Nexia Dashboard", layout="wide", page_icon="🎓")

# Custom CSS for more attractive UI
st.markdown("""
<style>
    .metric-row {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .main-header {
        color: #4f46e5;
        font-weight: 700;
    }
    .logout-btn {
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_id = None

def login():
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_id = None

# ----------------- LOGIN SCREEN -----------------
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #4f46e5;'>Nexia Administration Login</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Please enter your credentials.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.form("login_form"):
            user_id = st.text_input("User ID (admin / Mentor ID)")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                if user_id == "admin" and password == "admin":
                    st.session_state.role = "Admin"
                    login()
                    st.rerun()
                elif user_id.isdigit() and password == "mentor":
                    st.session_state.role = "Mentor"
                    st.session_state.user_id = user_id
                    login()
                    st.rerun()
                else:
                    st.error("Invalid credentials. Use 'admin'/'admin' for Admin and '101'/'mentor' for Mentor.")
                    
# ----------------- ADMIN DASHBOARD -----------------
elif st.session_state.role == "Admin":
    # Sidebar
    st.sidebar.title("Admin Menu")
    st.sidebar.markdown(f"**Logged in as:** Admin")
    if st.sidebar.button("Logout", key="logout_admin"):
        logout()
        st.rerun()
        
    st.markdown("<h2 class='main-header'>Admin Dashboard ⚙️</h2>", unsafe_allow_html=True)
    
    # Overview Metrics
    students_res = requests.get(f"{API_BASE}/students")
    students_data = students_res.json().get("students", []) if students_res.status_code == 200 else []
    
    mentors_res = requests.get(f"{API_BASE}/mentors")
    mentors_data = mentors_res.json().get("mentors", []) if mentors_res.status_code == 200 else []

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students Enrolled", len(students_data))
    col2.metric("Active Mentors", len(mentors_data))
    col3.metric("System Load", "Stable")
    
    st.divider()

    tab1, tab2, tab3 = st.tabs(["👥 Student Overview", "🧪 System Actions", "🛠️ Manage Roles"])
    
    with tab1:
        st.subheader("Master Student Database")
        if students_data:
            df = pd.DataFrame(students_data)
            st.dataframe(df, use_container_width=True)
            
            # Simple Chart
            st.markdown("### Average Attendance Trends (Mocked view)")
            if 'attendance' in df.columns:
                # Filter out 'N/A' to plot
                plot_data = df[df['attendance'] != 'N/A']
                if not plot_data.empty:
                    st.bar_chart(plot_data, x="name", y="attendance")
        else:
            st.info("No students found.")
            
    with tab2:
        st.subheader("Global Process Triggers")
        st.write("Force manually run the multi-agent backend scripts instead of waiting for cron scheduler.")
        c1, c2 = st.columns(2)
        if c1.button("▶ Run Attendance Checks"):
            res = requests.post(f"{API_BASE}/trigger-attendance")
            st.success(res.json().get("message", "Attendance triggered"))
        if c2.button("▶ Run Fee Reminders"):
            res = requests.post(f"{API_BASE}/trigger-fees")
            st.success(res.json().get("message", "Fee reminders triggered"))

    with tab3:
        st.subheader("Role Assignments")
        c1, c2 = st.columns(2)
        with c1:
            with st.form("add_mentor"):
                st.write("**Register New Mentor**")
                m_id = st.text_input("Mentor ID")
                m_name = st.text_input("Name")
                m_dept = st.text_input("Department")
                m_phone = st.text_input("Phone Number")
                if st.form_submit_button("Create Mentor", use_container_width=True):
                    res = requests.post(f"{API_BASE}/add-mentor", json={"mentor_id": m_id, "name": m_name, "department": m_dept, "phone": m_phone})
                    if res.status_code == 200: st.success("Created successfully")
                    else: st.error("Error creating mentor")
        with c2:
            with st.form("assign_student"):
                st.write("**Map Student to Mentor**")
                s_id = st.text_input("Student ID")
                target_m_id = st.text_input("Mentor ID")
                if st.form_submit_button("Assign Student", use_container_width=True):
                    res = requests.post(f"{API_BASE}/assign-mentor", json={"student_id": s_id, "mentor_id": target_m_id})
                    if res.status_code == 200: st.success("Assigned successfully")
                    else: st.error("Error assigning student")

# ----------------- MENTOR DASHBOARD -----------------
elif st.session_state.role == "Mentor":
    # Sidebar
    mentor_id = st.session_state.user_id
    st.sidebar.title("Mentor Menu")
    st.sidebar.markdown(f"**Logged in as:** Mentor {mentor_id}")
    if st.sidebar.button("Logout", key="logout_mentor"):
        logout()
        st.rerun()

    st.markdown(f"<h2 class='main-header'>Mentor Dashboard 🎓</h2>", unsafe_allow_html=True)
    st.write(f"Welcome back! Viewing records specifically tracked by Mentor ID: **{mentor_id}**")
    
    # Fetch Mentor Data
    students_res = requests.get(f"{API_BASE}/mentor/{mentor_id}/students")
    students_data = students_res.json().get("students", []) if students_res.status_code == 200 else []
    
    alerts_res = requests.get(f"{API_BASE}/mentor/{mentor_id}/alerts")
    alerts_data = alerts_res.json().get("alerts", []) if alerts_res.status_code == 200 else []

    col1, col2 = st.columns(2)
    col1.metric("Students Assigned", len(students_data))
    col2.metric("Critical Alerts", len(alerts_data), delta_color="inverse")
    
    st.divider()

    tab1, tab2 = st.tabs(["🚨 Priority Alerts", "📋 Student Portfolio"])
    
    with tab1:
        st.subheader("Items Requires Immediate Attention")
        if alerts_data:
            for alert in alerts_data:
                severity_color = "🔴" if alert["severity"] == "High" else "🟠"
                with st.container():
                    st.markdown(f"#### {severity_color} {alert['type']} (Student {alert['student_id']})")
                    st.write(f"**Details:** {alert['message']}")
                    st.markdown("---")
        else:
            st.success("No active critical alerts for your students! 🎉 You're all caught up.")

    with tab2:
        st.subheader("Your Mentees")
        if students_data:
            df = pd.DataFrame(students_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No students are currently assigned to your mentoring group.")
