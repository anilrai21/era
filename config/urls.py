"""sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.userprofile.views import KipaLoginView, RegisterView

urlpatterns = [
    path("this-blog/", admin.site.urls),
    path(
        "",
        include(
            ("apps.shop.urls", "apps.shop"), namespace="shop"
        ),
    ),
    path(
        "profile/",
        include(
            ("apps.userprofile.urls", "apps.userprofile"),
            namespace="profile",
        ),
    ),
    path(
        "cms/",
        include(("apps.cms.urls", "apps.cms"), namespace="cms"),
    ),
    path("register", RegisterView.as_view(), name="register_view"),
    path("login", KipaLoginView.as_view(), name="login_view"),
    path(
        "logout",
        auth_views.LogoutView.as_view(
            template_name="ecommerce/authentication/logout.html"
        ),
        name="logout_view",
    ),
    path("summernote/", include("django_summernote.urls")),
    path("api/", include(("config.urls_api", "config"), namespace="api")),
    path(r"captcha/", include("captcha.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
