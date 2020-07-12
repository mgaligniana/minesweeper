# RESTful API for a minesweeper game

Here is the implementation for bullets: 1A, 1B, 1C and 1D defined in the [challenge file](https://github.com/mgaligniana/minesweeper/blob/master/CHALLENGE.md)

## Stack used
* Django
* Django Rest Framework
* PostgreSQL

## Project folders structure

```
/api/ -> DRF
/app/ -> project settings
/apps/ -> project apps
```

## Run the project

```
docker-compose build
docker-compose up
docker-compose run web python manage.py migrate
```

## Run tests

```
docker-compose run web python manage.py test
```

## API endpoints documentation

```
METHOD
POST

PATH
/api/v1/boards/

PAYLOAD
{
    "x": 3,
    "y": 3,
    "mines": 3
}

RESPONSE
{
    "x": 3,
    "y": 3,
    "mines": 3,
    "data": [  # returns cell ids
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
}

```

```
METHOD
GET

PATH
/api/v1/boards/{id}/

RESPONSE
[  # returns the grid painted for the user
    [0, 0, 0],  # 0 == cell not actived
    [0, 1, 0],  # 1 == cell revelead
    [0, 0, !]   # ! == cell flagged
]

```

```
METHOD
PATCH

PATH
/api/v1/boards/{id}/flag/

PAYLOAD
{
    "x": 0,
    "y": 0
}
```

```
METHOD
PATCH

PATH
/api/v1/boards/{id}/reveal/

PAYLOAD
{
    "x": 0,
    "y": 0
}
```
