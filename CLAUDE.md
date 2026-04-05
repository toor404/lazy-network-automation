# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Stack

This project primarily uses Python (Django) with HTML templates and Markdown documentation. Always use Python 3 conventions and Django best practices.

- **Backend:** Python 3.10+, Django 6.x
- **Frontend:** HTML templates (Bootstrap-based), no JS framework
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Key libs:** Paramiko (SSH), django-filter, python-decouple, requests

## Platform Awareness

When suggesting shell commands, always check for OS/platform differences. Prefer cross-platform Python solutions over platform-specific shell commands when possible.

- `ping`: macOS uses `-W` in milliseconds, Linux in seconds, Windows uses `-n` (count) and `-w` (timeout ms)
- `snmpwalk`: macOS path is `/opt/homebrew/bin/snmpwalk` or `/usr/local/bin/snmpwalk`; Linux `/usr/bin/snmpwalk`; Windows requires net-snmp installer
- Use `platform.system()` to detect OS at runtime — already done in `automation/views.py` for ping and SNMP walk
- Always use `l_env/bin/python` directly (not `python` or `source activate`) since shell state doesn't persist between Bash calls

## Tool Usage Constraints

Never attempt to run interactive CLI commands directly (e.g., `gh auth login`, `ssh-keygen` with prompts, `git rebase -i`). Instead, provide the exact command for the user to run manually using the `! <command>` prefix in the prompt, or use non-interactive flags/environment variables where available.

Before any destructive git operation (filter-repo, reset --hard, rebase), always create a backup branch first:
```bash
git branch backup-$(date +%s)
```

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

SQLite (`db.sqlite3`) for development. PostgreSQL config is commented out in `settings.py` for future production use.

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

## GitHub Workflow

**Every change must be pushed to GitHub with a clear description.** After completing any code change:

```bash
git add <changed files>
git commit -m "short summary

- bullet describing what changed and why
- another bullet if needed"
git push origin main
```

Commit message rules:
- First line: short imperative summary (`Add ping tool`, `Fix SNMP walk timeout`, `Refactor SSH vendor dispatch`)
- Body bullets: what changed, which files, and why — enough context for someone reading the history to understand without looking at the diff
- Never use vague messages like `fix`, `update`, or `changes`
- One logical change per commit — don't bundle unrelated edits
