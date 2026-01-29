from django.utils import timezone
from rest_framework import serializers

from apps.base.serializers import CitySerializer
from apps.slots.serializers import SlotSerializer

from .models import Cinema


class CinemaSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Cinema
        fields = [
            "id",
            "name",
            "location",
            "rows",
            "seats_per_row",
            "city",
        ]


class CinemaSlotSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    slots = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = [
            "id",
            "name",
            "location",
            "rows",
            "seats_per_row",
            "city",
            "slots",
        ]

    def get_slots(self, obj):
        active_slots = obj.slots.filter(date_time__gte=timezone.now()).order_by(
            "date_time"
        )

        return SlotSerializer(active_slots, many=True).data
