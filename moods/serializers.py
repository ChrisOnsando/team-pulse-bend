from typing import Any
from rest_framework import serializers
from moods.models import Mood


class MoodSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    value = serializers.IntegerField()
    description = serializers.CharField(max_length=255)
    image_url = serializers.CharField(allow_blank=True, required=False)
    
    class Meta:
        model = Mood
        fields = ("id", "value", "description", "image_url", "created_at")
        read_only_fields = ("id", "created_at")
    
    def update(self, instance: Any, validated_data: Any) -> Any:
        instance.value = validated_data.get("value", instance.value)
        instance.description = validated_data.get("description", instance.description)
        instance.image_url = validated_data.get("image_url", instance.image_url)
        instance.save()
        return instance
