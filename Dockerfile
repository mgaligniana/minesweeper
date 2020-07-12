FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /minesweeper
WORKDIR /minesweeper
COPY requirements.txt /minesweeper/
RUN pip install -r requirements.txt
COPY . /minesweeper/
