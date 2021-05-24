from django.urls import path

from users.views import RegistrationView, LoginView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name='login'),
]
