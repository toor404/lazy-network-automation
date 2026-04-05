# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Lazy Network Automation** — a Django web application for managing and automating network device configuration via SSH (Paramiko). It allows users to push configs, verify configs, backup configs, and monitor devices across a managed device inventory.

## Commands

```bash
# Activate the virtual environment first
source l_env/bin/activate

# Run the development server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Run tests for a specific app
python manage.py test automation
python manage.py test masterdata
python manage.py test nms

# Django shell
python manage.py shell
```

## Architecture

### Apps

- **masterdata** — Device inventory. Manages `MasterData` (network devices with SSH/SNMP credentials) and `LOV` (List of Values: device types, vendors, SNMP versions). All automation operations pull device info from here.
- **automation** — Core automation engine. Uses Paramiko to SSH into devices and run commands. Handles push config, verify config, backup config, and logs results to `Log` and `BackupConfig` models. Backup files are saved to `media/backup_config/`.
- **nms** — Network monitoring integration. Fetches device data from an external NMS REST API and displays it.
- **mywebsite** — Django project root. Contains settings, root URL config, and auth views (login/logout/register).

### Key relationships

- `automation` views import `MasterData` from `masterdata` to look up SSH credentials before connecting.
- `automation.filters` uses `django_filters` for filtering both `MasterData` and `Log` querysets.
- All views are login-protected via `@login_required`.

### Database

PostgreSQL (`lazy` database, user `lazymin`, port 5432 on localhost). A commented-out MySQL config is also present in `settings.py`.

### Templates

All templates live in the project-level `templates/` directory (not per-app). They extend `base.html`. Static assets use a frontend build in `static/` with a `gulpfile.js`.

### Vendor-specific SSH logic

In `automation/views.py`, device vendor is checked by string-comparing `str(mangsa.device_vendor)`. The goal is to support many vendors — currently only `'Ransnet'` has partial SSH handling; all others fall through to an "Unrecognized Vendor" log entry.

**Target vendor support** (to be implemented):

| Vendor | CLI style | Notes |
|---|---|---|
| Ransnet | enable shell | Already partially wired; string check is inconsistent (`'Ransnet'` vs `'ransnet'`) — normalize to lowercase |
| MikroTik | RouterOS CLI | No `enable` prompt; direct commands after SSH login |
| Cisco IOS/IOS-XE | enable shell | `enable` → enable password → exec commands |
| Cisco IOS-XR | direct exec | No enable mode |
| Fortinet FortiGate | direct exec | `config` / `end` blocks |
| Ruijie | enable shell | Similar to Cisco IOS |
| Teltonika | Linux shell | Busybox/OpenWRT-based; standard Unix commands |

When adding a new vendor, add a branch in the `if vendorna == ...` block for each operation (push, verify, backup). Extract the vendor string with `.strip().split(" - ")[-1]` (already done in `verify_config`) and compare case-insensitively (`vendorna.lower()`). Consider refactoring repeated SSH connection and vendor dispatch into a shared utility to avoid duplicating the pattern across all three operation views.
