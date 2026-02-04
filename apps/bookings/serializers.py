from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from apps.slots.models import Slot

from .models import Booking, Seat


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["row", "number"]


class BookingSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True)
    slot_id = serializers.IntegerField(source="slot.id")

    class Meta:
        model = Booking
        fields = [
            "id",
            "slot_id",
            "status",
            "created_at",
            "seats",
        ]


class BookingCreateSerializer(serializers.Serializer):
    slot_id = serializers.IntegerField()
    seats = SeatSerializer(many=True)

    def validate_slot_id(self, value):
        try:
            slot = Slot.objects.get(id=value)
        except Slot.DoesNotExist:
            raise serializers.ValidationError("Invalid slot") from None

        if slot.date_time < timezone.now():
            raise serializers.ValidationError("Slot is no longer active")

        return value

    def create(self, validated_data):
        user = self.context["request"].user
        slot_id = validated_data["slot_id"]
        seats_data = validated_data["seats"]

        with transaction.atomic():
            booking = Booking.objects.create(
                user=user,
                slot_id=slot_id,
                status=Booking.Status.BOOKED,
            )

            for seat in seats_data:
                seat_obj = Seat(
                    booking=booking,
                    row=seat["row"],
                    number=seat["number"],
                )
                seat_obj.save()

            booking.save()

        return booking
