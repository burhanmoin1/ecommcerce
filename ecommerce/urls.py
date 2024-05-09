from django.contrib import admin
from django.urls import path
from brand.views import *
from superuser.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('brandform/', brandform, name='brandform'),
    path('addsuperuser/', addsuperuser, name='addsuperuser'),
    path('loginsuperuser/', loginsuperuser, name='loginsuperuser'),
    path('adminsessionchecker/', adminsessionchecker, name='adminsessionchecker'),
    path('brandaccount/', BrandFormView.as_view(), name='BrandFormViewlist'),
    path('brandaccount/<str:brand_id>/', BrandFormView.as_view(), name='BrandFormView'),
]
