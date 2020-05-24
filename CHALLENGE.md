# Django Backend Interview - Minesweeper

![Minesweeper](http://minesweeperonline.com/og_image.jpg)

Your job is to design the RESTful API for a minesweeper game. We're leaving a lot of open ends here so you can make your own decisions. You can assume that there's a frontend (or mobile) app already designed and it needs to connect to your API.

Preferably, you should use Django and Django Rest Framework for it. Our preferred database is PostgreSQL.

Make your project Open Source and upload it to your preferred version control platform (Github, GitLab, etc).

## Required

Here are the describe methods. You MUST include tests for all these methods, and ideally for any other functionality you include

### API Methods

##### 1.a Create a game

Somehow the user has to initiate a game, indicating the size of the grid and how many mines to include. You can place mines randomly.

##### 1.b "Flag" a cell as containing a mine

The user can "flag" a given cell indicating that there's a mine in there.

##### 1.c "Reveal" a cell

The user can decide to reveal a cell. If there's a mine in there, the game ends and you have to indicate it.

##### 1.d Get the board.

This is the simplest method, just returns the entire board with the revealed positions and the flags.

### Deployment

Deploy your app using your favorite setup and document the process so we can understand it.

## Optional Topics

Do these if you have enough time and the challenge is interesting enough.

##### Dockerize your app

Create a Dockerfile that we can use to run and test your app.

##### Show number of mines surrounding the area

This is a heavy algorithmic task, so don't worry if you don't want to do it. The GET board method can show also how many mines are surrounding each cell, like a traditional minesweeper game.

##### Include a GraphQL API

Migrate your REST API to GraphQL.

##### Improve storage

There might be ways to optimize storage using caches. If you can find any, it'd be interesting to see it!
