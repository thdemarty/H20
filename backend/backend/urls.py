from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('se-connecter/', LoginView.as_view(), name='login'),
    path('se-deconnecter/', logout_then_login, name='logout'),
    path('', include('accounts.urls', namespace="accounts")),
]
