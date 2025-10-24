from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('remove/<int:image_id>/', views.remove_image, name='remove_image'),
]