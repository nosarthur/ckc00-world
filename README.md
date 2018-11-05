# ckc00
[![Build Status](https://travis-ci.org/nosarthur/ckc00alumni.svg?branch=master)](https://travis-ci.org/nosarthur/ckc00alumni)

CKC00 alumni locator

django REST backend + vue2 frontend

## installation

After downloading the source code, run
```
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

To setup database
```
make migrate
```

To populate the cities_light related database entries
```
python3 manage.py cities_light --progress
```

Then create superuser
```
python3 manage.py createsuperuser
```

## endpoints

After creating super user, spin up the server `python manage.py runserver`.

Then log in as super user at `http://localhost:8000/admin/`. The API access
points can be seen at

* http://localhost:8000/doc
* http://localhost:8000/api/
