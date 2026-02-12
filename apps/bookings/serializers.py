from rest_framework.serializers import ModelSerializer

from .models import Seat


class SeatSerializer(ModelSerializer):
    class Meta:
        model = Seat
        fields = ["row", "number"]
