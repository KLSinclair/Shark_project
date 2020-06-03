from django.urls import path

from . import views

urlpatterns = [
    path('', views.index), # localhost:8000
    path('login', views.login),
    path('register', views.register), # ← this URL is dependent on this method ;-)
    path('success', views.success),
    path('logout', views.logout),
]