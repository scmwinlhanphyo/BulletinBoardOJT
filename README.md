# locallibrary
 Django BulletinBoard Project

## Create Virtual Environment

`python -m venv .bulletin-board-env`

## Activate Virtual Environment
`.bulletin-board-env\Scripts\activate`

## Install Dependencies
`python -m pip install -r requirements.txt`

# Create Mysql Database
create 'bulletinboard' database.

# Change My SQL Username and password
dir => bulletinboard/bulletinboard.cnf

name = bulletinboard

port = 3306

host = localhost

username = root

password = root

## Migrate database

`python manage.py makemigrations`

`python manage.py migrate`

## Create admin

`python manage.py createsuperuser`

*** Add user name, email and password. ***

## Run Django App

`py manage.py runserver`

### Admin pannel

[/admin/](http://localhost:8000/admin/)

### Posts app

[/post/](http://localhost:8000/posts/)

### Run Django Test Code
python manage.py test posts.tests

# Run Test Code only one file
py manage.py test --pattern="test_views.py"

# Run Test Code with coverage
coverage run --source='.' manage.py test
coverage report -m

# Run Test Code only one file with coverage
coverage run --source='.' manage.py test --pattern="test_views.py"
coverage report -m