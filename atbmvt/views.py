from django.shortcuts import render, redirect
from .forms import CategoryForm

def homepage(request):
    return render(request, "home.html")

def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_category")
    else:
        form = CategoryForm

    return render(request, "atbmvt/create_category.html", {"form": form})