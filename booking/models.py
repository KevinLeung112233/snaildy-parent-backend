from django.conf import settings
from django.db import models

# Import Service and TimeSlot from service app
from service.models import Service, TimeSlot


class BookingStatus(models.Model):
    status = models.CharField(max_length=50, unique=True, verbose_name="狀態")

    class Meta:
        verbose_name = "預約狀態"
        verbose_name_plural = "預約狀態"

    def __str__(self):
        return self.status


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="會員"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name="服務"
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        verbose_name="時段"
    )
    status = models.ForeignKey(
        BookingStatus,
        on_delete=models.PROTECT,
        verbose_name="預約狀態"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "預約"
        verbose_name_plural = "預約"

    def __str__(self):
        return f"預約: {self.user} - {self.service.name} @ {self.time_slot.start_datetime} ({self.status})"
