from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CategoryForm
from .utils import save_custom_image
from .models import Category

# Create your views here.

def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                if 'image' in request.FILES:
                    image = request.FILES.get("image")
                    category.image = save_custom_image(image, (1024, 1024), 'large')
                category.save()
                return redirect("list")
            except Exception as e:
                messages.error(request, f"Щось пішло не так: {str(e)}")
    else:
        form = CategoryForm()

    return render(request, "create_category.html", {"form": form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, "list.html", {
        "categories": categories
    })