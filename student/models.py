from django.db import models
from django.conf import settings
import uuid


class Grade(models.Model):
    # Using string ID like 'primary_1', 'secondary_1'
    id = models.CharField(max_length=50, primary_key=True, verbose_name="編號")
    name = models.CharField(max_length=100, verbose_name="年級")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "年級"
        verbose_name_plural = "年級"


class Student(models.Model):
    # Strong, secure, unique ID using UUID4
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="編號"
    )
    strn = models.CharField(max_length=255, blank=True,
                            null=True, verbose_name="STRN", unique=True)
    id_no = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name="HKID", unique=True)

    chinese_name = models.CharField(max_length=255, verbose_name="中文姓名")
    english_name = models.CharField(max_length=255, verbose_name="英文姓名")
    school = models.ForeignKey(
        'school.School',
        on_delete=models.PROTECT,
        related_name="students",
        verbose_name="學校",
        blank=True
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.PROTECT,
        related_name="students",
        verbose_name="就讀年級",
        blank=True
    )
    date_of_birth = models.DateField(verbose_name="出生日期",
                                     blank=True)

    # Add reference to custom user
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name="家長",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.chinese_name} ({self.english_name})"

    class Meta:
        verbose_name = "學生"
        verbose_name_plural = "學生"


class StudentSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='student_sessions',
        on_delete=models.CASCADE,
        verbose_name="用戶"
    )
    student = models.ForeignKey(
        'Student',  # or your app label e.g. 'app_name.Student'
        related_name='sessions',
        on_delete=models.CASCADE,
        null=True, blank=True,  # optional if session might not always link to a student
        verbose_name="學生"
    )
    session_id = models.CharField(
        max_length=255, unique=True, verbose_name="SessionId")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    def __str__(self):
        return f"Session {self.session_id} for user {self.user}"

    class Meta:
        verbose_name = "Student Session"
        verbose_name_plural = "Student Session"
