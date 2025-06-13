from django.db import models
from student.models import Student


class HollandCode(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Student", related_name='holland_codes', null=True)
    first_code = models.CharField(
        max_length=10, verbose_name="First Code")  # Mandatory
    second_code = models.CharField(
        max_length=10, verbose_name="Second Code")  # Mandatory
    third_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Third Code")  # Optional

    date = models.DateField(blank=True, null=True,
                            verbose_name="日期")  # Optional

    class Meta:
        verbose_name = "HollandCode"
        verbose_name_plural = "HollandCode"

    def __str__(self):
        codes = [self.first_code, self.second_code]
        if self.third_code:
            codes.append(self.third_code)
        return f"{self.student_id} - " + " / ".join(codes)
