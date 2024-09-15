from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('requestion/', views.requestion, name='requestion'),
    path('requestions_list/', views.requestions_list, name='requestions_list'),
    path('requestion/<int:pk>/', views.requestion_detail, name='requestion_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


