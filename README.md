setup with pip

create secret_key.json file in the config > settings of the format

    {
        "email_app_password": "password",
        "secret_key": "some_secret_key"
    }


setup database postgres

    sudo apt-get install postgresql
    sudo su postgres
    psql -d postgres -U postgres
    CREATE USER era WITH PASSWORD 'erahakarasimra';
    CREATE DATABASE era;
    GRANT ALL PRIVILEGES ON DATABASE era TO era;
    
    python manage.py migrate
    
    python manage.py runserver 0.0.0.0:8000
    
    gunicorn --bind 0.0.0.0:8000 config.wsgi


dev@localhost:/opt/letsencrypt$ sudo -H ./letsencrypt-auto certonly --standalone --renew-by-default -d kipaprints.com


OSX
    
    brew install postgres
    brew services start postgresql
    psql postgres


Watch SASS

    sass static_dev/bulma/style.scss:static_dev/bulma/css/style.min.css --watch --style compressed
