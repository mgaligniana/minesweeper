from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.minesweeper.models import Board, Cell

from .serializers import BoardSerializer


class BoardViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):

    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Overwrite retrieve to paint the board with the cell states for the user
        """
        instance = self.get_object()

        paint = []

        for row in instance.data:
            row_aux = []
            for cell in row:
                c = Cell.objects.get(pk=cell)
                if c.state == Cell.REVEAL and c.is_mine:
                    row_aux.append('*')
                else:
                    row_aux.append(c.get_state_display())
            paint.append(row_aux)

        return Response(paint)

    @action(detail=True, methods=['patch'])
    def flag(self, request, pk=None):
        board = self.get_object()
        x = self.request.data.get('x')
        y = self.request.data.get('y')

        try:
            cell = board.get_cell(x, y)
            cell.flag()
        except Exception as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        mines = list(board.cell_set.filter(is_mine=True).values_list('pk', flat=True))
        cells_flagged = list(board.cell_set.filter(state=Cell.FLAG).values_list('pk', flat=True))

        if mines == cells_flagged:
            return Response({'notification': 'You won!'})

        return Response({'success': 'Flagged!'})

    @action(detail=True, methods=['patch'])
    def reveal(self, request, pk=None):
        board = self.get_object()
        x = self.request.data.get('x')
        y = self.request.data.get('y')

        try:
            cell = board.get_cell(x, y)
            cell.reveal()
        except Exception as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        if cell.is_mine:
            return Response({'notification': 'You lost!'})

        return Response({'success': 'Revealed!'})
