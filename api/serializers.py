from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()
    city = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print("instance", instance)
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance
