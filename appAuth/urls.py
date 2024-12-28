from django.urls import path

from . import views


urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("verify/", views.VerifyUserView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("details/<int:id>/", views.UserDetailsView.as_view()),
    path("update/<int:id>", views.UserUpdateView.as_view()),
    path("delete/<int:id>/", views.UserDeleteView.as_view()),
]
