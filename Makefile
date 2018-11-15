.PHONY: test shell migrate run

test:
	python3 manage.py test --parallel

shell:
	python3 manage.py shell

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

run:
	python3 manage.py runserver
