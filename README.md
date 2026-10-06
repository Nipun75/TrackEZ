# TrackEZ Expense Tracker

Django + SQLite income and expense tracker.

## Features
- User registration and login
- Income and expense management
- Dashboard balance calculation
- Income vs expense trend chart
- Top 5 income and expense charts
- Transaction history and date filtering
- Secure user-specific transaction access
- Quick transaction calculation without saving
- Excel (.xlsx) export with optional date filtering

## Run locally
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ and register an account.

## Automated tests
Run:
```bash
python manage.py test
```

The test suite covers dashboard totals, transaction creation, user-data isolation, deletion protection, quick calculations, date filtering, Excel export, and authentication-protected pages.
