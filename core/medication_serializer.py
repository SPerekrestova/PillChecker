from rest_framework import serializers

from MedsRecognition.models import Medication


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["id", "title", "active_ingredients", "profile"]
