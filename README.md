# RESTful API for a minesweeper game

## Actions supported
* Create a game: The user has to initiate the game, indicating the size of the grid and how many mines to include (the mines are placed randomly)

* "Flag" a cell as containing a mine: The user can "flag" a given cell indicating that there's a mine in there

* "Reveal" a cell: The user can decide to reveal a cell. If there's a mine in there, he/she lost

* Get the board: Just returns the entire board with the revealed positions and the flags

## Stack used
* Django
* Django Rest Framework
* PostgreSQL

> This is a local project; please set up a postgres db and overwrite the settings in app/settings.py, sorry.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'minesweeperdb',
        'USER': 'minesweeperuser',
        'PASSWORD': 'minesweeperpassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

## Project folders structure

```
/api/ -> DRF
/app/ -> project settings
/apps/ -> project apps
```

## Run the project

```
pipenv install
pipenv shell
./manage.py migrate
./manage.py runserver
```

## Run tests

```
./manage.py test api.tests
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
