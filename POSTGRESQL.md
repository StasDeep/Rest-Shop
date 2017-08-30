## PostgreSQL

The following apt commands will get you the packages you need:

```
sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
```

During the Postgres installation, an operating system user named postgres was created to correspond to the postgres PostgreSQL administrative user.
We need to change to this user to perform administrative tasks:
```
sudo su - postgres
```

You should now be in a shell session for the postgres user. Log into a Postgres session by typing:
```
psql
```

Create database `restshop`:
```
CREATE DATABASE restshop;
```

Create a database user:
```
CREATE USER restshopuser WITH PASSWORD '12345678';
```

Change user settings:
```
ALTER ROLE restshopuser SET client_encoding TO 'utf8';
ALTER ROLE restshopuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE restshopuser SET timezone TO 'UTC';
ALTER ROLE restshopuser CREATEDB;
```

Now, all we need to do is give our database user access rights to the database we created:
```
GRANT ALL PRIVILEGES ON DATABASE restshop TO restshopuser;
```

Exit the SQL prompt to get back to the postgres user's shell session:
```
\q
```

Exit out of the postgres user's shell session to get back to your regular user's shell session:
```
exit
```
