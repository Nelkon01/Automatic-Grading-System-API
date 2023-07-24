from django.urls import path

from home import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginViews.as_view(), name='login'),
    path('user', views.UserViews.as_view(), name='user'),
]
