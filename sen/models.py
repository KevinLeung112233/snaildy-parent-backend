from django.db import models


class SenType(models.Model):
    """
    SEN Type examples: ASD, HI, ADHD
    """
    id = models.CharField(max_length=100, unique=True, primary_key=True,
                          verbose_name="id")
    name = models.CharField(max_length=50, unique=True,
                            verbose_name="特殊教育需求類型")

    class Meta:
        verbose_name = "特殊教育需求類型"
        verbose_name_plural = "特殊教育需求類型"

    def __str__(self):
        return self.name


class SenLevel(models.Model):
    """
    SEN Level: 輕, 中, 重
    """
    id = models.CharField(max_length=100, unique=True,
                          primary_key=True, verbose_name="id")
    name = models.CharField(max_length=10, unique=True, verbose_name="程度")

    class Meta:
        verbose_name = "程度"
        verbose_name_plural = "程度"

    def __str__(self):
        return self.name


class SenStatus(models.Model):
    """
    SEN Status: e.g. 已確認, 觀察中
    """
    id = models.CharField(max_length=100, unique=True,
                          primary_key=True, verbose_name="id")
    name = models.CharField(max_length=50, unique=True, verbose_name="狀態")

    class Meta:
        verbose_name = "狀態"
        verbose_name_plural = "狀態"

    def __str__(self):
        return self.name


class Sen(models.Model):
    """
    Main SEN record referencing student, SEN type, level, and status.
    """
    student = models.ForeignKey('student.Student',
                                on_delete=models.CASCADE, verbose_name="Student", related_name='sens', null=True)
    sen_type = models.ForeignKey(
        SenType, on_delete=models.PROTECT, verbose_name="特殊教育需求類型")
    level = models.ForeignKey(
        SenLevel, on_delete=models.PROTECT, verbose_name="程度")
    status = models.ForeignKey(
        SenStatus, on_delete=models.PROTECT, verbose_name="狀態")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "特殊教育需求"
        verbose_name_plural = "特殊教育需求"

    def __str__(self):
        return f"{self.student_id} - {self.sen_type.name} ({self.level.name}) [{self.status.name}]"
