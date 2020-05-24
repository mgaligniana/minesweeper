from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.minesweeper.models import Board, Cell


class MinesweeperTests(APITestCase):
    def test_create_board(self):
        """
        Create new board
        """
        url = reverse('boards-list')
        data = {
            'x': 3,
            'y': 3,
            'mines': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.count(), 1)
        self.assertEqual(Board.objects.get().x, 3)
        self.assertEqual(Board.objects.get().y, 3)
        self.assertEqual(Board.objects.get().mines, 3)
        self.assertEqual(Board.objects.get().data, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_retrieve_board(self):
        """
        Get board
        """
        board = Board.objects.create(x=3, y=3, mines=3)
        url = reverse('boards-detail', args=[board.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']])

    def test_flag_cell(self):
        """
        Flag a cell
        """
        board = Board.objects.create(x=3, y=3, mines=3)
        url = reverse('boards-flag', args=[board.pk])

        # error
        data = {
            'x': 0
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Both coordinates are required'})

        # error
        data = {
            'x': 1234,
            'y': 1234
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Coordinates given are out of board index range'})

        # success
        data = {
            'x': 0,
            'y': 0
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': 'Flagged!'})

        # Get the board
        url = reverse('boards-detail', args=[board.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, [['!', '0', '0'], ['0', '0', '0'], ['0', '0', '0']])

    def test_reveal_cell(self):
        """
        Reveal a cell
        """
        board = Board.objects.create(x=3, y=3, mines=0)  # 0 mines to don't have possibility of lost
        url = reverse('boards-reveal', args=[board.pk])

        # error
        data = {
            'x': 0
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Both coordinates are required'})

        # error
        data = {
            'x': 1234,
            'y': 1234
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Coordinates given are out of board index range'})

        # success
        data = {
            'x': 0,
            'y': 0
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': 'Revealed!'})

        # Get the board
        url = reverse('boards-detail', args=[board.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, [['1', '0', '0'], ['0', '0', '0'], ['0', '0', '0']])

    def test_win(self):
        board = Board.objects.create(x=3, y=3, mines=3)
        mines = Cell.objects.filter(board=board.pk, is_mine=True)
        url = reverse('boards-flag', args=[board.pk])

        for mine in mines:
            response = self.client.patch(url, mine._get_my_position(), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'notification': 'You won!'})

    def test_lost(self):
        board = Board.objects.create(x=3, y=3, mines=3)
        mine = Cell.objects.filter(board=board.pk, is_mine=True).first()
        url = reverse('boards-reveal', args=[board.pk])
        response = self.client.patch(url, mine._get_my_position(), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'notification': 'You lost!'})
