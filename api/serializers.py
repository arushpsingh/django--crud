from rest_framework import serializers

class StudentSerializer(serializers.Serialzer):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    city = models.CharField(max_length=20)