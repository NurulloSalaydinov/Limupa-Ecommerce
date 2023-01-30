from django.urls import path
from .import views

app_name = 'main'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<slug:product_slug>/', views.product_detail_view, name='product_detail'),
    path('shop/', views.ProductListView.as_view(), name='shop')
]
