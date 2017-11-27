# Rest-Shop

Training e-commerce with Python 3 and Angular.

## Installation

Create [virtual environment](https://virtualenv.pypa.io/en/stable/) (preferably):
```
virtualenv -p python3 restshop
```

Install dependencies (make sure you are inside your virtual environment):
```
pip install -r requirements.txt
```

Install PostgreSQL: [instructions here](POSTGRESQL.md).

Set environment variables:
```
export DB_USER=YOUR_DB_USERNAME
export DB_PASSWORD=YOUR_DB_PASSWORD
```

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

For development, run with `--env=dev`:
```
gulp --env=dev
```

## Populating database

If you want to automatically populate database with data,
you need to get it from a website with a scraper.

You can use a small bash script for that purpose:
```
./scrape_nike.sh
```


## Running

Run server:
```
python manage.py runserver
```

Go to http://localhost:8000 and start using app.
