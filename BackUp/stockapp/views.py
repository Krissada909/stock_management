from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # บันทึกสินค้าใหม่
            return redirect('product_list')  # เปลี่ยนเส้นทางไปยังหน้า product_list
    else:
        form = ProductForm()
    return render(request, 'stockapp/add_product.html', {'form': form})


def product_list(request):
    products = Product.objects.all()  # ดึงข้อมูลสินค้าทั้งหมด
    return render(request, 'stockapp/product_list.html', {'products': products})




from django.shortcuts import get_object_or_404, redirect
from .models import Product

def sell_products(request):
    if request.method == 'POST':
        order_numbers = request.POST.getlist('product_ids')  # รับค่า order ที่เลือก
        for order_number in order_numbers:
            if order_number:  # ตรวจสอบว่า order_number ไม่ว่าง
                try:
                    product = Product.objects.get(order=order_number)  # เข้าถึง Product โดยใช้ order
                    if product.quantity > 0:  # ตรวจสอบว่าสินค้ามีในสต็อก
                        product.sold_quantity += 1  # เพิ่มจำนวนที่ขาย
                        product.quantity -= 1  # ลดจำนวนสินค้าในสต็อก
                        product.save()  # บันทึกการเปลี่ยนแปลง
                except Product.DoesNotExist:
                    continue  # ข้ามหากไม่พบสินค้า

        return redirect('product_list')  # กลับไปที่หน้ารายการสินค้า

    return render(request, 'product_list.html')  # หากไม่ใช่ POST ให้แสดงรายการสินค้า


def delete_selected_products(request):
    if request.method == "POST":
        product_ids = request.POST.getlist('product_ids')
        if product_ids:
            # ใช้ order แทน id
            Product.objects.filter(order__in=product_ids).delete()
        return redirect('product_list')  # กลับไปที่หน้าขายสินค้า