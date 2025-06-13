from django.db import models


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('physical', '實體商品'),
        ('virtual', '虛擬商品'),
    ]

    name = models.CharField(
        max_length=255, verbose_name="商品名稱")  # Product name
    description = models.TextField(
        blank=True, verbose_name="商品描述")  # Product description
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default='physical',
        verbose_name="商品類型"
    )  # Type: physical or virtual
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="價格")  # Price of the product
    # Stock quantity, null for virtual goods
    stock = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="庫存數量")
    sku = models.CharField(max_length=100, unique=True,
                           verbose_name="庫存單位")  # Stock keeping unit
    # Whether product is active/available
    is_active = models.BooleanField(default=True, verbose_name="是否上架")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="建立時間")  # Creation timestamp
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="更新時間")  # Last update timestamp

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品列表"

    def __str__(self):
        return self.name

    def is_in_stock(self):
        # For physical products, check stock availability; virtual goods are always in stock
        if self.product_type == 'virtual':
            return True
        return self.stock is not None and self.stock > 0
