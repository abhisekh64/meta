from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("add-campaign", views.Add_campaign.as_view(), name="add_campaign"),
    path("add-set", views.Add_set.as_view(), name="add_set"),
    
    path("auth/meta/", views.meta_auth, name="meta_auth"),
    path("auth/meta/callback/", views.meta_callback, name="meta_callback"),
]
