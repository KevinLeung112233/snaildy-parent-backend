from django.conf import settings
from django.db import models


class Mentor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mentor_profile',
        verbose_name="使用者",
        null=True
    )
    # phone field removed, use user.phone_number instead

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "導師"
        verbose_name_plural = "導師"
