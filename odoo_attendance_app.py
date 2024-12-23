import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv
import sys

# Add the path to import_attendance.py
module_path = os.path.join(os.path.dirname(__file__), 
    "sucess_project_folders/sucess_2_with_test_and create missing attendance/row data/odoo_attendance_import")
sys.path.append(module_path)

from import_attendance import OdooAPI, process_excel_file, visualize_attendance

# Set page config
st.set_page_config(
    page_title="Odoo Attendance Import",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .step-header {
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'attendance_df' not in st.session_state:
        st.session_state.attendance_df = None
    if 'odoo_api' not in st.session_state:
        st.session_state.odoo_api = None
    if 'missing_employees' not in st.session_state:
        st.session_state.missing_employees = []
    if 'existing_employees' not in st.session_state:
        st.session_state.existing_employees = []
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    if 'odoo_connected' not in st.session_state:
        st.session_state.odoo_connected = False
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False

def display_metrics(df):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Unique Employees", len(df['employee_id'].unique()))
    with col3:
        st.metric("Date Range", f"{df['date'].min()} to {df['date'].max()}")
    with col4:
        avg_hours = df['total_hours'].mean()
        st.metric("Average Hours", f"{avg_hours:.2f}")

def main():
    st.title("🏢 Odoo Attendance Import Tool")
    
    # Initialize session state
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Progress Checklist")
        st.write("✔️ File Upload" if st.session_state.file_uploaded else "⭕ File Upload")
        st.write("✔️ Data Processing" if st.session_state.processing_complete else "⭕ Data Processing")
        st.write("✔️ Odoo Connection" if st.session_state.odoo_connected else "⭕ Odoo Connection")
        st.write("✔️ Import Complete" if 'import_complete' in st.session_state else "⭕ Import Complete")
        
        st.markdown("---")
        st.markdown("### 🔧 Help")
        st.markdown("""
        1. Upload your Excel file
        2. Review processed data
        3. Connect to Odoo
        4. Import attendance records
        """)
    
    # Step 1: File Upload
    with st.expander("📤 STEP 1: Upload Excel File", expanded=not st.session_state.file_uploaded):
        uploaded_file = st.file_uploader("Choose an Excel file", type=['xls', 'xlsx'])
        
        if uploaded_file:
            try:
                with st.spinner('Processing file...'):
                    st.session_state.attendance_df = process_excel_file(uploaded_file)
                    st.session_state.file_uploaded = True
                st.success("✅ File processed successfully!")
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                st.session_state.file_uploaded = False
    
    # Step 2: Data Processing and Analysis
    if st.session_state.file_uploaded:
        with st.expander("📊 STEP 2: Data Processing and Analysis", expanded=True):
            st.subheader("Data Overview")
            display_metrics(st.session_state.attendance_df)
            
            tab1, tab2, tab3 = st.tabs(["📈 Raw Data", "📊 Visualizations", "📑 Summary"])
            
            with tab1:
                st.dataframe(st.session_state.attendance_df, use_container_width=True)
            
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Daily Hours by Employee")
                    # Your visualization code here
                    
                with col2:
                    st.subheader("Average Hours by Employee")
                    # Your visualization code here
            
            with tab3:
                st.subheader("Statistical Summary")
                st.dataframe(st.session_state.attendance_df.describe(), use_container_width=True)
            
            if st.button("✅ Confirm Data Processing"):
                st.session_state.processing_complete = True
                st.success("Data processing confirmed!")
    
    # Step 3: Connect to Odoo
    if st.session_state.processing_complete:
        with st.expander("🔌 STEP 3: Connect to Odoo", expanded=not st.session_state.odoo_connected):
            if st.button("Connect to Odoo"):
                try:
                    with st.spinner('Connecting to Odoo...'):
                        st.session_state.odoo_api = OdooAPI()
                        st.session_state.odoo_connected = True
                    
                    unique_employees = st.session_state.attendance_df['employee_id'].unique()
                    st.session_state.missing_employees, st.session_state.existing_employees = \
                        st.session_state.odoo_api.check_missing_employees(unique_employees)
                    
                    st.success("✅ Successfully connected to Odoo!")
                    
                    if st.session_state.missing_employees:
                        st.warning(f"⚠️ Found {len(st.session_state.missing_employees)} missing employees")
                except Exception as e:
                    st.error(f"❌ Error connecting to Odoo: {str(e)}")
                    st.session_state.odoo_connected = False
    
    # Step 4: Import Records
    if st.session_state.odoo_connected:
        with st.expander("📥 STEP 4: Import Records", expanded=True):
            if st.session_state.missing_employees:
                st.warning(f"⚠️ Please create {len(st.session_state.missing_employees)} missing employees first")
                for badge_id in st.session_state.missing_employees:
                    create_employee_form(badge_id)
            else:
                if st.button("Start Import"):
                    with st.spinner('Importing records...'):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        total_records = len(st.session_state.attendance_df)
                        success_count = 0
                        error_count = 0
                        
                        for index, row in st.session_state.attendance_df.iterrows():
                            try:
                                employee_id = st.session_state.odoo_api.get_employee_id(row['employee_id'])
                                st.session_state.odoo_api.create_attendance(
                                    employee_id=employee_id,
                                    check_in=row['check_in'],
                                    check_out=row['check_out']
                                )
                                success_count += 1
                            except Exception as e:
                                error_count += 1
                            
                            progress = (index + 1) / total_records
                            progress_bar.progress(progress)
                            status_text.text(f"Processing... {index + 1}/{total_records}")
                        
                        st.session_state.import_complete = True
                        st.success(f"✅ Import completed!\n\n"
                                 f"Successfully imported: {success_count} records\n"
                                 f"Failed: {error_count} records")

if __name__ == "__main__":
    main()
