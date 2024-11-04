from django.urls import path
from .views import product_list, add_product
from django.urls import path
from .views import product_list, sell_products  # นำเข้า view ที่ต้องการ
from . import views
from .views import sell_products, edit_product  # เพิ่ม import edit_product



urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),  # เพิ่มเส้นทางสำหรับเพิ่มสินค้า
    path('sell_products/', sell_products, name='sell_products'),  # เพิ่ม URL สำหรับการตัดสต็อก
    path('delete_selected_products/', views.delete_selected_products, name='delete_selected_products'),
    path('edit_product/<str:order_number>/', edit_product, name='edit_product'),  # เช็คว่า URL นี้ถูกต้อง
    
    
]