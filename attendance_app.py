import streamlit as st
import datetime
import math
import pandas as pd

st.set_page_config(page_title="IIITP Attendance Tracker for CSE(SEC-A)", layout="wide", initial_sidebar_state="collapsed")


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700;900&display=swap');

    .stApp {
        background-color: #09090B;
        color: #FAFAFA;
        font-family: 'Space Grotesk', sans-serif;
    }
    .kinetic-title {
        font-size: clamp(3rem, 10vw, 12rem);
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.05em;
        line-height: 0.85;
        margin-bottom: 2rem;
        margin-top: -1rem;
    }
    .text-white { color: #FAFAFA; }
    .text-yellow { color: #DFE104; }
    
    .kinetic-subtitle {
        font-size: clamp(1.5rem, 4vw, 4rem);
        font-weight: 700;
        text-transform: uppercase;
        color: #DFE104;
        letter-spacing: -0.02em;
        margin-bottom: 1rem;
    }

    .marquee-container {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        background-color: #DFE104;
        color: #000000;
        padding: 1.5rem 0;
        margin: 2rem 0 3rem 0;
        border-top: 2px solid #3F3F46;
        border-bottom: 2px solid #3F3F46;
    }
    .marquee-content {
        display: inline-block;
        font-size: clamp(1.5rem, 3vw, 3rem);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: -0.05em;
        animation: marquee-scroll 15s linear infinite;
    }
    @keyframes marquee-scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    .stButton>button {
        background-color: transparent;
        color: #FAFAFA;
        border: 2px solid #3F3F46;
        border-radius: 0px !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        padding: 0.8rem 0.2rem;
        font-size: 0.95rem;
        transition: all 0.2s ease-in-out;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
    }
    .stButton>button[kind="primary"] {
        background-color: #DFE104;
        color: #000000;
        border-color: #DFE104;
    }
    .stButton>button:hover {
        background-color: #DFE104 !important;
        color: #000000 !important;
        border-color: #DFE104 !important;
        transform: scale(1.03);
    }
    .stButton>button:active {
        transform: scale(0.97);
    }

    div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0px !important;
        border-bottom: 2px solid #3F3F46 !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-bottom: 2px solid #DFE104 !important;
    }
    input {
        color: #FAFAFA !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.5rem !important;
        text-transform: uppercase !important;
    }

    div[data-testid="metric-container"] {
        background-color: #09090B;
        border: 2px solid #3F3F46;
        border-radius: 0px;
        padding: 2rem 1rem;
        text-align: center;
        transition: all 0.1s;
    }
    div[data-testid="metric-container"] label {
        color: #A1A1AA !important;
        font-family: 'Space Grotesk', sans-serif;
        text-transform: uppercase;
        font-weight: 500;
        letter-spacing: 0.1em;
    }
    div[data-testid="metric-container"] div {
        color: #FAFAFA !important;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem !important;
        font-weight: 900;
    }
    div[data-testid="metric-container"]:hover {
        background-color: #DFE104;
        border-color: #DFE104;
    }
    div[data-testid="metric-container"]:hover label,
    div[data-testid="metric-container"]:hover div {
        color: #000000 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 2px solid #3F3F46;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif;
        text-transform: uppercase;
        font-weight: 700;
        color: #A1A1AA;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        color: #DFE104 !important;
        border-bottom: 2px solid #DFE104 !important;
        background-color: transparent !important;
    }
    
    [data-testid="stDataFrame"] {
        border: 2px solid #3F3F46;
        font-family: 'Space Grotesk', sans-serif;
    }
</style>
""", unsafe_allow_html=True)



START_DATE = datetime.date(2026, 8, 20)
END_DATE = datetime.date(2026, 12, 11)

HOLIDAYS = [
    datetime.date(2026, 8, 26), datetime.date(2026, 9, 14), 
    datetime.date(2026, 10, 2), datetime.date(2026, 10, 13), 
    datetime.date(2026, 10, 14), datetime.date(2026, 10, 15), 
    datetime.date(2026, 10, 16), datetime.date(2026, 10, 20), 
    datetime.date(2026, 10, 23), datetime.date(2026, 10, 24), 
    datetime.date(2026, 10, 25), datetime.date(2026, 11, 9), 
    datetime.date(2026, 11, 10), datetime.date(2026, 11, 11), 
    datetime.date(2026, 11, 24)
]

def get_timetable(lab_group):
    tt = {
        0: ["CDE", "LWS", "CPCP"],
        1: ["EVS", "CDE", "CDE Tut"],
        2: ["ET", "BEE", "CPCP", "IKS / EVS", "LWS"],
        3: ["BEE", "CDE", "ET"],
        4: ["CPCP", "ET", "BEE"]
    }
    if lab_group == "G1":
        tt[0].append("BEE Lab")
        tt[1].append("CPCP Lab")
    elif lab_group == "G2":
        tt[0].append("CPCP Lab")
        tt[1].append("BEE Lab")
    elif lab_group == "G3":
        tt[3].append("CPCP Lab")
        tt[4].append("BEE Lab")
    return tt



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""


if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "student": "student123",
        st.secrets["credentials"]["admin_username"]: st.secrets["credentials"]["admin_password"]
    }

if "lab_batch" not in st.session_state:
    st.session_state.lab_batch = "G1"
    
if "absences" not in st.session_state:
    st.session_state.absences = {}
    
if "extra_classes" not in st.session_state:
    st.session_state.extra_classes = {}
    
if "cancelled_classes" not in st.session_state:
    st.session_state.cancelled_classes = {}

if "current_subject" not in st.session_state:
    st.session_state.current_subject = "BEE"

def get_active_classes(subj):
    tt = get_timetable(st.session_state.lab_batch)
    valid_dates = set()
    curr_date = START_DATE
    
    while curr_date <= END_DATE:
        if curr_date.weekday() < 5 and curr_date not in HOLIDAYS:
            if subj in tt.get(curr_date.weekday(), []):
                valid_dates.add(curr_date)
        curr_date += datetime.timedelta(days=1)
        
    for extra_date in st.session_state.extra_classes.get(subj, []):
        valid_dates.add(extra_date)
    for cancel_date in st.session_state.cancelled_classes.get(subj, []):
        valid_dates.discard(cancel_date)
        
    return sorted(list(valid_dates))

def get_all_subjects():
    tt = get_timetable(st.session_state.lab_batch)
    subjects = set()
    for day, subjs in tt.items():
        subjects.update(subjs)
    return sorted(list(subjects))




if not st.session_state.logged_in:
    st.markdown("""
    <div class="kinetic-title">
        <span class="text-white">ATTENDANCE</span><br>
        <span class="text-yellow">TRACKER</span><br>
        <span class="text-yellow">PORTAL</span>
    </div>
    """, unsafe_allow_html=True)
    
    auth_tab1, auth_tab2 = st.tabs(["LOG IN", "SIGN UP"])
    
    with auth_tab1:
        st.markdown('<div class="kinetic-subtitle">ENTER DETAILS</div>', unsafe_allow_html=True)
        l_user = st.text_input("USERNAME", key="l_user")
        l_pass = st.text_input("PASSWORD", type="password", key="l_pass")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("LOG IN", type="primary", key="login_btn"):
            clean_user = l_user.strip()
            clean_pass = l_pass.strip()
            
            if clean_user in st.session_state.users_db and st.session_state.users_db[clean_user] == clean_pass:
                st.session_state.logged_in = True
                st.session_state.username = clean_user
                st.session_state.role = "Admin" if clean_user == "admin" else "Student"
                st.rerun()
            else:
                st.error("INVALID USERNAME OR PASSWORD.")

    with auth_tab2:
        st.markdown('<div class="kinetic-subtitle">CREATE ACCOUNT</div>', unsafe_allow_html=True)
        s_user = st.text_input("CHOOSE USERNAME", key="s_user")
        s_pass = st.text_input("CHOOSE PASSWORD", type="password", key="s_pass")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("REGISTER", key="signup_btn"):
            clean_s_user = s_user.strip()
            clean_s_pass = s_pass.strip()
            if not clean_s_user or not clean_s_pass:
                st.error("FIELDS CANNOT BE BLANK.")
            elif clean_s_user in st.session_state.users_db:
                st.error("USERNAME ALREADY EXISTS.")
            else:
                st.session_state.users_db[clean_s_user] = clean_s_pass
                st.success("ACCOUNT CREATED. SWITCH TO LOG IN TAB.")
                
    st.stop()




st.sidebar.markdown(f'<div class="kinetic-subtitle">{st.session_state.role}</div>', unsafe_allow_html=True)
st.sidebar.write(f"USER: **{st.session_state.username.upper()}**")

if st.sidebar.button("LOGOUT"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""
    st.rerun()

all_subjects = get_all_subjects()

if st.session_state.role == "Student":
    st.sidebar.markdown("---")
    new_batch = st.sidebar.selectbox("SELECT LAB BATCH", ["G1", "G2", "G3"], index=["G1", "G2", "G3"].index(st.session_state.lab_batch))
    if new_batch != st.session_state.lab_batch:
        st.session_state.lab_batch = new_batch
        st.session_state.current_subject = get_all_subjects()[0]
        st.rerun()



if st.session_state.role == "Student":
    low_attendance_subjects = []
    for s in all_subjects:
        active_dates = get_active_classes(s)
        if len(active_dates) > 0:
            valid_absences = [d for d in st.session_state.absences.get(s, []) if d in active_dates]
            attended = len(active_dates) - len(valid_absences)
            percentage = (attended / len(active_dates)) * 100
            if percentage < 80:
                low_attendance_subjects.append(f"{s} ({percentage:.1f}%)")
                
    if low_attendance_subjects:
        warning_msg = f"⚠️ WARNING: Attendance has fallen below 80% in: {', '.join(low_attendance_subjects)}"
        st.error(warning_msg)



total_overall_classes = 0
total_overall_attended = 0

for s in all_subjects:
    active_dates = get_active_classes(s)
    total_overall_classes += len(active_dates)
    valid_absences = [d for d in st.session_state.absences.get(s, []) if d in active_dates]
    total_overall_attended += (len(active_dates) - len(valid_absences))

overall_percentage = (total_overall_attended / total_overall_classes * 100) if total_overall_classes > 0 else 0

st.markdown("""
<div class="kinetic-title">
    <span class="text-white">ATTENDANCE</span><br>
    <span class="text-yellow">TRACKING</span><br>
    <span class="text-yellow">SYSTEM</span>
</div>
""", unsafe_allow_html=True)

marquee_text = f"OVERALL METRICS /// ATTENDANCE: {overall_percentage:.1f}% /// ATTENDED: {total_overall_attended} /// TOTAL CLASSES: {total_overall_classes} /// " * 3
st.markdown(f"""
<div class="marquee-container">
    <div class="marquee-content">{marquee_text}</div>
</div>
""", unsafe_allow_html=True)



st.markdown('<div class="kinetic-subtitle">SELECT SUBJECT</div>', unsafe_allow_html=True)
cols = st.columns(len(all_subjects))
for idx, subj in enumerate(all_subjects):
    with cols[idx]:
        btn_type = "primary" if st.session_state.current_subject == subj else "secondary"
        if st.button(subj, key=f"tab_{subj}", type=btn_type):
            st.session_state.current_subject = subj
            st.rerun()

current_subj = st.session_state.current_subject
active_classes = get_active_classes(current_subj)
subj_absences = [d for d in st.session_state.absences.get(current_subj, []) if d in active_classes]

total_subj_classes = len(active_classes)
attended_subj = total_subj_classes - len(subj_absences)
subj_percentage = (attended_subj / total_subj_classes * 100) if total_subj_classes > 0 else 0
mandatory_subj = math.ceil(0.75 * total_subj_classes)
skips_remaining = (total_subj_classes - mandatory_subj) - len(subj_absences)

st.markdown("<br><br>", unsafe_allow_html=True)

s_col1, s_col2, s_col3 = st.columns(3)
s_col1.metric("SUBJECT ATTENDANCE", f"{subj_percentage:.1f}%")
s_col2.metric("SKIPS REMAINING", skips_remaining)
s_col3.metric("TOTAL CLASSES", total_subj_classes)

st.markdown("<br>", unsafe_allow_html=True)



if st.session_state.role == "Student":
    st.markdown('<div class="kinetic-subtitle">MARK ATTENDANCE</div>', unsafe_allow_html=True)
    
    today = datetime.date.today()
    selected_date = st.date_input("SELECT DATE", value=today)
    
    if selected_date in active_classes:
        is_absent = selected_date in st.session_state.absences.get(current_subj, [])
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            att_label = "MARKED: ATTENDED" if not is_absent else "MARK AS ATTENDED"
            if st.button(att_label, type="primary" if not is_absent else "secondary", use_container_width=True):
                if is_absent:
                    st.session_state.absences[current_subj].remove(selected_date)
                    st.rerun()
        with btn_col2:
            skip_label = "MARKED: SKIPPED" if is_absent else "MARK AS SKIPPED"
            if st.button(skip_label, type="primary" if is_absent else "secondary", use_container_width=True):
                if not is_absent:
                    if current_subj not in st.session_state.absences:
                        st.session_state.absences[current_subj] = []
                    st.session_state.absences[current_subj].append(selected_date)
                    st.rerun()
    else:
        st.info(f"NO {current_subj} CLASS SCHEDULED ON {selected_date.strftime('%b %d, %Y')}.")



if st.session_state.role == "Admin":
    st.markdown("---")
    st.markdown('<div class="kinetic-subtitle">SCHEDULE CONTROLS</div>', unsafe_allow_html=True)
    
    admin_date = st.date_input("SELECT DATE TO MODIFY", value=datetime.date.today(), key="admin_date")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        if st.button("ADD EXTRA CLASS", type="primary"):
            if current_subj not in st.session_state.extra_classes:
                st.session_state.extra_classes[current_subj] = []
            if admin_date not in st.session_state.extra_classes[current_subj]:
                st.session_state.extra_classes[current_subj].append(admin_date)
                if current_subj in st.session_state.cancelled_classes and admin_date in st.session_state.cancelled_classes[current_subj]:
                    st.session_state.cancelled_classes[current_subj].remove(admin_date)
                st.success(f"EXTRA CLASS ADDED ON {admin_date}")
                st.rerun()
            else:
                st.warning("CLASS ALREADY EXISTS ON THIS DATE.")
                
    with col_a2:
        if st.button("CANCEL CLASS", type="primary"):
            if current_subj not in st.session_state.cancelled_classes:
                st.session_state.cancelled_classes[current_subj] = []
            if admin_date not in st.session_state.cancelled_classes[current_subj]:
                st.session_state.cancelled_classes[current_subj].append(admin_date)
                if current_subj in st.session_state.extra_classes and admin_date in st.session_state.extra_classes[current_subj]:
                    st.session_state.extra_classes[current_subj].remove(admin_date)
                st.success(f"CLASS CANCELLED ON {admin_date}")
                st.rerun()
            else:
                st.warning("CLASS IS ALREADY CANCELLED.")

    st.markdown("---")
    
    st.markdown('<div class="kinetic-subtitle">REGISTERED USERS</div>', unsafe_allow_html=True)
    
    users_data = []
    for u in st.session_state.users_db.keys():
        role = "Admin" if u == "admin" else "Student"
        users_data.append({"Username": u, "Account Role": role})
    
    users_df = pd.DataFrame(users_data)
    
    st.dataframe(
        users_df, 
        hide_index=True, 
        use_container_width=True
    )
