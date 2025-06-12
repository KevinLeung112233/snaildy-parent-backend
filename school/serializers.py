# serializers.py
from rest_framework import serializers
from school.models import School  # Adjust import path as needed


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name']  # include fields you want to expose
