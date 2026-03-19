from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ProductImage
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import JsonResponse
import uuid
import json
import logging
from .models import Product

# Create your views here.
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)

        for img in product.images.all():
            if img.image:
                img.image.delete(save=False)
            img.delete()

        product.delete()

    except Product.DoesNotExist:
        pass

    return redirect('products:show_products')

def show_products(request):
    products = Product.objects.prefetch_related("images").all()
    return render(request, 'products.html', {'products': products})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            try:
                product = form.save()

                # 🔥 handle images (same logic as add)
                raw_ids = request.POST.getlist("images")

                seen = set()
                image_ids = []
                for img_id in raw_ids:
                    if img_id not in seen:
                        seen.add(img_id)
                        image_ids.append(img_id)

                # existing images
                existing_images = product.images.all()

                # remove images not in submitted list
                for img in existing_images:
                    if str(img.id) not in image_ids:
                        img.image.delete(save=False)
                        img.delete()

                # attach new images
                for index, image_id in enumerate(image_ids):
                    img = ProductImage.objects.get(id=image_id)
                    img.product = product
                    img.is_temp = False
                    img.order = index
                    img.save()

                messages.success(request, "Product updated successfully")
                return redirect("products:show_products")

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = ProductForm(instance=product)

    return render(request, "edit_product.html", {
        "form": form,
        "product": product
    })

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            try:
                product = form.save()

                raw_ids = request.POST.getlist("images")

                seen = set()
                image_ids = []
                for img_id in raw_ids:
                    if img_id not in seen:
                        seen.add(img_id)
                        image_ids.append(img_id)

                for index, image_id in enumerate(image_ids):
                    try:
                        img = ProductImage.objects.get(id=image_id)

                        img.product = product
                        img.is_temp = False
                        img.priority = index
                        img.save()

                    except ProductImage.DoesNotExist:
                        continue

                messages.success(request, "Product created successfully")
                return redirect("products:show_products")

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

        else:
            messages.error(request, "Form is invalid")

    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})

@csrf_exempt
def upload_temp_image(request):
    if request.method == "POST":
        file_key = list(request.FILES.keys())[0]
        image_file = request.FILES[file_key]

        img = ProductImage()
        img_image = Image.open(image_file)
        if img_image.mode in ("RGBA", "P"):
            img_image = img_image.convert("RGB")

        filename = f"{uuid.uuid4().hex}.webp"
        buffer = BytesIO()
        img_image.save(buffer, format="WEBP")
        buffer.seek(0)
        img.image.save(filename, ContentFile(buffer.read()), save=True)
        
        return JsonResponse({"file_id": img.id})
    
@csrf_exempt
def delete_temp_image(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            file_id = data.get("file_id")

            img = ProductImage.objects.get(id=file_id)

            # delete file from storage
            if img.image:
                img.image.delete(save=False)

            # delete DB record
            img.delete()

            return JsonResponse({"status": "ok"})
        except ProductImage.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Image not found"})
    
    return JsonResponse({"status": "error"})