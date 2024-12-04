
# MediTech API Setup Guide

## Prerequisites
Before starting, ensure you have the following installed:

1. **Python** (Version 3.9 or higher)
   - Download from [python.org](https://www.python.org/).
   - Verify installation:  
     ```bash
     python --version  # or python3 --version
     ```
2. **pip** (Python package manager)  
   Comes bundled with Python. Verify:
   ```bash
   pip --version
   ```
3. **Git**  
   Install Git to clone the repository. Verify:  
   ```bash
   git --version
   ```

4. (Optional) **Virtual Environment Tool**  
   Recommended for isolated development:
   ```bash
   pip install virtualenv
   ```

---

## Cloning the Repository
Clone the MediTech API repository from GitHub:
```bash
git clone https://github.com/xMakuno/meditech-api.git
cd meditech-api
```

---

## Setting Up the Environment

### 1. Create a Virtual Environment  
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Required Dependencies  
Install the dependencies from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, generate it first:
```bash
pip freeze > requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory to configure sensitive environment variables. Here’s a template:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
SQLALCHEMY_DATABASE_URI=sqlite:///meditech.db  # Or your database URI
BCRYPT_LOG_ROUNDS=12
SESSION_TYPE=filesystem
```

---

## Database Setup

### 1. Initialize the Database  
Run the following commands to initialize and migrate the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 2. Seed Data (Optional)  
If there’s a script for seeding data, run it:
```bash
python seed.py  # Replace with your seeding script if available
```

---

## Running the API

### 1. Start the Development Server  
Run the Flask application:
```bash
flask run
```
The server will be available at `http://127.0.0.1:5000`.

### 2. Run with Gunicorn (Production, Linux)  
For production, use Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## Windows-Specific Steps
If Flask fails to run on Windows:
1. Ensure Flask scripts directory is added to PATH. Example for Python 3.9:
   ```bash
   set PATH=%PATH%;C:\Users\YourUsername\AppData\Local\Programs\Python\Python39\Scripts
   ```

2. Use `flask` as an environment variable:
   ```bash
   set FLASK_APP=run.py
   set FLASK_ENV=development
   ```

---

## Linux-Specific Notes

### Installing SQLite (if not installed)
```bash
sudo apt update
sudo apt install sqlite3
```

### Permissions for Virtual Environment
Ensure the virtual environment is activated with appropriate permissions:
```bash
chmod -R 755 venv
source venv/bin/activate
```

---

## Testing

Run unit tests (if configured):
```bash
pytest tests/
```

---

## Deployment (Optional)

### Using WSGI with Gunicorn and Nginx (Linux)

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```
2. Create a Gunicorn systemd service file (`/etc/systemd/system/meditech.service`):
   ```ini
   [Unit]
   Description=MediTech API
   After=network.target

   [Service]
   User=your_user
   Group=your_group
   WorkingDirectory=/path/to/meditech-api
   ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app

   [Install]
   WantedBy=multi-user.target
   ```
3. Start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start meditech
   sudo systemctl enable meditech
   ```

4. Set up Nginx as a reverse proxy:
   ```bash
   sudo apt install nginx
   sudo nano /etc/nginx/sites-available/meditech
   ```
   Example Nginx configuration:
   ```nginx
   server {
       listen 80;
       server_name your_domain_or_ip;

       location / {
           proxy_pass http://127.0.0.1:5000;
           include proxy_params;
           proxy_redirect off;
       }
   }
   ```
   Enable the configuration:
   ```bash
   sudo ln -s /etc/nginx/sites-available/meditech /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

This guide covers both development and production setups.
