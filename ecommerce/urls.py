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
    path('brandaccountsessionchecker/', brandaccountsessionchecker, name='brandaccountsessionchecker'),
    path('addbrandaccount/', addbrandaccount, name='addbrandaccount'),
    path('BrandAccountLogin/', BrandAccountLogin, name='BrandAccountLogin'),
    path('brandaccount/', BrandFormView, name='BrandFormViewlist'),
    path('brandaccount/<str:brand_id>/', BrandFormView, name='BrandFormView'),
    path('addprimarycategory/', AddPrimaryCategory.as_view(), name='addprimarycategory'),
    path('addsecondarycategory/', AddSecondaryCategory.as_view(), name='addsecondarycategory'),
    path('get_secondary_categories/', get_secondary_categories, name='get_secondary_categories'),
    path('brandproductsfordashboard/', BrandProductsforDashboard.as_view(), name='brandproductsfordashboard'),
    path('api/superusers/', SuperUserCreateView.as_view(), name='superuser-create'),
]
