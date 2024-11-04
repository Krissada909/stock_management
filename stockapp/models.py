from django.db import models

class Product(models.Model):
    # ฟิลด์สำหรับลำดับรายการ
    order = models.AutoField(primary_key=True)  # ลำดับรายการ (Primary Key)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # ฟิลด์สำหรับอัปโหลดภาพ
    date_added = models.DateField(auto_now_add=True)  # ฟิลด์วันที่เพิ่มสินค้า
    sold_quantity = models.IntegerField(default=0)  # ฟิลด์สำหรับจำนวนที่ขายไป
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ฟิลด์สำหรับน้ำหนัก
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ฟิลด์สำหรับราคารวม
    website_url = models.URLField(max_length=500, blank=True, null=True)  # ฟิลด์สำหรับเก็บ URL ของเว็บไซต์

    def remaining_stock(self):
        return self.quantity - self.sold_quantity  # คำนวณจำนวนที่เหลือ

    def calculate_total_price(self):
        self.total_price = self.price * self.sold_quantity  # คำนวณราคารวม
        self.save()  # บันทึกการเปลี่ยนแปลง

    def __str__(self):
        return self.name
