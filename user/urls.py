from django.contrib.auth.views import LoginView
from django.urls import path, include

from user.views import signup_view, user_profile, edit_profile

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import signup_view, user_profile, edit_profile

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("profile/", user_profile, name="profile"),
    path("login/", LoginView.as_view(template_name="user/login_template.html"), name="login"),
    path("profile-edit/", edit_profile, name="edit_profile"),
    # Redirect to 'login' named URL after logout
    path('logout/', LogoutView.as_view(next_page='user:login'), name='logout')
]

app_name = "user"
