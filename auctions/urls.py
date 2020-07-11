from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("view/<str:title>", views.listing_page, name="view"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<str:category>", views.category, name="category"),
    path("my_listings", views.my_listings, name="my_listings")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
