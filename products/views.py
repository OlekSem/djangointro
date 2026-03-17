from django.shortcuts import render, redirect
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

# Create your views here.
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
                return redirect("product_list")

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