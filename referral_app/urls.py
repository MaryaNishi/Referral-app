from django.urls import path

from . import views

app_name = "referral"
urlpatterns = [
    path('api/check-invite-code/', views.check_invite_code, name='check_invite_code'),
    path("", views.profile_view, name="profile"),
    path("login/", views.login_view, name="login"),
    path("authenticate/", views.get_authentication, name="authentication"),
    path("logout/", views.logout_view, name="logout"),
    path("login_user/", views.login_user, name="login_user"),
    path('api/profile/invite-users/', views.get_phone_numbers, name='invite_users'),
]
