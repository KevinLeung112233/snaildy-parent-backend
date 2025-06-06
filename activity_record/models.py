import uuid
from django.db import models
from django.conf import settings


class AttendanceStatus(models.TextChoices):
    ATTENDED = 'attended', '已出席'
    ABSENT = 'absent', '缺席'
    LATE = 'late', '遲到'
    EXCUSED = 'excused', '已請假'


class StudentRecord(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )
    # Reference to Student model using string reference to avoid import issues
    student = models.ForeignKey(
        'student.Student',
        on_delete=models.CASCADE,
        related_name='activity_records',
        verbose_name="學生"
    )
    # Reference to Service and TimeSlot models via string reference
    service = models.ForeignKey(
        'service.Service',
        on_delete=models.PROTECT,
        related_name='student_records',
        verbose_name="服務"
    )
    timeslot = models.ForeignKey(
        'service.TimeSlot',
        on_delete=models.PROTECT,
        related_name='student_records',
        verbose_name="時段"
    )
    attendance = models.CharField(
        max_length=10,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.ATTENDED,
        verbose_name="出席狀況"
    )
    remark = models.TextField(blank=True, verbose_name="備註")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "學生活動紀錄"
        verbose_name_plural = "學生活動紀錄"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student} - {self.service} @ {self.timeslot} ({self.attendance})"


class ParentRecord(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )
    # Reference to custom user model for parent
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_records',
        verbose_name="家長"
    )
    service = models.ForeignKey(
        'service.Service',
        on_delete=models.PROTECT,
        related_name='parent_records',
        verbose_name="服務"
    )
    timeslot = models.ForeignKey(
        'service.TimeSlot',
        on_delete=models.PROTECT,
        related_name='parent_records',
        verbose_name="時段"
    )
    attendance = models.CharField(
        max_length=10,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.ATTENDED,
        verbose_name="出席狀況"
    )
    remark = models.TextField(blank=True, verbose_name="備註")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "家長活動紀錄"
        verbose_name_plural = "家長活動紀錄"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.parent} - {self.service} @ {self.timeslot} ({self.attendance})"


class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, verbose_name="ID")

    student_record = models.ForeignKey(
        'StudentRecord',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name="學生活動紀錄附件"
    )
    parent_record = models.ForeignKey(
        'ParentRecord',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name="家長活動紀錄附件"
    )

    file = models.FileField(
        upload_to='activity_attachments/', verbose_name="附件(圖片或影片)")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上傳時間")

    class Meta:
        verbose_name = "活動附件"
        verbose_name_plural = "活動附件"
        ordering = ['-uploaded_at']

    def __str__(self):
        if self.student_record:
            return f"Attachment for StudentRecord {self.student_record.id}"
        elif self.parent_record:
            return f"Attachment for ParentRecord {self.parent_record.id}"
        return f"Attachment {self.id}"
