# ckc00
[![Build Status](https://travis-ci.org/nosarthur/ckc00alumni.svg?branch=master)](https://travis-ci.org/nosarthur/ckc00alumni)

CKC00 alumni locator

django REST backend + vue3 frontend (separate repo)

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

Then login as super user at `http://localhost:8000/admin/`. The API access
points can be seen at

* http://localhost:8000/docs/
* http://localhost:8000/api/

Example responses:

* GET /api/gender/countries/
    * [["United States", [14, 19]], ["Canada", [10, 1]]]
* GET /api/gender/tags/
    * [["machine-learning", [20, 8]], ["block-chain", [7, 10]]]
* GET /api/users/
* GET /api/users/{id}/
    * { "pk": 422,
        "url": "http://localhost:8000/api/users/422/",
        "email": "aaa@gmail.com",
        "first_name": "John",
        "last_name": "Doe",
        "gender": "m",
        "phone": "",
        "employer": "",
        "homepage": null,
        "division": {
          "pk": 313,
          "url": "http://localhost:8000/api/division/313/",
          "name": "science",
          "number": "2"
        },
        "tags": [
          {
           "name": "finance"
          }
        ],
        "city": {
          "pk": 2686,
          "name": "New York City",
          "region": "New York",
          "country": "United States"
        }
      }
* GET /api/countries/
* GET /api/countries/{id}
    * {"pk":376,"url":"http://localhost:8000/api/divisions/376/","name":"Mixed","number":"1"}
