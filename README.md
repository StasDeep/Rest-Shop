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

## Frontend Setting

Go to `ui` folder:
```
cd ui/
```

Install nodejs dependencies:
```
npm install
```

Install gulp (for frontend building):
```
npm install -g gulp-cli
```

Install project dependencies:
```
bower install
```

Build frontend:
```
gulp
```

## Running

Run server:
```
python manage.py runserver
```

Go to http://localhost:8000 and start using app.
