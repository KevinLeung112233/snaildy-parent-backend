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
    id = models.PositiveSmallIntegerField(primary_key=True, verbose_name="編號")
    status = models.CharField(max_length=50, unique=True, verbose_name="狀態")

    def __str__(self):
        return self.status


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="服務名稱")
    detail = models.TextField(blank=True, verbose_name="詳細內容")
    price = models.IntegerField(verbose_name="價格")
    price_desc = models.TextField(blank=True, verbose_name="價格說明")
    location = models.CharField(max_length=255, verbose_name="地點")
    capacity = models.PositiveIntegerField(verbose_name="人數")
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name="機構")
    mentor = models.ForeignKey(
        Mentor, on_delete=models.PROTECT, verbose_name="導師")
    need_timeslot = models.BooleanField(default=False, verbose_name="需要時段")
    status = models.ForeignKey(
        ServiceStatus, on_delete=models.PROTECT, verbose_name="狀態")
    promote_label = models.CharField(
        max_length=255, blank=True, verbose_name="推廣標籤")

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    STATUS_CHOICES = [
        ('available', '可預約'),
        ('unavailable', '不可預約'),
        ('full', '已額滿'),
    ]

    service = models.ForeignKey(
        Service, related_name='time_slots', on_delete=models.CASCADE, verbose_name="服務")
    start_datetime = models.DateTimeField(verbose_name="開始時間")
    capacity = models.PositiveIntegerField(verbose_name="人數")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="狀態")
    current_headcount = models.PositiveIntegerField(
        default=0, verbose_name="現時人數")

    class Meta:
        unique_together = ('service', 'start_datetime')
        ordering = ['start_datetime']
        verbose_name = "時段"
        verbose_name_plural = "時段"

    def __str__(self):
        return f"{self.service.name} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"

    def increment_headcount(self):
        if self.current_headcount < self.capacity:
            self.current_headcount += 1
            if self.current_headcount >= self.capacity:
                self.status = 'full'
            self.save()
        else:
            raise ValueError("TimeSlot is already full")
