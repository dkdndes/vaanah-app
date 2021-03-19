# vaanah-app
Vaanah application

1- First  install django-oscar (after python and pip installation) :
$ pip install django-oscar

2- Start the django-oscar project  with this command :
$ django-admin startproject [project-name]
PS : Here you will find further action for setting up django-oscar

2- After create your virtualenv with :
$ virtualenv [virtualenv-name]

If you don't have a virtualenv yet you 'll need to install it first with this command :
$ pip install virtualenv
Then create your virtualenv with the command below.

3- Activate the virtualenv  :
On Mac OS/Unix :
$ source [virtualenv-name]/bin/activate
On Windows :
$ source [virtualenv-name]/Scripts/activate 

4- Generate requirements file 
$ pip freeze > requirements.txt

5- Install project dependencies:
$ pip install -r requirements.txt

6- Then simply apply the migrations :
$ python manage.py migrate

7- You can now run the development server :
$ python manage.py runserver
