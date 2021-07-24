from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
urlpatterns = [
    # path('', views.navbar, name = "navbar"),
    path('',views.index,name='Index'),
    path('my-profile/',views.my_profile, name='my-profile'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)