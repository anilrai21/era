from django.urls import include, path

urlpatterns = [
    path(
        "shop/",
        include(
            ("apps.shop.urls_api", "apps.shop"),
            namespace="shop_api",
        ),
    ),
    path(
        "profile/",
        include(
            ("apps.userprofile.urls_api", "apps.userprofile"),
            namespace="profile_api",
        ),
    ),
    path(
        "cms/",
        include(
            ("apps.cms.urls_api", "apps.cms"),
            namespace="cms_api",
        ),
    ),
]
