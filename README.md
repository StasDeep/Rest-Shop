# Rest-Shop

Sneakers shop test site with Python 3 and Angular.

## Installation

Install dependencies:
```
pip install -r requirements.txt
```

Install PostgreSQL: [instructions here](POSTGRESQL.md).

Copy secrets:
```
cp restshop_project/restshop_project/secret_settings.py.example restshop_project/restshop_project/secret_settings.py
```

Change `USER_NAME` and `USER_PASSWORD` constants in `secret_settings.py`.

Set up database schema:
```
python manage.py migrate
```

Create superuser:
```
python manage.py createsuperuser
```
