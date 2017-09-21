# Rest-Shop

Training e-commerce with Python 3 and Angular.

## Installation

Create [virtual environment](https://virtualenv.pypa.io/en/stable/) (preferably):
```
virtualenv -p python3 restshop
```

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

Install Node.js:
```
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
```

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
