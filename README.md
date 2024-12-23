# Streamlit Odoo Attendance Import

A Streamlit application for importing attendance data from Excel files into Odoo.

## Features
- Excel file processing and validation
- Interactive data visualization and analysis
- Seamless Odoo integration
- Employee management
- Automated attendance record import
- Progress tracking and error handling

## Setup
1. Clone the repository
```bash
git clone git@github.com:sabryyoussef/streamlit-odoo-attendance.git
cd streamlit-odoo-attendance
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
Create a .env file with:
```
ODOO_URL=your_odoo_url
ODOO_DB=your_database
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password
api_key=your_api_key
```

5. Run the application
```bash
streamlit run odoo_attendance_app.py
```

## Author
- Sabry Youssef
- Email: vendorah2@gmail.com

## License
MIT License
