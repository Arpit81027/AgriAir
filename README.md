# AgriAir

A Django-based smart agriculture application.

## Tech stack

- Python and Django
- SQLite
- Django templates, HTML, CSS, and JavaScript
- Pillow for image handling

## Run locally (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

For deployments, set `DJANGO_SECRET_KEY` to a secure, unique value. The built-in
fallback key is only for local development.
