# Lazy Network Automation

A web-based network automation platform built with Django. Manage network devices, push configurations, backup configs, run diagnostics, and monitor infrastructure — all from a browser.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Django](https://img.shields.io/badge/Django-6.0-green)

---

## Features

- **Device Inventory** — manage devices with SSH and SNMP credentials
- **Push Config** — send CLI commands to multiple devices simultaneously via SSH
- **Verify Config** — run show/check commands and view live output
- **Backup Config** — save device configs to files with timestamps
- **Ping Tool** — ping multiple devices and see per-device results
- **SNMP Walk** — walk any OID using device credentials from the inventory
- **Compare File** — diff two backup config files side by side
- **History** — full log of all automation actions with status and messages
- **Multi-vendor SSH** — supports MikroTik, Cisco, FortiGate, Ruijie, Teltonika, Ransnet (in progress)

---

## Requirements

- Python 3.10+
- `snmpwalk` installed on the server for SNMP Walk feature:
  - **macOS:** `brew install net-snmp`
  - **Linux:** `sudo apt install snmp` or `sudo yum install net-snmp-utils`
  - **Windows:** [net-snmp installer](http://www.net-snmp.org/download.html)

---

## Quick Start (Development)

### 1. Clone the repository

```bash
git clone https://github.com/toor404/lazy-network-automation.git
cd lazy-network-automation
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv l_env

# macOS / Linux
source l_env/bin/activate

# Windows
l_env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install django django-filter paramiko requests python-decouple psycopg2-binary
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
SECRET_KEY=your-django-secret-key-here
DB_NAME=lazy
DB_USER=lazymin
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432
NMS_API_TOKEN=your-nms-api-token
```

> **Development tip:** The app uses SQLite by default — no database setup needed for local dev. The DB variables in `.env` are only needed if you switch to PostgreSQL.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Start the server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## Production Deployment (Linux)

### 1. System dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx snmp
```

### 2. Clone and set up

```bash
git clone https://github.com/toor404/lazy-network-automation.git
cd lazy-network-automation
python3 -m venv l_env
source l_env/bin/activate
pip install django django-filter paramiko requests python-decouple psycopg2-binary gunicorn
```

### 3. Set up PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE lazy;
CREATE USER lazymin WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE lazy TO lazymin;
\q
```

### 4. Configure environment

```bash
cp .env.example .env
nano .env
```

Update `settings.py` to use PostgreSQL by replacing the `DATABASES` block:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

### 5. Prepare static files and database

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### 6. Run with Gunicorn

```bash
gunicorn mywebsite.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### 7. Nginx config

Create `/etc/nginx/sites-available/lazy`:

```nginx
server {
    listen 80;
    server_name your-domain-or-ip;

    location /static/ {
        alias /path/to/lazy-network-automation/static/;
    }

    location /media/ {
        alias /path/to/lazy-network-automation/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/lazy /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

---

## Project Structure

```
lazy-network-automation/
├── automation/        # SSH automation engine (push, backup, verify, ping, SNMP, diff)
├── masterdata/        # Device inventory and LOV (List of Values)
├── nms/               # External NMS API integration
├── mywebsite/         # Django project settings, root URLs, auth views
├── templates/         # All HTML templates (extend base.html)
├── static/            # CSS, JS, and image assets
├── media/             # Uploaded and generated files (backup configs)
├── .env.example       # Environment variable template
└── manage.py
```

---

## Adding a New Device Vendor

1. Add the vendor name to the LOV table via **Master Data → LOV** in the UI
2. In `automation/views.py`, add a branch for the vendor in `push_config`, `verify_config`, and `backup_config`:

```python
elif vendorna.lower() == 'yourvendor':
    # vendor-specific SSH interaction here
```

Refer to the vendor table in `CLAUDE.md` for CLI style notes per vendor.

---

## License

MIT
