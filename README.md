# Streamlit Odoo Attendance Import

A Streamlit application for importing attendance data from Excel files into Odoo.

## Features
- Excel file processing
- Data visualization and analysis
- Odoo integration
- Employee management
- Attendance record import

## Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a .env file with your Odoo credentials:
   ```
   ODOO_URL=your_odoo_url
   ODOO_DB=your_database
   ODOO_USERNAME=your_username
   ODOO_PASSWORD=your_password
   api_key=your_api_key
   ```
5. Run the application:
   ```bash
   streamlit run odoo_attendance_app.py
   ```

## Usage
1. Upload Excel file
2. Review processed data
3. Connect to Odoo
4. Import attendance records

## Author
- Sabry Youssef
- Email: vendorah2@gmail.com
