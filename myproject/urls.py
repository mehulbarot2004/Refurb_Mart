"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('admin/', admin.site.urls),
    path("", views.indexpage),
    path('contact',views.contactpage),
    path('shop-3-column',views.shop3),
    path('shop-4-column',views.shop4),
    path('addproduct',views.addproductpage),
    path('new',views.newpage),
    path('product',views.productpage),
    path("addproduct",views.productpage),
    path("fetchadddata",views.fetchadddata),
    path("singleproduct/<int:id>",views.single_productpage),
    path("single-product-variable/<int:id>",views.single_product_variablepage),
    path("login", views.loginpage),
    path("my-account",views.myaccountpage),
    path("cart",views.cartpage),
    path("fetchregister",views.fetchregister),
    path("fetchlogin", views.fetchlogin),
    path("contact",views.contactpage),
    path("about",views.aboutpage),
    path("manageproduct",views.manageproductpage),
    path("logout",views.logout),
    path("deleteproduct/<int:id>", views.deletepage),
    path("insertintocart", views.insertintocart),
    path("deleteitem/<int:id>", views.deleteitem),
    path("editproduct/<int:id>",views.editproduct),
    path("updateproduct",views.updateproduct),
    path("updatelogin",views.updatelogin),
    path("editlogin",views.editlogin),
    path('placeorder', views.placeorder),
    path('yourordersingle/<int:id>',views.yourordersingle),
    path("insertintocartrefurbish",views.insertintocartrefurbish),
    path('payment-success', views.payment_success),
     path("searchproduct", views.search_product_view, name="searchproduct"),
    path("contactfetch",views.contactfetch),
    path("",views.shop4),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
