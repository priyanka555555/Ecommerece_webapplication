from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login', views.login, name='login'),
    path('', views.register, name='register'),
    path('buyer_product/<int:pk>/', views.buyer_product, name='buyer_product'),
    path('logout/', views.logout_view, name='logout'),
    path('productlist/', views.productlist, name='productlist'),
    
    path('product/create/', views.product_create, name='product_create'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


















 
                                 