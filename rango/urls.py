from django.urls import path, include
from django.conf.urls import url
from rango import views
from registration.backends.simple.views import RegistrationView


app_name = "rango"
urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name="show_category"),
    path("add_category/", views.add_category, name="add_category"),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name="add_page"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("restricted/", views.restricted, name="restricted"),
    path("logout/", views.user_logout, name="logout"),
    path("goto/", views.track_url, name="goto"),
    path("register_profile/", views.register_profile, name="register_profile"),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    path("profiles/", views.list_profiles, name="list_profiles"),
    path("like/", views.like_category, name="like_category"),
]