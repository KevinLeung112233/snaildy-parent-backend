from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid


class SubscriptionPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('monthly', '月費'),
        ('annual', '年費'),
        ('lifetime', '終身'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="方案編號"
    )
    name = models.CharField(max_length=100, verbose_name="方案名稱")  # Plan name
    description = models.TextField(verbose_name="方案描述")  # Plan description
    billing_cycle = models.CharField(
        max_length=20,
        choices=PLAN_TYPE_CHOICES,
        default='monthly',
        verbose_name="計費週期"
    )  # Billing frequency
    duration_days = models.PositiveIntegerField(
        verbose_name="有效天數")  # Duration in days
    # JSON field for plan features
    features = models.JSONField(default=dict, verbose_name="方案功能")
    is_active = models.BooleanField(
        default=True, verbose_name="是否啟用")  # Active status

    class Meta:
        verbose_name = "訂閱方案"
        verbose_name_plural = "訂閱方案"

    def __str__(self):
        return self.name


class SubscriptionPlanPrice(models.Model):
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name='tier_prices',
        verbose_name="訂閱方案"
    )
    member_tier = models.ForeignKey(
        'accounts.MemberTier',
        on_delete=models.CASCADE,
        verbose_name="會員等級"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="價格")  # Price for this tier

    class Meta:
        verbose_name = "訂閱方案價格"
        verbose_name_plural = "訂閱方案價格"
        # Ensure one price per tier per plan
        unique_together = ('plan', 'member_tier')

    def __str__(self):
        return f"{self.plan.name} - {self.member_tier.name}: {self.price}"


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', '有效'),
        ('expired', '已過期'),
        ('canceled', '已取消'),
        ('past_due', '逾期未付'),
    ]

    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name="會員"
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        verbose_name="訂閱方案"
    )
    start_date = models.DateTimeField(
        default=timezone.now, verbose_name="開始日期")
    end_date = models.DateTimeField(verbose_name="結束日期")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="狀態"
    )
    auto_renew = models.BooleanField(default=True, verbose_name="自動續訂")
    payment = models.ForeignKey(
        'payment.Payment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="關聯付款"
    )
    trial_start = models.DateTimeField(
        null=True, blank=True, verbose_name="試用開始")
    trial_end = models.DateTimeField(
        null=True, blank=True, verbose_name="試用結束")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "訂閱紀錄"
        verbose_name_plural = "訂閱紀錄"

    def __str__(self):
        return f"{self.user} - {self.plan}"

    def is_active(self):
        return self.status == 'active' and self.end_date > timezone.now()

    def days_remaining(self):
        return (self.end_date - timezone.now()).days if self.is_active() else 0

    def is_trial_period(self):
        if self.trial_start and self.trial_end:
            now = timezone.now()
            return self.trial_start <= now <= self.trial_end
        return False
