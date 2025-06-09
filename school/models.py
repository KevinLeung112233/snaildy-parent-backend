from django.db import models


class School(models.Model):
    class Meta:
        verbose_name = "學校"
        verbose_name_plural = "學校列表"

    # Choices for area
    AREA_CHOICES = [
        ('香港島', '香港島'),
        ('九龍', '九龍'),
        ('新界', '新界'),
        ('離島', '離島'),
    ]

    # Choices for district (example subset, add all districts you need)
    DISTRICT_CHOICES = [
        ('中西區', '中西區'),
        ('東區', '東區'),
        ('灣仔區', '灣仔區'),
        ('南區', '南區'),
        ('九龍城區', '九龍城區'),
        ('觀塘區', '觀塘區'),
        ('深水埗區', '深水埗區'),
        ('黃大仙區', '黃大仙區'),
        ('油尖旺區', '油尖旺區'),
        ('元朗區', '元朗區'),
        ('屯門區', '屯門區'),
        ('西貢區', '西貢區'),
        ('北區', '北區'),
        ('沙田區', '沙田區'),
        ('大埔區', '大埔區'),
        ('葵青區', '葵青區'),
        ('荃灣區', '荃灣區'),
        ('離島區', '離島區'),
        # Add other districts as needed
    ]

    # Choices for type
    TYPE_CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
    ]

    name_cn = models.CharField("中文名稱", max_length=255)
    name_eng = models.CharField("English Name", max_length=255)
    address = models.TextField("地址")

    district = models.CharField(
        "區域",
        max_length=20,
        choices=DISTRICT_CHOICES,
    )

    area = models.CharField(
        "地區",
        max_length=10,
        choices=AREA_CHOICES,
    )

    type = models.CharField(
        "類別",
        max_length=10,
        choices=TYPE_CHOICES,
    )

    def __str__(self):
        return self.name_cn  # or return self.name_cn
