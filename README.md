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

Then create superuser
```
python3 manage.py createsuperuser
```

## steps

ubuntu 18.04

maybe use docker later

## useful endpoints

After spin up the server `python manage.py runserver`, checkout

* http://localhost:8000/doc
* http://localhost:8000/admin/
* http://localhost:8000/api/
