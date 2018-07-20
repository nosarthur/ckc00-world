.PHONY: test shell migrate

test:
	python manage.py test --parallel

shell:
	python manage.py shell

migrate:
	python manage.py makemigrations
	python manage.py migrate
