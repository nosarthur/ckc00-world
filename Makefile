.PHONY: test shell migrate venv run

test:
	python manage.py test --parallel

shell:
	python manage.py shell

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver
