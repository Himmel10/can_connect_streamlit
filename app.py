import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib
import json
import time
from streamlit_option_menu import option_menu
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="CanConnect - Cantilan Digital Government",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern, Clean CSS
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 20px;
        color: white;
        font-size: 2.5em;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .info-box {
        background: rgba(255,255,255,0.95);
        padding: 15px;
        border-left: 4px solid #667eea;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 5px;
    }
    
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
    }
    
    .stButton>button {
        background: #667eea;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: #764ba2;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'submitted_applications' not in st.session_state:
    st.session_state.submitted_applications = []
if 'announcements' not in st.session_state:
    st.session_state.announcements = [
        {"date": "2026-03-14", "title": "New Digital Services Available", "message": "Check out our latest government services."},
        {"date": "2026-03-10", "title": "System Maintenance", "message": "Scheduled maintenance completed successfully."}
    ]

# Helper function for login
def login(username, password):
    # Simple authentication (replace with real authentication in production)
    if username and len(password) >= 6:
        st.session_state.logged_in = True
        st.session_state.user_name = username
        return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.user_name = ""

# ============================================
# SIDEBAR MENU
# ============================================
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: white;'>⚙️ Navigation</h3>", unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.write(f"**Welcome, {st.session_state.user_name}!**")
        
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Apply for Services", "Track Applications", "Pay Bills", "Announcements", "Profile", "Logout"],
            icons=["house", "file-earmark", "clock-history", "credit-card", "megaphone", "person", "box-arrow-right"],
            menu_icon="cast",
            default_index=0
        )
    else:
        selected = option_menu(
            menu_title=None,
            options=["Home", "Login"],
            icons=["house", "box-arrow-in-right"],
            menu_icon="cast",
            default_index=0
        )

# ============================================
# MAIN APP LOGIC
# ============================================

