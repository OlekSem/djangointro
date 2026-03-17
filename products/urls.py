from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path("upload_temp_image/", views.upload_temp_image, name="upload_temp_image"),
    path("delete-temp-image/", views.delete_temp_image, name="delete_temp_image"), 
]