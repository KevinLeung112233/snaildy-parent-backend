from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError


class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name="機構名稱")
    phone = models.CharField(max_length=20, blank=True, verbose_name="電話")
    website = models.URLField(blank=True, verbose_name="網站")
    contact = models.CharField(max_length=255, blank=True, verbose_name="聯絡人")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "機構"
        verbose_name_plural = "機構"


class ServiceType(models.Model):
    name = models.CharField(max_length=100, verbose_name="服務類型名稱")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "服務類型"
        verbose_name_plural = "服務類型"


class ServiceStatus(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    status = models.CharField(max_length=50, unique=True, verbose_name="狀態")
    display_name = models.CharField(
        max_length=50, unique=True, null=True, blank=True, verbose_name="顯示名稱"
    )

    def __str__(self):
        return f"{self.status} - {self.display_name}"

    class Meta:
        verbose_name = "服務狀態"
        verbose_name_plural = "服務狀態"


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="服務名稱")
    detail = CKEditor5Field(blank=True, verbose_name="詳細內容")
    price = models.IntegerField(verbose_name="價格")
    deposit_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="訂金(%)",
    )
    price_desc = models.TextField(blank=True, verbose_name="價格說明")
    location = models.CharField(max_length=255, verbose_name="地點")
    type = models.ForeignKey(
        ServiceType, on_delete=models.PROTECT, verbose_name="類型", null=True, blank=True,
    )
    capacity = models.TextField(blank=True, verbose_name="人數 (e.g. 12人)")
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name="機構"
    )
    mentors = models.ManyToManyField(
        'mentor.Mentor', blank=True, verbose_name="導師")  # Changed here
    status = models.ForeignKey(
        ServiceStatus, on_delete=models.PROTECT, verbose_name="狀態"
    )
    promote_label = models.CharField(
        max_length=255, blank=True, verbose_name="推廣標籤"
    )

    expiry_date = models.DateField(null=True, blank=True, verbose_name="截止日期")
    period_start = models.DateField(
        null=True, blank=True, verbose_name="活動開始日期")
    period_end = models.DateField(null=True, blank=True, verbose_name="活動結束日期")

    min_selection = models.PositiveIntegerField(
        default=1, verbose_name="最少選擇時段"
    )
    max_selection = models.PositiveIntegerField(
        default=1, verbose_name="最多選擇時段"
    )

    free_accompanying_children = models.PositiveIntegerField(
        default=1, verbose_name="免費可同行的子女數"
    )
    extra_child_fee = models.IntegerField(default=0, verbose_name="超過的子女每位收費")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "服務"
        verbose_name_plural = "服務"


class TimeSlot(models.Model):
    STATUS_CHOICES = [
        ('available', '可預約'),
        ('unavailable', '不可預約'),
        ('full', '已額滿'),
        ('in-progress', '進行中'),
        ('finished', '已完結'),
        ('cancelled', '已取消'),
        ('postponed', '延期'),
    ]

    service = models.ForeignKey(
        Service,
        related_name='time_slots',
        on_delete=models.CASCADE,
        verbose_name="服務",
    )
    start_datetime = models.DateTimeField(
        verbose_name="開始時間", null=True, blank=True,
    )
    end_datetime = models.DateTimeField(
        verbose_name="結束時間", null=True, blank=True,
    )

    capacity = models.PositiveIntegerField(verbose_name="人數")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="狀態"
    )
    current_headcount = models.PositiveIntegerField(
        editable=True, default=0, verbose_name="現時人數"
    )

    class Meta:
        unique_together = ('service', 'start_datetime')
        ordering = ['start_datetime']
        verbose_name = "時段"
        verbose_name_plural = "時段"

    def clean(self):
        if self.end_datetime and self.start_datetime and self.end_datetime <= self.start_datetime:
            raise ValidationError("結束時間必須晚於開始時間")

    def __str__(self):
        if self.start_datetime:
            start_str = self.start_datetime.strftime('%Y-%m-%d %H:%M')
        else:
            start_str = "未設定開始時間"
        return f"{self.service.name} - {start_str}"
