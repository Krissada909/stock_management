from django.urls import path
from .views import product_list, add_product
from django.urls import path
from .views import product_list, sell_products  # นำเข้า view ที่ต้องการ
from . import views



urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),  # เพิ่มเส้นทางสำหรับเพิ่มสินค้า
    path('sell_products/', sell_products, name='sell_products'),  # เพิ่ม URL สำหรับการตัดสต็อก
    path('delete_selected_products/', views.delete_selected_products, name='delete_selected_products'),
    
]