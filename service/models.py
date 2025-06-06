from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name="機構名稱")
    phone = models.CharField(max_length=20, blank=True, verbose_name="電話")
    website = models.URLField(blank=True, verbose_name="網站")
    contact = models.CharField(max_length=255, blank=True, verbose_name="聯絡人")

    def __str__(self):
        return self.name


class Mentor(models.Model):
    name = models.CharField(max_length=255, verbose_name="導師姓名")
    email = models.EmailField(verbose_name="電子郵件")
    phone = models.CharField(max_length=20, blank=True, verbose_name="電話")

    def __str__(self):
        return self.name


class ServiceStatus(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    status = models.CharField(max_length=50, unique=True, verbose_name="狀態")
    display_name = models.CharField(
        max_length=50, unique=True, null=True, blank=True, verbose_name="Display Name"
    )

    def __str__(self):
        return f"{self.status} - {self.display_name}"


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="服務名稱")
    detail = models.TextField(blank=True, verbose_name="詳細內容")
    price = models.IntegerField(verbose_name="價格")
    price_desc = models.TextField(blank=True, verbose_name="價格說明")
    location = models.CharField(max_length=255, verbose_name="地點")
    capacity = models.PositiveIntegerField(verbose_name="人數")
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name="機構"
    )
    mentors = models.ManyToManyField(Mentor, blank=True, verbose_name="導師")
    status = models.ForeignKey(
        ServiceStatus, on_delete=models.PROTECT, verbose_name="狀態"
    )
    promote_label = models.CharField(
        max_length=255, blank=True, verbose_name="推廣標籤")

    expiry_date = models.DateField(null=True, blank=True, verbose_name="截止日期")
    period_start = models.DateField(
        null=True, blank=True, verbose_name="活動開始日期")
    period_end = models.DateField(null=True, blank=True, verbose_name="活動結束日期")

    min_selection = models.PositiveIntegerField(default=1, verbose_name="最少選擇")
    max_selection = models.PositiveIntegerField(default=1, verbose_name="最多選擇")

    def __str__(self):
        return self.name


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
    start_datetime = models.DateTimeField(verbose_name="開始時間")
    capacity = models.PositiveIntegerField(verbose_name="人數")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="狀態"
    )
    current_headcount = models.PositiveIntegerField(
        default=0, verbose_name="現時人數")

    class Meta:
        unique_together = ('service', 'start_datetime')
        ordering = ['start_datetime']
        verbose_name = "時段"
        verbose_name_plural = "時段"

    def __str__(self):
        return f"{self.service.name} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"
