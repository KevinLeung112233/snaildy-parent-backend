from django.db import models
from django.conf import settings


class StudentSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='student_sessions', on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
