from rest_framework import serializers

from apps.minesweeper.models import Board


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ('pk', 'x', 'y', 'mines', 'data')
