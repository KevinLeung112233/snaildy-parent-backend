from rest_framework import serializers
from .models import Student, Grade
from school.models import School


class StudentCreateSerializer(serializers.ModelSerializer):
    grade = serializers.SlugRelatedField(
        slug_field='id',  # since Grade's PK is a string id
        queryset=Grade.objects.all(),
        required=False,
    )
    school = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all(),
        required=False,
    )

    class Meta:
        model = Student
        fields = ['strn', 'id_no', 'chinese_name', 'english_name',
                  'grade', 'date_of_birth', 'school']
