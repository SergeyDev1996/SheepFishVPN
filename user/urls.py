from django.contrib.auth.views import LoginView
from django.urls import path, include

from user.views import signup_view, user_profile, edit_profile

urlpatterns = [
    path("signup/", signup_view),
    path("profile/", user_profile, name="profile"),
    path("login/", LoginView.as_view(template_name="user/login_template.html", redirect_authenticated_user=True),
         name="login"),
    path("profile-edit/", edit_profile, name="edit_profile"),
]
app_name = "user"
