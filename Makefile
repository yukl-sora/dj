# WORKING WITH PROJECT
r:
	./manage.py runserver

m:
	./manage.py makemigrations
	./manage.py migrate

# TESTING APPLICATION
ta:
	./manage.py test apps.account.tests
tp:
	./manage.py test apps.profiles.tests

# CREATING ADMIN ACCOUNT
su:
	./manage.py createsuperuser

# STARTING CELERY
c:
	celery -A apps.account.tasks worker -l info

# WRITING REQUIREMENTS
req:
	pip freeze > requirements.txt