import random

# https://docs.djangoproject.com/en/2.2/ref/contrib/postgres/fields/
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Board(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    mines = models.IntegerField()
    data = ArrayField(ArrayField(models.IntegerField()), null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Board, self).save(*args, **kwargs)

        if not self.data:
            self.data = self._initialize_matrix()
            self.save()

    def _initialize_matrix(self):
        matrix = []

        for j in range(0, self.y):
            row = []
            for i in range(0, self.x):
                c = Cell.objects.create(board=self)
                row.append(c.pk)
            matrix.append(row)

        self._fill_with_mines(matrix)

        return matrix

    def _fill_with_mines(self, matrix):
        count = self.mines
        while count:
            x = random.randint(0, self.x - 1)
            y = random.randint(0, self.y - 1)

            c = Cell.objects.get(pk=matrix[y][x])
            if not c.is_mine:
                c.is_mine = True
                c.save()
                count -= 1

    def get_cell(self, x, y):
        if x is None or y is None:
            raise Exception('Both coordinates are required')

        try:
            cell_pk = self.data[y][x]
        except IndexError as e:
            raise Exception('Coordinates given are out of board index range')

        cell = Cell.objects.get(pk=cell_pk)

        return cell


class Cell(models.Model):
    board = models.ForeignKey('Board', on_delete=models.SET_NULL, null=True)

    HIDE = 'hide'
    REVEAL = 'reveal'
    FLAG =  'flag'
    STATE = [
        (HIDE, '0'),
        (REVEAL, '1'),
        (FLAG, '!')
    ]
    state = models.CharField(max_length=6, choices=STATE, default=HIDE)
    is_mine = models.BooleanField(default=False)

    def _get_my_position(self):
        coordinates = {
            'x': None,
            'y': None
        }

        for index, row in enumerate(self.board.data):
            if self.pk in row:
                coordinates['y'] = index
                coordinates['x'] = row.index(self.pk)
                break

        return coordinates

    def reveal(self):
        self.state = self.REVEAL
        self.save()

    def flag(self):
        if self.state != self.FLAG:
            self.state = self.FLAG
        else:
            self.state = self.HIDE
        self.save()
