from .views import login, logout
from rest_framework.urlpatterns import path

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]
