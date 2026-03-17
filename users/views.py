from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .utils import save_custom_image

# Create your views here.
# Create your views here.
def register(request):
    if request.method == 'POST':
        # print("---Зберігаємо дані користувача---")
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                if 'email' in form.cleaned_data:
                    user.username = form.cleaned_data['email']
                if 'image' in request.FILES:
                    image = request.FILES.get("image")
                    user.image_small = save_custom_image(image, size=(300,300), folder="small")
                    user.image_medium = save_custom_image(image, size=(800,800), folder="medium")
                    user.image_large = save_custom_image(image, size=(1200,1200), folder="large")
                user.save()
                login(request, user)
                return redirect('homepage')
            except Exception as e:
                messages.error(request, f"Щось пішло не так: {str(e)}")
        else:
            messages.success(request, 'Виправте помилки у формі')
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data = request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('homepage')
    else:
        form = CustomUserLoginForm()
    
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('homepage')