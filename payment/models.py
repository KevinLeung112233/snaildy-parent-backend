from django.db import models
from booking.models import Booking
from coupon.models import Coupon


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', '處理中'),
        ('completed', '已完成'),
        ('failed', 'Failed'),
        ('refunded', '已退款'),
    ]
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='payment', verbose_name="預約")
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='payment', verbose_name="預約")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="金額")
    currency = models.CharField(
        max_length=10, default='HKD', verbose_name="貨幣")
    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="付款狀態", db_index=True)
    transaction_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="交易編號", db_index=True)
    payment_method = models.CharField(
        max_length=100, blank=True, verbose_name="付款方式")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name="使用的優惠券"
    )

    class Meta:
        verbose_name = "付款"
        verbose_name_plural = "付款紀錄"

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.status}"

    @property
    def is_successful(self):
        return self.status == 'completed'
