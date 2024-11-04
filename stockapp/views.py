from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
from django.shortcuts import get_object_or_404, redirect
from decimal import Decimal

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
    products = Product.objects.all()
    
    for product in products:
        # คำนวณ total_price และเก็บค่าใน attribute ชั่วคราว
        product.total_price = product.price + (product.weight * 130)
    return render(request, 'stockapp/product_list.html', {'products': products})


def sell_products(request):
    if request.method == 'POST':
        order_numbers = request.POST.getlist('product_ids')  # รับค่า order ที่เลือก
        quantities = []
        weights = []

        for order_number in order_numbers:
            if order_number:  # ตรวจสอบว่า order_number ไม่ว่าง
                try:
                    product = Product.objects.get(order=order_number)  # เข้าถึง Product โดยใช้ order
                    quantity_to_sell = int(request.POST.get(f'quantity_to_sell_{order_number}', 1))  # รับค่าจำนวนที่ต้องการขาย
                   

                    if product.quantity >= quantity_to_sell:  # ตรวจสอบว่ามีสินค้าพอ
                        product.sold_quantity += quantity_to_sell  # เพิ่มจำนวนที่ขาย
                        product.quantity -= quantity_to_sell  # ลดจำนวนสินค้าในสต็อก
                     
                        product.save()  # บันทึกการเปลี่ยนแปลง
                except Product.DoesNotExist:
                    continue  # ข้ามหากไม่พบสินค้า

        return redirect('product_list')  # กลับไปที่หน้ารายการสินค้า

    return render(request, 'product_list.html')  # หากไม่ใช่ POST ให้แสดงรายการสินค้า

def edit_product(request, order_number):
    product = get_object_or_404(Product, order=order_number)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.quantity = int(request.POST.get('quantity'))
        product.price = Decimal(request.POST.get('price'))
        product.weight = Decimal(request.POST.get('weight'))
        product.save()
        return redirect('product_list')

    return render(request, 'stockapp/edit_product.html', {'product': product})  # ระบุชื่อเส้นทางที่ถูกต้อง

def delete_selected_products(request):
    if request.method == "POST":
        product_ids = request.POST.getlist('product_ids')
        if product_ids:
            # ใช้ order แทน id
            Product.objects.filter(order__in=product_ids).delete()
        return redirect('product_list')  # กลับไปที่หน้าขายสินค้า