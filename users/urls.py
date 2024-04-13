from django.urls import path
from users.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('signup/', RegisterView.as_view({
        'post': 'create'
    }), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view({
        'post': 'create'
    }), name='logout')
]
