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

For development, run with `--env=dev`:
```
gulp --env=dev
```

## Populating database

If you want to automatically populate database with data,
you need to get it from a website with a scraper.

I've programmed a spider for Nike website, so you can use it (it may take up to an hour):
```
cd restshop/fixtures/products/
scrapy crawl nike -o nike.json
```

Convert spider output to Django fixture:
```
cd restshop/fixtures/
python process_raw.py -i products/nike.json -o nike.json
```

Copy scraped images to media folder:
```
cd restshop_project/
mv restshop/fixtures/products/product_images media/product_images
```

Load data from Django fixture (it may take several minutes):
```
python manage.py loaddata nike
```

## Running

Run server:
```
python manage.py runserver
```

Go to http://localhost:8000 and start using app.