if not st.session_state.logged_in:
    if selected == "Home":
        # Landing Page
        st.markdown("<div class='main-header'>🏛️ CanConnect</div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Cantilan Digital Government Services</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h3>📋 Apply</h3>
                <p>Submit applications online easily</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='metric-card'>
                <h3>📊 Track</h3>
                <p>Monitor your application status</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='metric-card'>
                <h3>💳 Pay</h3>
                <p>Secure online payment system</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.write("### Features")
            st.write("""
            ✅ Quick digital applications  
            ✅ Real-time status tracking  
            ✅ Secure payment processing  
            ✅ Document management  
            ✅ 24/7 online access  
            ✅ Mobile-friendly interface
            """)
        
        with col2:
            st.write("### Contact Us")
            st.write("""
            📍 Cantilan, Philippines  
            📞 (123) 456-7890  
            ✉️ info@canconnect.gov  
            🕐 Mon-Fri: 8AM-5PM
            """)
    
    elif selected == "Login":
        st.markdown("<div class='main-header'>🔐 Login</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.write("")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔓 Login", use_container_width=True):
                    if login(username, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Password must be at least 6 characters.")
            
            with col_btn2:
                if st.button("📝 Register", use_container_width=True):
                    st.info("Registration coming soon!")
            
            st.markdown("---")
            st.write("**Demo Credentials:**")
            st.info("Username: demo | Password: demo123")

else:
    # ============================================
    # LOGGED IN - DASHBOARD
    # ============================================
    
    if selected == "Dashboard":
        st.markdown(f"<div class='main-header'>📊 Dashboard</div>", unsafe_allow_html=True)
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Active Applications", value=len(st.session_state.submitted_applications), delta="2 pending")
        
        with col2:
            st.metric(label="Completed Services", value=12, delta="3 this month")
        
        with col3:
            st.metric(label="Account Status", value="Active", delta="Good standing")
        
        with col4:
            st.metric(label="Balance Due", value="₱0.00", delta="All paid")
        
        st.markdown("---")
        
        # Quick Stats Chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Monthly Applications")
            df = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'Applications': [5, 7, 3, 8, 6, 4]
            })
            fig = px.bar(df, x='Month', y='Applications', color='Applications', 
                        color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("### Service Categories")
            df_pie = pd.DataFrame({
                'Category': ['Permits', 'Licenses', 'Certificates', 'Other'],
                'Count': [8, 5, 4, 3]
            })
            fig_pie = px.pie(df_pie, names='Category', values='Count')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        st.write("### Recent Activity")
        st.info("✅ Certificate of Good Moral Character approved - Mar 10, 2026")
        st.info("⏳ Business Permit application pending - Mar 8, 2026")
        st.info("✅ Barangay Clearance issued - Mar 1, 2026")
    
    elif selected == "Apply for Services":
        st.markdown("<div class='main-header'>📋 Apply for Services</div>", unsafe_allow_html=True)
        
        service_type = st.selectbox("Select Service Type", [
            "Barangay Clearance",
            "Business Permit",
            "Certificate of Good Moral Character",
            "Senior Citizen ID",
            "PWD ID",
            "Marriage Certificate",
            "Birth Certificate"
        ])
        
        st.write(f"### Apply for {service_type}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name")
            date_of_birth = st.date_input("Date of Birth")
            email = st.text_input("Email Address")
        
        with col2:
            last_name = st.text_input("Last Name")
            contact = st.text_input("Contact Number")
            address = st.text_area("Address")
        
        st.write("### Additional Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            purpose = st.text_area("Purpose of Application")
            urgent = st.checkbox("Mark as Urgent (Additional fee: ₱500)")
        
        with col2:
            documents = st.multiselect("Required Documents", [
                "Valid ID (Front & Back)",
                "Proof of Residence",
                "Birth Certificate",
                "Marriage Certificate"
            ])
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("📤 Submit Application", use_container_width=True):
                if all([first_name, last_name, email, contact, address, purpose]):
                    app = {
                        "id": f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "service": service_type,
                        "name": f"{first_name} {last_name}",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "status": "Submitted"
                    }
                    st.session_state.submitted_applications.append(app)
                    st.success(f"✅ Application submitted! Reference: {app['id']}")
                else:
                    st.error("❌ Please fill all required fields")
    
    elif selected == "Track Applications":
        st.markdown("<div class='main-header'>📍 Track Applications</div>", unsafe_allow_html=True)
        
        if st.session_state.submitted_applications:
            for app in st.session_state.submitted_applications:
                with st.container():
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.write(f"**ID:** {app['id']}")
                    with col2:
                        st.write(f"**Service:** {app['service']}")
                    with col3:
                        st.write(f"**Date:** {app['date']}")
                    with col4:
                        if app['status'] == 'Submitted':
                            st.info(f"**Status:** {app['status']}")
                        elif app['status'] == 'Processing':
                            st.warning(f"**Status:** {app['status']}")
                        else:
                            st.success(f"**Status:** {app['status']}")
                
                # Progress tracking
                steps = st.columns(5)
                step_names = ["📝 Submitted", "🔍 Reviewing", "⚙️ Processing", "✅ Approved", "📦 Ready"]
                
                for step_col, step_name in zip(steps, step_names):
                    with step_col:
                        if "Submitted" in step_name or "Reviewing" in step_name:
                            st.write(f"<div style='text-align: center; color: green;'>{step_name}</div>", unsafe_allow_html=True)
                        else:
                            st.write(f"<div style='text-align: center; color: lightgray;'>{step_name}</div>", unsafe_allow_html=True)
                
                st.markdown("---")
        else:
            st.info("📭 No applications yet. Start by applying for a service!")
    
    elif selected == "Pay Bills":
        st.markdown("<div class='main-header'>💳 Pay Bills</div>", unsafe_allow_html=True)
        
        payment_type = st.selectbox("Select Payment Type", [
            "Application Fees",
            "Business Tax",
            "Property Tax",
            "Other Government Fees"
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Payment Details")
            reference = st.text_input("Reference Number")
            amount = st.number_input("Amount (₱)", min_value=0.0, step=100.0)
        
        with col2:
            st.write("### Payment Method")
            payment_method = st.radio("Select method:", [
                "Online Banking",
                "Credit/Debit Card",
                "E-Wallet",
                "Over the Counter"
            ])
        
        st.markdown("---")
        
        if amount > 0:
            st.write(f"**Total Amount:** ₱{amount:,.2f}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💰 Pay Now", use_container_width=True):
                    st.success(f"✅ Payment of ₱{amount:,.2f} processed successfully!")
                    st.balloons()
            
            with col2:
                if st.button("💾 Save for Later", use_container_width=True):
                    st.info("📌 Payment saved to your account")
            
            with col3:
                if st.button("📨 Send Receipt", use_container_width=True):
                    st.info("✉️ Receipt sent to your email")
        else:
            st.warning("⚠️ Please enter an amount to proceed")
    
    elif selected == "Announcements":
        st.markdown("<div class='main-header'>📢 Announcements</div>", unsafe_allow_html=True)
        
        for announcement in st.session_state.announcements:
            st.write(f"#### {announcement['title']}")
            st.write(f"📅 {announcement['date']}")
            st.write(announcement['message'])
            st.markdown("---")
        
        st.write("### Post New Announcement (Admin)")
        new_title = st.text_input("Announcement Title")
        new_message = st.text_area("Message")
        
        if st.button("📤 Post Announcement"):
            if new_title and new_message:
                st.session_state.announcements.insert(0, {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "title": new_title,
                    "message": new_message
                })
                st.success("✅ Announcement posted!")
            else:
                st.error("❌ Please fill all fields")
    
    elif selected == "Profile":
        st.markdown("<div class='main-header'>👤 My Profile</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Personal Information")
            st.text_input("Username", value=st.session_state.user_name, disabled=True)
            new_email = st.text_input("Email")
            new_contact = st.text_input("Contact Number")
            new_address = st.text_area("Address")
        
        with col2:
            st.write("### Account Settings")
            notification = st.checkbox("Email Notifications", value=True)
            language = st.selectbox("Language", ["English", "Tagalog"])
            theme = st.selectbox("Theme", ["Light", "Dark"])
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save Changes", use_container_width=True):
                st.success("✅ Profile updated successfully!")
        
        with col2:
            if st.button("🔐 Change Password", use_container_width=True):
                st.info("Password change email sent!")
    
    elif selected == "Logout":
        st.markdown("<div class='main-header'>👋 Goodbye!</div>", unsafe_allow_html=True)
        st.write("You have been logged out successfully.")
        
        logout()
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white; padding: 20px;'>
    <p>© 2026 CanConnect - Cantilan Digital Government Services</p>
    <p>For support, contact: support@canconnect.gov | (123) 456-7890</p>
</div>
""", unsafe_allow_html=True)
