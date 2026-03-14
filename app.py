import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import hashlib
import json
import time
from streamlit_option_menu import option_menu
import random
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="CanConnect - Cantilan Digital Government Services",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with animations and modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Modern Headers */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeInDown 1s ease;
    }
    
    .sub-header {
        font-size: 2rem;
        font-weight: 600;
        color: #2D3748;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        display: inline-block;
    }
    
    /* Animated Service Cards */
    .service-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        animation: fadeInUp 0.5s ease;
        cursor: pointer;
    }
    
    .service-card:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Status Badges with Animations */
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .status-pending { 
        background: linear-gradient(135deg, #f6b26b, #e69138);
        color: white;
    }
    .status-processing { 
        background: linear-gradient(135deg, #6fa8dc, #3c78d8);
        color: white;
    }
    .status-approved { 
        background: linear-gradient(135deg, #93c47d, #6aa84f);
        color: white;
    }
    .status-rejected { 
        background: linear-gradient(135deg, #e06666, #cc0000);
        color: white;
    }
    
    /* Notification Animations */
    .notification {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        animation: slideInRight 0.5s ease;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Progress Bar Animation */
    .progress-container {
        width: 100%;
        background-color: #f0f0f0;
        border-radius: 10px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 10px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        transition: width 0.5s ease-in-out;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Floating Action Button */
    .fab {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1000;
        animation: bounce 2s infinite;
    }
    
    .fab:hover {
        transform: scale(1.1) rotate(90deg);
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Loading Spinner */
    .loader {
        border: 5px solid #f3f3f3;
        border-top: 5px solid #667eea;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Document Upload Area */
    .upload-area {
        border: 3px dashed #667eea;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        background: rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .upload-area:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: scale(1.02);
    }
    
    /* Statistics Cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeIn 1s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Chat Bubble */
    .chat-bubble {
        background: white;
        border-radius: 20px;
        padding: 1rem;
        margin: 0.5rem 0;
        max-width: 80%;
        animation: fadeIn 0.5s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .chat-bubble.user {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-left: auto;
    }
    
    .chat-bubble.bot {
        background: #f0f0f0;
        color: #333;
    }
    
    /* Timeline */
    .timeline-item {
        display: flex;
        margin: 1rem 0;
        animation: slideInLeft 0.5s ease;
    }
    
    .timeline-dot {
        width: 20px;
        height: 20px;
        background: #667eea;
        border-radius: 50%;
        margin-right: 1rem;
        position: relative;
    }
    
    .timeline-dot::before {
        content: '';
        position: absolute;
        width: 2px;
        height: 50px;
        background: #667eea;
        left: 9px;
        top: 20px;
    }
    
    .timeline-item:last-child .timeline-dot::before {
        display: none;
    }
    
    .timeline-content {
        flex: 1;
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize all session state variables
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'authenticated': False,
        'user_type': None,
        'username': None,
        'language': 'English',
        'applications': [],
        'chat_history': [],
        'notifications': [],
        'favorites': [],
        'drafts': [],
        'documents': [],
        'appointments': [],
        'feedback': [],
        'survey_responses': [],
        'search_history': [],
        'theme': 'light',
        'font_size': 'medium',
        'notifications_enabled': True,
        'email_notifications': True,
        'sms_notifications': True,
        'two_factor_enabled': False,
        'last_login': None,
        'login_attempts': 0,
        'security_questions': [],
        'backup_email': None,
        'backup_phone': None,
        'preferred_payment': None,
        'digital_signature': None,
        'verified_status': 'unverified',
        'verification_documents': [],
        'trusted_devices': [],
        'activity_log': [],
        'saved_searches': [],
        'custom_templates': [],
        'shared_documents': [],
        'delegated_access': [],
        'recurring_applications': [],
        'deadline_reminders': [],
        'priority_alerts': [],
        'service_ratings': {},
        'announcements_read': [],
        'training_progress': {},
        'certifications': [],
        'badges': [],
        'points': 0,
        'level': 1,
        'achievements': [],
        'challenges': [],
        'leaderboard_rank': None,
        'community_posts': [],
        'helpful_votes': 0,
        'expertise_areas': [],
        'mentor_status': False,
        'mentees': [],
        'office_hours': [],
        'appointment_slots': [],
        'department_stats': {},
        'team_members': [],
        'projects': [],
        'tasks': [],
        'calendar_events': [],
        'meeting_notes': [],
        'document_templates': [],
        'report_templates': [],
        'data_exports': [],
        'audit_logs': [],
        'system_backups': [],
        'error_logs': [],
        'performance_metrics': {},
        'user_feedback': [],
        'feature_requests': [],
        'bug_reports': [],
        'system_updates': [],
        'maintenance_schedule': [],
        'security_alerts': [],
        'compliance_checks': [],
        'risk_assessments': [],
        'disaster_recovery_plans': [],
        'business_continuity_plans': [],
        'incident_reports': [],
        'change_requests': [],
        'approval_workflows': [],
        'budget_tracking': {},
        'resource_allocation': {},
        'procurement_requests': [],
        'vendor_management': {},
        'contracts': [],
        'invoices': [],
        'payments': [],
        'reimbursements': [],
        'travel_requests': [],
        'leave_requests': [],
        'overtime_requests': [],
        'attendance_records': [],
        'performance_reviews': [],
        'training_records': [],
        'certification_tracking': {},
        'skill_assessments': [],
        'career_development_plans': [],
        'succession_planning': {},
        'employee_recognition': [],
        'awards': [],
        'disciplinary_actions': [],
        'grievances': [],
        'exit_interviews': [],
        'alumni_tracking': [],
        'volunteer_hours': [],
        'community_engagement': {},
        'outreach_programs': [],
        'event_planning': [],
        'budget_forecasting': {},
        'financial_reports': [],
        'grant_applications': [],
        'donation_tracking': {},
        'sponsorships': [],
        'partnerships': [],
        'moa_tracking': [],
        'project_proposals': [],
        'impact_assessments': [],
        'sustainability_reports': [],
        'annual_reports': [],
        'strategic_plans': [],
        'policy_documents': [],
        'ordinances': [],
        'resolutions': [],
        'legal_documents': [],
        'court_orders': [],
        'permits_issued': [],
        'licenses_granted': [],
        'certificates_awarded': [],
        'violations_recorded': [],
        'complaints_filed': [],
        'resolutions_made': [],
        'appeals_processed': [],
        'hearings_scheduled': [],
        'mediations_conducted': [],
        'arbitrations_handled': [],
        'settlements_reached': [],
        'judgments_rendered': [],
        'enforcement_actions': [],
        'inspections_performed': [],
        'audits_conducted': [],
        'investigations_completed': [],
        'reviews_completed': [],
        'evaluations_completed': [],
        'assessments_completed': [],
        'surveys_completed': [],
        'studies_completed': [],
        'research_completed': [],
        'analysis_completed': [],
        'recommendations_made': [],
        'implementations_completed': [],
        'monitoring_completed': [],
        'reporting_completed': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize session state
init_session_state()

# Language dictionary with more comprehensive translations
translations = {
    'English': {
        'welcome': 'Welcome to CanConnect',
        'subtitle': 'Unified Digital Government Service System for the Municipality of Cantilan',
        'login': 'Login',
        'register': 'Register',
        'username': 'Username',
        'password': 'Password',
        'citizen': 'Citizen',
        'lgu_staff': 'LGU Staff',
        'admin': 'Administrator',
        'services': 'Available Services',
        'my_applications': 'My Applications',
        'new_application': 'New Application',
        'track_application': 'Track Application',
        'chatbot': 'AI Assistant',
        'notifications': 'Notifications',
        'profile': 'Profile',
        'logout': 'Logout',
        'dashboard': 'Dashboard',
        'processing_queue': 'Processing Queue',
        'reports': 'Reports & Analytics',
        'system_admin': 'System Administration',
        'documents': 'My Documents',
        'appointments': 'Appointments',
        'feedback': 'Feedback & Surveys',
        'community': 'Community Forum',
        'learning': 'Learning Center',
        'achievements': 'Achievements',
        'settings': 'Settings',
        'help': 'Help & Support',
        'emergency': 'Emergency Services',
        'announcements': 'Announcements',
        'events': 'Community Events',
        'directory': 'Government Directory',
        'faq': 'FAQ',
        'contact': 'Contact Us',
        'about': 'About CanConnect'
    },
    'Cebuano': {
        'welcome': 'Maayong Pag-abot sa CanConnect',
        'subtitle': 'Unified Digital Government Service System para sa Munisipyo sa Cantilan',
        'login': 'Log-in',
        'register': 'Pag-rehistro',
        'username': 'Ngalan sa Gumagamit',
        'password': 'Password',
        'citizen': 'Lungsuranon',
        'lgu_staff': 'Staff sa LGU',
        'admin': 'Administrator',
        'services': 'Mga Serbisyo',
        'my_applications': 'Akong mga Aplikasyon',
        'new_application': 'Bag-ong Aplikasyon',
        'track_application': 'Subayon ang Aplikasyon',
        'chatbot': 'AI Tabang',
        'notifications': 'Mga Pahibalo',
        'profile': 'Profile',
        'logout': 'Pag-gawas',
        'dashboard': 'Dashboard',
        'processing_queue': 'Queue sa Pagproseso',
        'reports': 'Mga Report ug Analytics',
        'system_admin': 'Pagdumala sa Sistema',
        'documents': 'Akong mga Dokumento',
        'appointments': 'Mga Appointment',
        'feedback': 'Feedback ug Surveys',
        'community': 'Forum sa Komunidad',
        'learning': 'Learning Center',
        'achievements': 'Mga Achievements',
        'settings': 'Settings',
        'help': 'Tabang ug Suporta',
        'emergency': 'Emergency Services',
        'announcements': 'Mga Pahibalo',
        'events': 'Mga Event sa Komunidad',
        'directory': 'Government Directory',
        'faq': 'FAQ',
        'contact': 'Contact Us',
        'about': 'Mahitungod sa CanConnect'
    }
}

def get_text(key):
    """Get translated text based on selected language"""
    return translations[st.session_state.language].get(key, key)

# Enhanced authentication functions
def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password, user_type):
    """Enhanced login with security features"""
    # Simulate database check
    hashed_password = hash_password(password)
    
    # Check for brute force attempts
    if st.session_state.login_attempts >= 5:
        st.error("Too many failed attempts. Please try again in 15 minutes.")
        return False
    
    # Simulate successful login for demo
    st.session_state.authenticated = True
    st.session_state.user_type = user_type
    st.session_state.username = username
    st.session_state.last_login = datetime.now()
    st.session_state.login_attempts = 0
    
    # Log activity
    st.session_state.activity_log.append({
        'timestamp': datetime.now(),
        'action': 'login',
        'details': f'User {username} logged in as {user_type}'
    })
    
    return True

def logout_user():
    """Enhanced logout with activity logging"""
    st.session_state.activity_log.append({
        'timestamp': datetime.now(),
        'action': 'logout',
        'details': f'User {st.session_state.username} logged out'
    })
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.username = None
    st.rerun()

# Enhanced notification system
def add_notification(title, message, type='info', duration=5):
    """Add a notification with animation"""
    notification = {
        'id': len(st.session_state.notifications),
        'title': title,
        'message': message,
        'type': type,
        'timestamp': datetime.now(),
        'read': False,
        'duration': duration
    }
    st.session_state.notifications.insert(0, notification)
    return notification

def get_unread_notifications():
    """Get unread notifications count"""
    return len([n for n in st.session_state.notifications if not n['read']])

# Sidebar with enhanced navigation
with st.sidebar:
    # Animated logo and title
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <div style='font-size: 3rem; animation: bounce 2s infinite;'>🏛️</div>
        <h2 style='color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>CanConnect</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selector with icons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇬🇧 EN", use_container_width=True):
            st.session_state.language = 'English'
            st.rerun()
    with col2:
        if st.button("🇵🇭 CEB", use_container_width=True):
            st.session_state.language = 'Cebuano'
            st.rerun()
    
    if not st.session_state.authenticated:
        # Animated login/register cards
        st.markdown("""
        <div class='glass-card' style='padding: 1.5rem;'>
            <h3 style='color: white; text-align: center;'>🔐 Access Government Services</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        # User profile card with animation
        st.markdown(f"""
        <div class='glass-card' style='padding: 1rem; margin-bottom: 1rem;'>
            <div style='display: flex; align-items: center; gap: 1rem;'>
                <div style='font-size: 3rem; animation: pulse 2s infinite;'>👤</div>
                <div>
                    <h4 style='color: white; margin: 0;'>{st.session_state.username}</h4>
                    <p style='color: rgba(255,255,255,0.8); margin: 0;'>{st.session_state.user_type}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Notification bell with counter
        unread_count = get_unread_notifications()
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("🔔", help="Notifications"):
                st.session_state.selected = get_text('notifications')
        with col3:
            if unread_count > 0:
                st.markdown(f"""
                <div style='background: #ff4444; color: white; border-radius: 50%; 
                          width: 20px; height: 20px; text-align: center; font-size: 12px;
                          animation: pulse 1s infinite;'>
                    {unread_count}
                </div>
                """, unsafe_allow_html=True)
        
        # Enhanced navigation based on user type
        if st.session_state.user_type == get_text('citizen'):
            selected = option_menu(
                menu_title=None,
                options=[
                    get_text('dashboard'),
                    get_text('services'),
                    get_text('new_application'),
                    get_text('my_applications'),
                    get_text('track_application'),
                    get_text('documents'),
                    get_text('appointments'),
                    get_text('chatbot'),
                    get_text('community'),
                    get_text('learning'),
                    get_text('achievements'),
                    get_text('feedback'),
                    get_text('notifications'),
                    get_text('profile'),
                    get_text('settings'),
                    get_text('help'),
                    get_text('logout')
                ],
                icons=['house', 'grid', 'plus-circle', 'list', 'search', 'file-text', 
                      'calendar', 'robot', 'people', 'book', 'trophy', 'star', 
                      'bell', 'person', 'gear', 'question-circle', 'box-arrow-right'],
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {"color": "white", "font-size": "14px", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"background-color": "rgba(255, 255, 255, 0.2)", "color": "white"}
                }
            )
        elif st.session_state.user_type == get_text('lgu_staff'):
            selected = option_menu(
                menu_title=None,
                options=[
                    get_text('dashboard'),
                    get_text('processing_queue'),
                    get_text('reports'),
                    get_text('documents'),
                    get_text('appointments'),
                    get_text('community'),
                    get_text('learning'),
                    get_text('achievements'),
                    get_text('feedback'),
                    get_text('notifications'),
                    get_text('profile'),
                    get_text('settings'),
                    get_text('help'),
                    get_text('logout')
                ],
                icons=['house', 'list-check', 'graph-up', 'file-text', 'calendar',
                      'people', 'book', 'trophy', 'star', 'bell', 'person', 
                      'gear', 'question-circle', 'box-arrow-right'],
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {"color": "white", "font-size": "14px", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"background-color": "rgba(255, 255, 255, 0.2)", "color": "white"}
                }
            )
        else:  # Admin
            selected = option_menu(
                menu_title=None,
                options=[
                    get_text('dashboard'),
                    get_text('processing_queue'),
                    get_text('reports'),
                    get_text('system_admin'),
                    get_text('documents'),
                    get_text('community'),
                    get_text('learning'),
                    get_text('feedback'),
                    get_text('notifications'),
                    get_text('profile'),
                    get_text('settings'),
                    get_text('help'),
                    get_text('logout')
                ],
                icons=['house', 'list-check', 'graph-up', 'gear', 'file-text',
                      'people', 'book', 'star', 'bell', 'person', 'gear', 
                      'question-circle', 'box-arrow-right'],
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {"color": "white", "font-size": "14px", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"background-color": "rgba(255, 255, 255, 0.2)", "color": "white"}
                }
            )
        
        if selected == get_text('logout'):
            logout_user()

# Main content area
if not st.session_state.authenticated:
    # Enhanced login/register page with animations
    st.markdown(f"<h1 class='main-header'>🏛️ {get_text('welcome')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: white; font-size: 1.2rem; animation: fadeInUp 1s ease;'>{get_text('subtitle')}</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Animated tabs
        tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "🆘 Emergency Access"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown("### Welcome Back! 👋")
                username = st.text_input(get_text('username'), placeholder="Enter your username")
                password = st.text_input(get_text('password'), type="password", placeholder="Enter your password")
                
                col1, col2 = st.columns(2)
                with col1:
                    user_type = st.selectbox(
                        "Login as",
                        [get_text('citizen'), get_text('lgu_staff'), get_text('admin')]
                    )
                with col2:
                    remember_me = st.checkbox("Remember me")
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    submitted = st.form_submit_button(
                        f"🔓 {get_text('login')}", 
                        use_container_width=True,
                        type="primary"
                    )
                
                if submitted:
                    with st.spinner("Authenticating..."):
                        time.sleep(1)  # Simulate loading
                        if login_user(username, password, user_type):
                            add_notification(
                                "Welcome Back! 👋",
                                f"Successfully logged in as {user_type}",
                                "success"
                            )
                            st.success("Login successful!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                
                st.markdown("---")
                st.markdown("""
                <div style='text-align: center;'>
                    <a href='#' style='color: white;'>Forgot Password?</a>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            with st.form("register_form"):
                st.markdown("### Join CanConnect Today! 🎉")
                
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    birth_date = st.date_input("Birth Date", min_value=datetime(1900, 1, 1))
                    
                with col2:
                    middle_name = st.text_input("Middle Name")
                    suffix = st.text_input("Suffix (Jr., III, etc.)")
                    
                address = st.text_area("Complete Address")
                
                col1, col2 = st.columns(2)
                with col1:
                    contact = st.text_input("Contact Number")
                    email = st.text_input("Email")
                    
                with col2:
                    alternate_contact = st.text_input("Alternate Contact")
                    alternate_email = st.text_input("Alternate Email")
                
                st.markdown("### Account Security")
                username = st.text_input("Desired Username")
                
                col1, col2 = st.columns(2)
                with col1:
                    password = st.text_input("Password", type="password")
                with col2:
                    confirm_password = st.text_input("Confirm Password", type="password")
                
                st.markdown("### Security Questions")
                security_q1 = st.selectbox(
                    "Security Question 1",
                    ["What was your first pet's name?", "What is your mother's maiden name?", 
                     "What was your first school?", "What is your favorite book?"]
                )
                security_a1 = st.text_input("Answer 1", type="password")
                
                security_q2 = st.selectbox(
                    "Security Question 2",
                    ["What city were you born in?", "What is your favorite movie?", 
                     "What was your childhood nickname?", "What is your dream job?"]
                )
                security_a2 = st.text_input("Answer 2", type="password")
                
                st.markdown("### Terms and Conditions")
                agree_terms = st.checkbox("I agree to the Terms and Conditions")
                agree_privacy = st.checkbox("I agree to the Privacy Policy")
                agree_data = st.checkbox("I consent to data processing")
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    submitted = st.form_submit_button(
                        "📝 Register Account", 
                        use_container_width=True,
                        type="primary"
                    )
                
                if submitted:
                    if password != confirm_password:
                        st.error("Passwords do not match")
                    elif not agree_terms or not agree_privacy or not agree_data:
                        st.error("Please agree to all terms and conditions")
                    else:
                        with st.spinner("Creating your account..."):
                            time.sleep(2)
                            add_notification(
                                "Welcome to CanConnect! 🎉",
                                "Your account has been created successfully. Please check your email for verification.",
                                "success"
                            )
                            st.success("Registration successful! Please check your email to verify your account.")
        
        with tab3:
            st.markdown("""
            <div class='glass-card' style='text-align: center;'>
                <h3 style='color: white;'>🚨 Emergency Services Access</h3>
                <p style='color: white;'>For urgent government services and assistance</p>
                <div style='font-size: 4rem; animation: pulse 1s infinite;'>🚑</div>
                <h2 style='color: #ff4444;'>Emergency Hotline: 911</h2>
                <p style='color: white;'>Or text: CANNECT to 2929</p>
            </div>
            """, unsafe_allow_html=True)

else:
    # Enhanced main content based on selection
    if selected == get_text('dashboard'):
        st.markdown(f"<h1 class='main-header'>📊 {get_text('dashboard')}</h1>", unsafe_allow_html=True)
        
        if st.session_state.user_type == get_text('citizen'):
            # Statistics cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class='stat-card'>
                    <div style='font-size: 2rem;'>📋</div>
                    <div class='stat-number'>3</div>
                    <div class='stat-label'>Active Applications</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                <div class='stat-card'>
                    <div style='font-size: 2rem;'>✅</div>
                    <div class='stat-number'>5</div>
                    <div class='stat-label'>Completed</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown("""
                <div class='stat-card'>
                    <div style='font-size: 2rem;'>⏳</div>
                    <div class='stat-number'>2</div>
                    <div class='stat-label'>Pending</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col4:
                st.markdown("""
                <div class='stat-card'>
                    <div style='font-size: 2rem;'>🔔</div>
                    <div class='stat-number'>4</div>
                    <div class='stat-label'>Notifications</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Recent activity timeline
            st.markdown(f"<h2 class='sub-header'>📅 Recent Activity</h2>", unsafe_allow_html=True)
            
            activities = [
                {"date": "2025-03-14", "time": "09:30 AM", "service": "Business Permit", "status": "Processing", "ref": "BP-2025-001"},
                {"date": "2025-03-13", "time": "02:15 PM", "service": "Barangay Clearance", "status": "Approved", "ref": "BC-2025-089"},
                {"date": "2025-03-12", "time": "10:00 AM", "service": "Health Appointment", "status": "Confirmed", "ref": "HA-2025-045"},
                {"date": "2025-03-11", "time": "11:30 AM", "service": "Police Clearance", "status": "Ready for Release", "ref": "PC-2025-123"}
            ]
            
            for activity in activities:
                status_class = {
                    'Processing': 'status-processing',
                    'Approved': 'status-approved',
                    'Confirmed': 'status-approved',
                    'Ready for Release': 'status-processing'
                }.get(activity['status'], 'status-pending')
                
                st.markdown(f"""
                <div class='timeline-item'>
                    <div class='timeline-dot'></div>
                    <div class='timeline-content'>
                        <div style='display: flex; justify-content: space-between;'>
                            <strong>{activity['service']}</strong>
                            <span>{activity['date']} {activity['time']}</span>
                        </div>
                        <p>Reference: {activity['ref']}</p>
                        <span class='status-badge {status_class}'>{activity['status']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Quick actions
            st.markdown(f"<h2 class='sub-header'>⚡ Quick Actions</h2>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📝 New Application", use_container_width=True):
                    st.session_state.selected = get_text('new_application')
                    st.rerun()
                    
            with col2:
                if st.button("🔍 Track Application", use_container_width=True):
                    st.session_state.selected = get_text('track_application')
                    st.rerun()
                    
            with col3:
                if st.button("📅 Schedule Appointment", use_container_width=True):
                    st.session_state.selected = get_text('appointments')
                    st.rerun()
                    
            with col4:
                if st.button("💬 Chat with AI", use_container_width=True):
                    st.session_state.selected = get_text('chatbot')
                    st.rerun()
            
        elif st.session_state.user_type == get_text('lgu_staff'):
            # Staff dashboard
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class='stat-card'>
                    <div style='font-size: 2rem;'>📥</div>
                    <div class='stat-number'>12</div>
                    <div class='stat-label'>Pending</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                <div class='stat-card'>
                    <div style='font-size: 2rem;'>⚙️</div>
                    <div class='stat-number'>8</div>
                    <div class='stat-label'>Processing</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown("""
                <div class='stat-card'>
                    <div style='font-size: 2rem;'>✅</div>
                    <div class='stat-number'>15</div>
                    <div class='stat-label'>Completed Today</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col4:
                st.markdown("""
                <div class='stat-card'>
                    <div style='font-size: 2rem;'>⏱️</div>
                    <div class='stat-number'>2.5</div>
                    <div class='stat-label'>Avg. Days</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Performance metrics
            st.markdown(f"<h2 class='sub-header'>📊 Performance Metrics</h2>", unsafe_allow_html=True)
            
            # Create gauge charts for performance
            fig = make_subplots(
                rows=1, cols=3,
                specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]]
            )
            
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=85,
                title={'text': "Efficiency Rate"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': "#667eea"}}
            ), row=1, col=1)
            
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=92,
                title={'text': "Accuracy Rate"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': "#764ba2"}}
            ), row=1, col=2)
            
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=78,
                title={'text': "Customer Satisfaction"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': "#23a6d5"}}
            ), row=1, col=3)
            
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Priority queue
            st.markdown(f"<h2 class='sub-header'>⚠️ Priority Queue</h2>", unsafe_allow_html=True)
            
            priority_items = [
                {"priority": "HIGH", "application": "Business Permit - Juan Dela Cruz", "waiting": "5 days", "action": "Urgent"},
                {"priority": "MEDIUM", "application": "Barangay Clearance - Maria Santos", "waiting": "2 days", "action": "Review"},
                {"priority": "HIGH", "application": "Medical Appointment - Pedro Reyes", "waiting": "1 day", "action": "Schedule"},
                {"priority": "LOW", "application": "Police Clearance - Ana Lim", "waiting": "3 days", "action": "Process"}
            ]
            
            for item in priority_items:
                color = "#ff4444" if item['priority'] == "HIGH" else "#ffaa00" if item['priority'] == "MEDIUM" else "#00C851"
                st.markdown(f"""
                <div class='service-card' style='border-left-color: {color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <span style='background: {color}; color: white; padding: 0.25rem 0.5rem; 
                                       border-radius: 5px; font-size: 0.8rem;'>{item['priority']}</span>
                            <h4 style='margin: 0.5rem 0;'>{item['application']}</h4>
                            <p>Waiting: {item['waiting']}</p>
                        </div>
                        <button style='background: {color}; color: white; border: none; 
                                     padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;'>
                            {item['action']}
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    elif selected == get_text('services'):
        st.markdown(f"<h1 class='main-header'>📋 {get_text('services')}</h1>", unsafe_allow_html=True)
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("🔍 Search services...", placeholder="Enter service name or keyword")
        with col2:
            category_filter = st.multiselect("Filter by", ["Business", "Health", "Civil Registry", "Clearances"])
        
        # Services grid
        services = [
            {
                "name": "Business Permit",
                "category": "Business",
                "description": "Apply for new or renewal of business permit",
                "requirements": ["Business name registration", "Barangay clearance", "Valid ID"],
                "processing_time": "3-5 working days",
                "fee": "Variable",
                "popular": True,
                "online": True,
                "icon": "🏢"
            },
            {
                "name": "Barangay Clearance",
                "category": "Clearances",
                "description": "Request for barangay clearance certificate",
                "requirements": ["Valid ID", "Proof of residency"],
                "processing_time": "1 working day",
                "fee": "₱50.00",
                "popular": True,
                "online": True,
                "icon": "📄"
            },
            {
                "name": "Police Clearance",
                "category": "Clearances",
                "description": "Apply for police clearance certificate",
                "requirements": ["Valid ID", "Barangay clearance"],
                "processing_time": "1-2 working days",
                "fee": "₱100.00",
                "popular": True,
                "online": True,
                "icon": "👮"
            },
            {
                "name": "Health Office Appointment",
                "category": "Health",
                "description": "Schedule medical/dental appointments",
                "requirements": ["Valid ID", "Medical history (if any)"],
                "processing_time": "Same day",
                "fee": "Free",
                "popular": False,
                "online": True,
                "icon": "🏥"
            },
            {
                "name": "Birth Certificate",
                "category": "Civil Registry",
                "description": "Request for certified copy of birth certificate",
                "requirements": ["Valid ID", "Request form"],
                "processing_time": "2-3 working days",
                "fee": "₱75.00",
                "popular": True,
                "online": True,
                "icon": "👶"
            },
            {
                "name": "Marriage Certificate",
                "category": "Civil Registry",
                "description": "Request for certified copy of marriage certificate",
                "requirements": ["Valid ID", "Request form"],
                "processing_time": "2-3 working days",
                "fee": "₱75.00",
                "popular": False,
                "online": True,
                "icon": "💑"
            },
            {
                "name": "Death Certificate",
                "category": "Civil Registry",
                "description": "Request for certified copy of death certificate",
                "requirements": ["Valid ID of requester", "Death details"],
                "processing_time": "2-3 working days",
                "fee": "₱75.00",
                "popular": False,
                "online": True,
                "icon": "🕊️"
            },
            {
                "name": "Building Permit",
                "category": "Business",
                "description": "Apply for construction or renovation permit",
                "requirements": ["Property title", "Construction plans", "Barangay clearance"],
                "processing_time": "7-10 working days",
                "fee": "Variable",
                "popular": False,
                "online": True,
                "icon": "🏗️"
            },
            {
                "name": "Senior Citizen ID",
                "category": "Civil Registry",
                "description": "Apply for senior citizen identification card",
                "requirements": ["Valid ID", "Birth certificate", "Barangay certification"],
                "processing_time": "3-5 working days",
                "fee": "Free",
                "popular": True,
                "online": True,
                "icon": "👴"
            },
            {
                "name": "PWD ID",
                "category": "Civil Registry",
                "description": "Apply for Persons with Disability ID",
                "requirements": ["Medical certificate", "Valid ID", "Barangay certification"],
                "processing_time": "3-5 working days",
                "fee": "Free",
                "popular": False,
                "online": True,
                "icon": "♿"
            },
            {
                "name": "Solo Parent ID",
                "category": "Civil Registry",
                "description": "Apply for solo parent identification card",
                "requirements": ["Proof of solo parent status", "Valid ID", "Barangay certification"],
                "processing_time": "3-5 working days",
                "fee": "Free",
                "popular": False,
                "online": True,
                "icon": "👪"
            },
            {
                "name": "Zoning Clearance",
                "category": "Business",
                "description": "Apply for zoning compliance certificate",
                "requirements": ["Property title", "Location map", "Barangay clearance"],
                "processing_time": "5-7 working days",
                "fee": "Variable",
                "popular": False,
                "online": True,
                "icon": "🗺️"
            }
        ]
        
        # Filter services based on search
        if search_query:
            services = [s for s in services if search_query.lower() in s['name'].lower() or 
                       search_query.lower() in s['description'].lower()]
        
        if category_filter:
            services = [s for s in services if s['category'] in category_filter]
        
        # Display services in grid
        cols = st.columns(3)
        for idx, service in enumerate(services):
            with cols[idx % 3]:
                popular_badge = "⭐ POPULAR" if service['popular'] else ""
                online_badge = "✅ Online" if service['online'] else "🏢 Walk-in"
                
                st.markdown(f"""
                <div class='service-card' onclick="alert('Selected: {service['name']}')">
                    <div style='font-size: 2rem; text-align: center;'>{service['icon']}</div>
                    <h3 style='text-align: center; margin: 0.5rem 0;'>{service['name']}</h3>
                    <div style='display: flex; justify-content: center; gap: 0.5rem; margin: 0.5rem 0;'>
                        <span style='background: #667eea; color: white; padding: 0.25rem 0.5rem; 
                                   border-radius: 5px; font-size: 0.8rem;'>{service['category']}</span>
                        <span style='background: #28a745; color: white; padding: 0.25rem 0.5rem; 
                                   border-radius: 5px; font-size: 0.8rem;'>{online_badge}</span>
                    </div>
                    <p style='color: #666;'>{service['description']}</p>
                    <p><strong>Processing:</strong> {service['processing_time']}</p>
                    <p><strong>Fee:</strong> {service['fee']}</p>
                    <div style='text-align: center; margin-top: 1rem;'>
                        <button style='background: linear-gradient(135deg, #667eea, #764ba2); 
                                     color: white; border: none; padding: 0.5rem 1rem; 
                                     border-radius: 5px; cursor: pointer; width: 100%;'>
                            Apply Now →
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    elif selected == get_text('new_application'):
        st.markdown(f"<h1 class='main-header'>📝 {get_text('new_application')}</h1>", unsafe_allow_html=True)
        
        # Multi-step form
        steps = ["Service Selection", "Personal Information", "Document Upload", "Review & Submit"]
        current_step = st.session_state.get('form_step', 0)
        
        # Progress bar
        progress = (current_step + 1) / len(steps)
        st.markdown(f"""
        <div class='progress-container'>
            <div class='progress-bar' style='width: {progress * 100}%;'></div>
        </div>
        <div style='display: flex; justify-content: space-between; margin-bottom: 2rem;'>
            {"".join([f"<span style='color: {'#667eea' if i <= current_step else '#999'};'>{s}</span>" for i, s in enumerate(steps)])}
        </div>
        """, unsafe_allow_html=True)
        
        if current_step == 0:
            st.markdown("### Step 1: Select Service")
            
            service_type = st.selectbox(
                "Choose Service Type",
                ["Business Permit", "Barangay Clearance", "Police Clearance", 
                 "Health Office Appointment", "Birth Certificate", "Marriage Certificate",
                 "Death Certificate", "Building Permit", "Senior Citizen ID", 
                 "PWD ID", "Solo Parent ID", "Zoning Clearance"]
            )
            
            # Service-specific information
            if service_type == "Business Permit":
                st.info("💡 Business permits require barangay clearance and valid IDs")
                business_type = st.selectbox("Business Type", ["Sole Proprietorship", "Partnership", "Corporation", "Cooperative"])
                business_name = st.text_input("Business Name")
                capital = st.number_input("Capital Amount (₱)", min_value=0, step=1000)
                
            elif service_type == "Barangay Clearance":
                st.info("💡 Barangay clearance is often required for other applications")
                years_residing = st.number_input("Years residing in barangay", min_value=0)
                
            elif service_type == "Police Clearance":
                st.info("💡 Police clearance requires barangay clearance first")
                purpose = st.selectbox("Purpose", ["Employment", "Travel", "School Requirement", "Others"])
                
            if st.button("Next →", type="primary"):
                st.session_state.form_step = 1
                st.rerun()
                
        elif current_step == 1:
            st.markdown("### Step 2: Personal Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                birth_date = st.date_input("Birth Date", min_value=datetime(1900, 1, 1))
                gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
                
            with col2:
                middle_name = st.text_input("Middle Name")
                suffix = st.text_input("Suffix (Jr., III, etc.)")
                birth_place = st.text_input("Birth Place")
                civil_status = st.selectbox("Civil Status", ["Single", "Married", "Widowed", "Separated"])
            
            address = st.text_area("Complete Address")
            
            col1, col2 = st.columns(2)
            with col1:
                contact = st.text_input("Contact Number")
                email = st.text_input("Email")
                
            with col2:
                alternate_contact = st.text_input("Alternate Contact")
                alternate_email = st.text_input("Alternate Email")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("← Back"):
                    st.session_state.form_step = 0
                    st.rerun()
            with col2:
                if st.button("Next →", type="primary"):
                    st.session_state.form_step = 2
                    st.rerun()
                    
        elif current_step == 2:
            st.markdown("### Step 3: Document Upload")
            
            st.markdown("""
            <div class='upload-area'>
                <div style='font-size: 3rem;'>📎</div>
                <h3>Drag and drop files here</h3>
                <p>or click to browse</p>
                <p style='font-size: 0.8rem; color: #666;'>Supported formats: PDF, PNG, JPG, JPEG (Max 10MB each)</p>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_files = st.file_uploader(
                "Upload supporting documents",
                accept_multiple_files=True,
                type=['pdf', 'png', 'jpg', 'jpeg'],
                key="doc_upload"
            )
            
            if uploaded_files:
                st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")
                
                # Document checklist
                st.markdown("### Required Documents Checklist")
                docs_required = ["Valid ID", "Barangay Clearance", "Proof of Residency"]
                
                for doc in docs_required:
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        uploaded = st.checkbox("", key=f"doc_{doc}")
                    with col2:
                        st.write(doc)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("← Back"):
                    st.session_state.form_step = 1
                    st.rerun()
            with col2:
                if st.button("Next →", type="primary"):
                    st.session_state.form_step = 3
                    st.rerun()
                    
        elif current_step == 3:
            st.markdown("### Step 4: Review & Submit")
            
            # Summary card
            st.markdown("""
            <div class='glass-card'>
                <h3>Application Summary</h3>
                <table style='width: 100%;'>
                    <tr>
                        <td><strong>Service:</strong></td>
                        <td>Business Permit</td>
                    </tr>
                    <tr>
                        <td><strong>Applicant:</strong></td>
                        <td>Juan Dela Cruz</td>
                    </tr>
                    <tr>
                        <td><strong>Documents:</strong></td>
                        <td>3 files uploaded</td>
                    </tr>
                    <tr>
                        <td><strong>Fee:</strong></td>
                        <td>₱500.00</td>
                    </tr>
                    <tr>
                        <td><strong>Processing Time:</strong></td>
                        <td>3-5 working days</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            # Terms agreement
            agree = st.checkbox("I certify that all information provided is true and correct")
            receive_updates = st.checkbox("I want to receive updates via SMS and email")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("← Back"):
                    st.session_state.form_step = 2
                    st.rerun()
            with col2:
                if st.button("📝 Submit Application", type="primary", disabled=not agree):
                    with st.spinner("Submitting application..."):
                        time.sleep(2)
                        ref_no = f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                        add_notification(
                            "Application Submitted! 🎉",
                            f"Your reference number is {ref_no}. We'll notify you of updates.",
                            "success"
                        )
                        st.balloons()
                        st.success(f"Application submitted successfully! Reference number: {ref_no}")
                        st.session_state.form_step = 0
                        time.sleep(3)
                        st.rerun()
    
    elif selected == get_text('chatbot'):
        st.markdown(f"<h1 class='main-header'>🤖 {get_text('chatbot')}</h1>", unsafe_allow_html=True)
        
        # Chat interface
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class='chat-bubble user'>
                        <strong>You:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='chat-bubble bot'>
                        <strong>AI Assistant:</strong> {message['content']}
                        <div style='font-size: 0.8rem; color: #666; margin-top: 0.5rem;'>
                            {message.get('timestamp', 'Just now')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Quick questions
        st.markdown("### Quick Questions")
        col1, col2, col3, col4 = st.columns(4)
        
        quick_questions = [
            "What are the requirements for Business Permit?",
            "How do I track my application?",
            "What are the office hours?",
            "How much are the fees?"
        ]
        
        for i, q in enumerate(quick_questions):
            with [col1, col2, col3, col4][i]:
                if st.button(q, use_container_width=True):
                    st.session_state.chat_history.append({
                        'role': 'user', 
                        'content': q,
                        'timestamp': datetime.now().strftime("%H:%M")
                    })
                    
                    # Simulate AI response
                    responses = {
                        "Business Permit": "For a Business Permit, you'll need: 1) Business name registration, 2) Barangay clearance, 3) Valid ID, and 4) Proof of business address. The fee varies based on your capital.",
                        "track": "You can track your application by going to the 'Track Application' section and entering your reference number, or by texting your reference number to 2929.",
                        "hours": "Our office hours are Monday to Friday, 8:00 AM to 5:00 PM. We're closed on weekends and holidays.",
                        "fees": "Fees vary by service: Barangay Clearance (₱50), Police Clearance (₱100), Birth Certificate (₱75). Business permits are based on capital amount."
                    }
                    
                    response = "I'm here to help! Please ask me about our services, requirements, or application process."
                    for key in responses:
                        if key.lower() in q.lower():
                            response = responses[key]
                            break
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response,
                        'timestamp': datetime.now().strftime("%H:%M")
                    })
                    st.rerun()
        
        # Chat input
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("Type your question here...", key="chat_input", 
                                      placeholder="Ask about services, requirements, or application status...")
        with col2:
            send = st.button("📤 Send", type="primary", use_container_width=True)
        
        if send and user_input:
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now().strftime("%H:%M")
            })
            
            # Enhanced AI response logic
            responses = {
                "hello": "Hello! How can I help you with government services today?",
                "hi": "Hi there! What would you like to know about our services?",
                "requirement": "Document requirements vary by service. Which specific service are you interested in?",
                "status": "You can check your application status by providing your reference number in the Track Application section.",
                "fee": "Service fees are based on LGU rates. Most clearances are ₱50-100, while permits vary.",
                "time": "Processing times: Barangay clearance (1 day), Police clearance (1-2 days), Business permit (3-5 days).",
                "location": "Our office is located at the Municipal Hall, Poblacion, Cantilan, Surigao del Sur.",
                "contact": "You can reach us at (086) 123-4567 or email canconnect@cantilan.gov.ph",
                "emergency": "For emergencies, please call 911 or text CANNECT to 2929 for urgent assistance."
            }
            
            response = "I understand you're asking about our services. Could you please be more specific? I can help with requirements, fees, processing times, and more."
            for key in responses:
                if key in user_input.lower():
                    response = responses[key]
                    break
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    elif selected == get_text('notifications'):
        st.markdown(f"<h1 class='main-header'>🔔 {get_text('notifications')}</h1>", unsafe_allow_html=True)
        
        # Notification controls
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("Mark All as Read", use_container_width=True):
                for n in st.session_state.notifications:
                    n['read'] = True
                st.rerun()
        with col3:
            if st.button("Clear All", use_container_width=True):
                st.session_state.notifications = []
                st.rerun()
        
        # Display notifications
        if st.session_state.notifications:
            for notification in st.session_state.notifications:
                icon = {
                    'info': 'ℹ️',
                    'success': '✅',
                    'warning': '⚠️',
                    'error': '❌'
                }.get(notification['type'], 'ℹ️')
                
                bg_color = {
                    'info': '#e3f2fd',
                    'success': '#e8f5e8',
                    'warning': '#fff3e0',
                    'error': '#ffebee'
                }.get(notification['type'], '#f5f5f5')
                
                st.markdown(f"""
                <div class='notification' style='background: {bg_color}; opacity: {1 if not notification['read'] else 0.7};'>
                    <div style='display: flex; justify-content: space-between;'>
                        <div>
                            <strong>{icon} {notification['title']}</strong>
                            <p>{notification['message']}</p>
                            <small>{notification['timestamp'].strftime('%Y-%m-%d %H:%M')}</small>
                        </div>
                        <div>
                            <button onclick="alert('Mark as read')" style='background: none; border: none; cursor: pointer;'>✓</button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No notifications to display")
    
    elif selected == get_text('documents'):
        st.markdown(f"<h1 class='main-header'>📁 {get_text('documents')}</h1>", unsafe_allow_html=True)
        
        # Document management
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### My Documents")
            
            # Document categories
            categories = ["All", "IDs", "Certificates", "Permits", "Others"]
            selected_category = st.radio("Category", categories, horizontal=True)
            
            # Sample documents
            documents = [
                {"name": "Valid ID - Passport", "type": "ID", "date": "2025-01-15", "size": "2.3 MB"},
                {"name": "Birth Certificate", "type": "Certificate", "date": "2025-02-20", "size": "1.1 MB"},
                {"name": "Barangay Clearance", "type": "Certificate", "date": "2025-03-01", "size": "0.5 MB"},
                {"name": "Business Permit", "type": "Permit", "date": "2025-03-10", "size": "1.8 MB"},
                {"name": "Proof of Residency", "type": "Others", "date": "2025-02-28", "size": "0.3 MB"}
            ]
            
            if selected_category != "All":
                documents = [d for d in documents if d['type'] == selected_category]
            
            for doc in documents:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"📄 {doc['name']}")
                with col2:
                    st.write(doc['date'])
                with col3:
                    st.write(doc['size'])
                with col4:
                    st.button("📥", key=f"download_{doc['name']}")
        
        with col2:
            st.markdown("### Quick Actions")
            
            if st.button("📤 Upload New Document", use_container_width=True):
                st.info("Upload feature coming soon")
            
            if st.button("📁 Create Folder", use_container_width=True):
                st.info("Create folder feature coming soon")
            
            if st.button("🔍 Search Documents", use_container_width=True):
                st.info("Search feature coming soon")
            
            # Storage usage
            st.markdown("### Storage Usage")
            storage_used = 5.2  # GB
            storage_total = 10  # GB
            storage_percent = (storage_used / storage_total) * 100
            
            st.markdown(f"""
            <div class='progress-container'>
                <div class='progress-bar' style='width: {storage_percent}%;'></div>
            </div>
            <p>{storage_used} GB of {storage_total} GB used</p>
            """, unsafe_allow_html=True)
    
    elif selected == get_text('appointments'):
        st.markdown(f"<h1 class='main-header'>📅 {get_text('appointments')}</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Schedule an Appointment")
            
            with st.form("appointment_form"):
                service = st.selectbox(
                    "Select Service",
                    ["Health Office", "Business Permit Processing", "Civil Registry", 
                     "Mayor's Office", "Treasurer's Office", "Assessor's Office"]
                )
                
                purpose = st.text_area("Purpose of Appointment")
                
                col1, col2 = st.columns(2)
                with col1:
                    date = st.date_input("Preferred Date", min_value=datetime.now().date())
                with col2:
                    time = st.time_input("Preferred Time")
                
                st.markdown("### Available Slots")
                slots = ["9:00 AM", "10:00 AM", "11:00 AM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"]
                selected_slot = st.selectbox("Choose Available Slot", slots)
                
                if st.form_submit_button("📅 Schedule Appointment", type="primary"):
                    st.session_state.appointments.append({
                        'service': service,
                        'date': date,
                        'time': selected_slot,
                        'purpose': purpose,
                        'status': 'Confirmed'
                    })
                    add_notification(
                        "Appointment Confirmed! ✅",
                        f"Your appointment for {service} on {date} at {selected_slot} has been scheduled.",
                        "success"
                    )
                    st.success("Appointment scheduled successfully!")
        
        with col2:
            st.markdown("### Upcoming Appointments")
            
            if st.session_state.appointments:
                for app in st.session_state.appointments:
                    st.markdown(f"""
                    <div class='service-card'>
                        <h4>{app['service']}</h4>
                        <p><strong>Date:</strong> {app['date']}</p>
                        <p><strong>Time:</strong> {app['time']}</p>
                        <p><strong>Status:</strong> {app['status']}</p>
                        <button style='background: #ff4444; color: white; border: none; 
                                     padding: 0.25rem 0.5rem; border-radius: 5px;'>
                            Cancel
                        </button>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No upcoming appointments")
    
    elif selected == get_text('community'):
        st.markdown(f"<h1 class='main-header'>👥 {get_text('community')}</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Community Forum")
            
            # Post creation
            with st.expander("Create New Post"):
                post_title = st.text_input("Post Title")
                post_content = st.text_area("Post Content")
                post_category = st.selectbox("Category", ["Question", "Suggestion", "Announcement", "Discussion"])
                
                if st.button("📝 Post", type="primary"):
                    st.success("Post created successfully!")
            
            # Sample posts
            posts = [
                {"user": "Maria S.", "title": "Business Permit Processing Time", 
                 "content": "Has anyone applied for business permit recently? How long did it take?",
                 "likes": 15, "comments": 5, "time": "2 hours ago"},
                {"user": "Juan D.", "title": "New Online Service Feature", 
                 "content": "I love the new tracking feature! Very helpful.",
                 "likes": 23, "comments": 8, "time": "5 hours ago"},
                {"user": "LGU_Official", "title": "Municipal Hall Holiday Schedule", 
                 "content": "Please be advised that the Municipal Hall will be closed on April 9-10.",
                 "likes": 45, "comments": 12, "time": "1 day ago"}
            ]
            
            for post in posts:
                st.markdown(f"""
                <div class='service-card'>
                    <div style='display: flex; justify-content: space-between;'>
                        <h4>{post['title']}</h4>
                        <small>{post['time']}</small>
                    </div>
                    <p><strong>by {post['user']}</strong></p>
                    <p>{post['content']}</p>
                    <div style='display: flex; gap: 1rem;'>
                        <span>❤️ {post['likes']}</span>
                        <span>💬 {post['comments']}</span>
                        <span>↗️ Share</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Trending Topics")
            trends = ["Business Permit", "Barangay Clearance", "Online Services", 
                     "Holiday Schedule", "New Features", "Community Updates"]
            
            for trend in trends:
                st.markdown(f"• #{trend}")
            
            st.markdown("### Community Stats")
            st.metric("Active Users", "1,234", "+56")
            st.metric("Posts Today", "45", "+12")
            st.metric"Solutions Found", "89", "+23")
    
    elif selected == get_text('learning'):
        st.markdown(f"<h1 class='main-header'>📚 {get_text('learning')}</h1>", unsafe_allow_html=True)
        
        # Learning categories
        categories = ["Getting Started", "Service Guides", "Video Tutorials", "FAQs", "Webinars"]
        selected_cat = st.radio("Browse by Category", categories, horizontal=True)
        
        col1, col2, col3 = st.columns(3)
        
        learning_resources = [
            {"title": "How to Apply for Business Permit", "type": "Guide", "duration": "10 min", "level": "Beginner"},
            {"title": "Understanding LGU Services", "type": "Video", "duration": "15 min", "level": "All Levels"},
            {"title": "Digital Document Upload Tips", "type": "Tutorial", "duration": "5 min", "level": "Beginner"},
            {"title": "Navigating the CanConnect Portal", "type": "Video", "duration": "8 min", "level": "Beginner"},
            {"title": "Frequently Asked Questions", "type": "FAQ", "duration": "20 min", "level": "All Levels"},
            {"title": "Advanced Features Tutorial", "type": "Guide", "duration": "12 min", "level": "Advanced"}
        ]
        
        for idx, resource in enumerate(learning_resources):
            with [col1, col2, col3][idx % 3]:
                icon = "📹" if resource['type'] == "Video" else "📄" if resource['type'] == "Guide" else "❓"
                st.markdown(f"""
                <div class='service-card'>
                    <div style='font-size: 2rem; text-align: center;'>{icon}</div>
                    <h4 style='text-align: center;'>{resource['title']}</h4>
                    <p><strong>Type:</strong> {resource['type']}</p>
                    <p><strong>Duration:</strong> {resource['duration']}</p>
                    <p><strong>Level:</strong> {resource['level']}</p>
                    <div style='text-align: center;'>
                        <button style='background: linear-gradient(135deg, #667eea, #764ba2); 
                                     color: white; border: none; padding: 0.5rem 1rem; 
                                     border-radius: 5px; cursor: pointer;'>
                            Start Learning →
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    elif selected == get_text('achievements'):
        st.markdown(f"<h1 class='main-header'>🏆 {get_text('achievements')}</h1>", unsafe_allow_html=True)
        
        # User stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2rem;'>⭐</div>
                <div class='stat-number'>1,250</div>
                <div class='stat-label'>Points</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2rem;'>🏅</div>
                <div class='stat-number'>12</div>
                <div class='stat-label'>Badges</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2rem;'>📊</div>
                <div class='stat-number'>5</div>
                <div class='stat-label'>Level</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2rem;'>👑</div>
                <div class='stat-number'>#42</div>
                <div class='stat-label'>Rank</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Achievements grid
        st.markdown("### Recent Achievements")
        
        achievements = [
            {"name": "First Application", "description": "Submitted your first application", "icon": "📝", "date": "2025-03-01"},
            {"name": "Early Adopter", "description": "Joined during launch month", "icon": "🚀", "date": "2025-03-05"},
            {"name": "Document Master", "description": "Uploaded 10+ documents", "icon": "📄", "date": "2025-03-10"},
            {"name": "Community Helper", "description": "Helped 5 users in forum", "icon": "🤝", "date": "2025-03-12"},
            {"name": "Fast Tracker", "description": "Tracked 20+ applications", "icon": "🔍", "date": "2025-03-14"},
            {"name": "Perfect Profile", "description": "Completed profile 100%", "icon": "👤", "date": "2025-03-15"}
        ]
        
        cols = st.columns(3)
        for idx, achievement in enumerate(achievements):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='service-card'>
                    <div style='font-size: 3rem; text-align: center;'>{achievement['icon']}</div>
                    <h4 style='text-align: center;'>{achievement['name']}</h4>
                    <p style='text-align: center; color: #666;'>{achievement['description']}</p>
                    <p style='text-align: center; font-size: 0.8rem;'>Earned: {achievement['date']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif selected == get_text('feedback'):
        st.markdown(f"<h1 class='main-header'>⭐ {get_text('feedback')}</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Share Your Feedback")
            
            with st.form("feedback_form"):
                feedback_type = st.selectbox(
                    "Feedback Type",
                    ["Suggestion", "Compliment", "Complaint", "Feature Request", "Bug Report"]
                )
                
                service_used = st.selectbox(
                    "Service Used",
                    ["Business Permit", "Barangay Clearance", "Police Clearance", 
                     "Health Appointment", "Document Request", "General"]
                )
                
                rating = st.slider("Rating", 1, 5, 5)
                
                feedback_text = st.text_area("Your Feedback")
                
                st.markdown("### How can we improve?")
                improvements = st.multiselect(
                    "Select areas for improvement",
                    ["Faster processing", "Better mobile experience", "More services", 
                     "Clearer instructions", "Better notifications", "More payment options"]
                )
                
                anonymous = st.checkbox("Submit anonymously")
                
                if st.form_submit_button("📤 Submit Feedback", type="primary"):
                    add_notification(
                        "Thank You! 🙏",
                        "Your feedback has been submitted successfully.",
                        "success"
                    )
                    st.success("Feedback submitted successfully!")
        
        with col2:
            st.markdown("### Recent Feedback")
            
            sample_feedback = [
                {"user": "Anonymous", "rating": 5, "comment": "Great service!", "time": "1 hour ago"},
                {"user": "Juan D.", "rating": 4, "comment": "Very helpful platform", "time": "3 hours ago"},
                {"user": "Maria S.", "rating": 5, "comment": "Easy to use", "time": "5 hours ago"}
            ]
            
            for fb in sample_feedback:
                stars = "⭐" * fb['rating']
                st.markdown(f"""
                <div class='service-card'>
                    <div style='display: flex; justify-content: space-between;'>
                        <strong>{fb['user']}</strong>
                        <small>{fb['time']}</small>
                    </div>
                    <p>{stars}</p>
                    <p>"{fb['comment']}"</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif selected == get_text('settings'):
        st.markdown(f"<h1 class='main-header'>⚙️ {get_text('settings')}</h1>", unsafe_allow_html=True)
        
        tabs = st.tabs(["Account", "Notifications", "Privacy", "Appearance", "Security"])
        
        with tabs[0]:
            st.markdown("### Account Settings")
            
            with st.form("account_settings"):
                st.text_input("Username", value=st.session_state.username, disabled=True)
                st.text_input("Email", value="user@example.com")
                st.text_input("Phone", value="09123456789")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input("New Password", type="password")
                with col2:
                    st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Update Account"):
                    st.success("Account settings updated!")
        
        with tabs[1]:
            st.markdown("### Notification Preferences")
            
            st.checkbox("Email Notifications", value=st.session_state.email_notifications)
            st.checkbox("SMS Notifications", value=st.session_state.sms_notifications)
            st.checkbox("Push Notifications", value=True)
            
            st.markdown("### Notification Types")
            st.checkbox("Application Updates", value=True)
            st.checkbox("Appointment Reminders", value=True)
            st.checkbox("System Announcements", value=True)
            st.checkbox("Community Activity", value=False)
            st.checkbox("Promotional Messages", value=False)
            
            if st.button("Save Notification Settings", type="primary"):
                st.success("Notification settings saved!")
        
        with tabs[2]:
            st.markdown("### Privacy Settings")
            
            st.checkbox("Show profile in community", value=True)
            st.checkbox("Share activity anonymously", value=False)
            st.checkbox("Allow data collection for improvements", value=True)
            
            st.markdown("### Data Management")
            if st.button("Download My Data"):
                st.info("Your data export is being prepared. You'll receive an email when ready.")
            
            if st.button("Delete Account", type="secondary"):
                st.warning("This action cannot be undone. Please contact support to delete your account.")
        
        with tabs[3]:
            st.markdown("### Appearance")
            
            theme = st.selectbox("Theme", ["Light", "Dark", "System Default"])
            font_size = st.select_slider("Font Size", options=["Small", "Medium", "Large", "Extra Large"])
            compact_mode = st.checkbox("Compact Mode")
            
            st.markdown("### Accessibility")
            st.checkbox("High Contrast Mode")
            st.checkbox("Screen Reader Optimized")
            st.selectbox("Font Family", ["Default", "OpenDyslexic", "ATypI"])
            
            if st.button("Apply Appearance Settings", type="primary"):
                st.success("Appearance settings applied!")
        
        with tabs[4]:
            st.markdown("### Security Settings")
            
            st.checkbox("Two-Factor Authentication", value=st.session_state.two_factor_enabled)
            st.checkbox("Login Notifications", value=True)
            st.checkbox("Device Tracking", value=True)
            
            st.markdown("### Session Management")
            st.write("Active Sessions: 2")
            if st.button("Log Out All Devices"):
                st.warning("You've been logged out of all other devices.")
            
            st.markdown("### Login History")
            login_history = [
                {"date": "2025-03-14 09:30", "device": "Chrome on Windows", "location": "Cantilan"},
                {"date": "2025-03-13 18:45", "device": "Safari on iPhone", "location": "Cantilan"},
                {"date": "2025-03-12 08:15", "device": "Firefox on Mac", "location": "Cantilan"}
            ]
            
            for login in login_history:
                st.write(f"• {login['date']} - {login['device']} ({login['location']})")
    
    elif selected == get_text('help'):
        st.markdown(f"<h1 class='main-header'>❓ {get_text('help')}</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Frequently Asked Questions")
            
            faqs = [
                {"q": "How do I apply for a Business Permit?", 
                 "a": "Go to Services > Business Permit, fill out the form, upload required documents, and submit."},
                {"q": "How can I track my application?", 
                 "a": "Use the Track Application feature with your reference number or text your ref no to 2929."},
                {"q": "What are the office hours?", 
                 "a": "Monday-Friday, 8:00 AM to 5:00 PM. Closed on weekends and holidays."},
                {"q": "How much are the fees?", 
                 "a": "Fees vary by service. Check the specific service page for detailed fee information."},
                {"q": "Can I apply without internet?", 
                 "a": "Yes! You can text your requests to 2929 or visit any barangay hall for assistance."}
            ]
            
            for faq in faqs:
                with st.expander(faq['q']):
                    st.write(faq['a'])
            
            st.markdown("### Video Tutorials")
            video_topics = ["Getting Started", "How to Apply", "Tracking Applications", "Using the Chatbot"]
            
            cols = st.columns(2)
            for idx, topic in enumerate(video_topics):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class='service-card'>
                        <div style='font-size: 2rem; text-align: center;'>📹</div>
                        <h4 style='text-align: center;'>{topic}</h4>
                        <p style='text-align: center;'>5 min tutorial</p>
                        <div style='text-align: center;'>
                            <button style='background: linear-gradient(135deg, #667eea, #764ba2); 
                                         color: white; border: none; padding: 0.5rem 1rem; 
                                         border-radius: 5px; cursor: pointer;'>
                                Watch Now
                            </button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Contact Support")
            
            st.markdown("""
            <div class='glass-card'>
                <h4>📞 Phone</h4>
                <p>(086) 123-4567</p>
                <p>Mon-Fri, 8AM-5PM</p>
                
                <h4>📧 Email</h4>
                <p>support@canconnect.gov.ph</p>
                
                <h4>💬 SMS</h4>
                <p>Text CANNECT to 2929</p>
                
                <h4>📍 Office</h4>
                <p>Municipal Hall<br>Poblacion, Cantilan<br>Surigao del Sur</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Emergency Contacts")
            st.markdown("""
            <div style='background: #ff4444; color: white; padding: 1rem; border-radius: 10px; text-align: center;'>
                <h3>🚨 911</h3>
                <p>Emergency Hotline</p>
                <hr>
                <p>🚒 Fire: 160</p>
                <p>🚓 Police: 117</p>
                <p>🚑 Ambulance: 143</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif selected == get_text('emergency'):
        st.markdown(f"<h1 class='main-header'>🚨 {get_text('emergency')}</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='glass-card' style='text-align: center; background: rgba(255, 68, 68, 0.9);'>
                <div style='font-size: 4rem; animation: pulse 1s infinite;'>🚨</div>
                <h1 style='color: white; font-size: 3rem;'>911</h1>
                <h3 style='color: white;'>Emergency Hotline</h3>
                <p style='color: white;'>Available 24/7</p>
                <button style='background: white; color: #ff4444; border: none; 
                             padding: 1rem 2rem; border-radius: 50px; font-size: 1.2rem;
                             margin: 1rem; cursor: pointer; animation: pulse 2s infinite;'>
                    📞 CALL NOW
                </button>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class='glass-card'>
                <h3>Emergency Services</h3>
                <table style='width: 100%;'>
                    <tr>
                        <td>🚒 Fire Department</td>
                        <td><strong>160</strong></td>
                    </tr>
                    <tr>
                        <td>🚓 Police Station</td>
                        <td><strong>117</strong></td>
                    </tr>
                    <tr>
                        <td>🚑 Ambulance</td>
                        <td><strong>143</strong></td>
                    </tr>
                    <tr>
                        <td>🏥 Rural Health Unit</td>
                        <td><strong>(086) 123-4568</strong></td>
                    </tr>
                    <tr>
                        <td>🌊 Disaster Risk Reduction</td>
                        <td><strong>(086) 123-4569</strong></td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='glass-card' style='margin-top: 1rem;'>
                <h3>SMS Emergency</h3>
                <p>Text CANNECT to <strong>2929</strong></p>
                <p>Format: EMERGENCY [your message] [location]</p>
                <p>Example: EMERGENCY Fire at Poblacion</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Emergency alerts
        st.markdown("### Active Alerts")
        alerts = [
            {"type": "Weather", "message": "Tropical Storm Warning - Signal #1", "time": "2 hours ago"},
            {"type": "Health", "message": "COVID-19 Booster Shot Available at RHU", "time": "1 day ago"},
            {"type": "Safety", "message": "Road Closure - National Highway", "time": "3 hours ago"}
        ]
        
        for alert in alerts:
            st.markdown(f"""
            <div class='notification' style='background: #fff3cd;'>
                <strong>⚠️ {alert['type']} Alert</strong>
                <p>{alert['message']}</p>
                <small>{alert['time']}</small>
            </div>
            """, unsafe_allow_html=True)

# Floating Action Button
st.markdown("""
<div class='fab' onclick="alert('Quick Help Menu')">
    💬
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: white; padding: 2rem; background: rgba(0,0,0,0.3); border-radius: 10px;'>
        <div style='display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem;'>
            <span>📞 (086) 123-4567</span>
            <span>✉️ support@canconnect.gov.ph</span>
            <span>📍 Poblacion, Cantilan, Surigao del Sur</span>
        </div>
        <p>© 2025 CanConnect - Municipality of Cantilan. All rights reserved.</p>
        <div style='display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;'>
            <span>Privacy Policy</span>
            <span>Terms of Use</span>
            <span>Accessibility</span>
            <span>Sitemap</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)