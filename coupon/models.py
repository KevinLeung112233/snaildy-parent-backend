from django.db import models
from django.conf import settings
from django.utils import timezone


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True,
                            verbose_name="優惠碼")  # Coupon code
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="折扣金額")  # Fixed discount amount
    discount_percent = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="折扣百分比")  # Discount percentage
    valid_from = models.DateTimeField(
        verbose_name="有效開始日期")  # Coupon valid start date
    valid_to = models.DateTimeField(
        verbose_name="有效結束日期")  # Coupon valid end date
    active = models.BooleanField(
        default=True, verbose_name="是否啟用")  # Is the coupon active?

    quota = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="總使用次數限制")  # Total usage quota
    # Number of times coupon has been used
    used_count = models.PositiveIntegerField(default=0, verbose_name="已使用次數")

    user_quota = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="每用戶使用次數限制")  # Usage limit per user
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='coupons',
        verbose_name="指定用戶",  # Specific users allowed to use this coupon
        help_text="允許使用此優惠券的用戶，留空表示所有用戶均可使用"  # Leave blank to allow all users
    )

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        within_date = self.valid_from <= now <= self.valid_to
        under_quota = (self.quota is None) or (self.used_count < self.quota)
        return self.active and within_date and under_quota

    def can_user_use(self, user):
        if self.users.exists() and user not in self.users.all():
            return False
        # Implement per-user usage tracking logic separately
        return True
