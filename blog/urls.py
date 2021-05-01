from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('send_email/', views.sendEmail, name="send_email"),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('downloads/', views.downloads,name='downloads'),

    path('password_reset/',
     auth_views.PasswordResetView.as_view(template_name="blog/password_reset.html"), name="reset_password"),
    path('password_reset_done/',
     auth_views.PasswordResetDoneView.as_view(template_name="blog/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="blog/password_reset_confirm.html"), name = "password_reset_confirm"),
    path('password_reset_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name="blog/password_reset_complete.html"), name="password_reset_complete"),
]
