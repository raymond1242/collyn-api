from rest_framework import serializers
from warehouse.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name"]
