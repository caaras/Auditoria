from django.contrib import admin
from django.urls import path, include

from webapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/email/', login_email, name='login_email'),
    path('login/password/', login_password, name='login_password'),
    path('', index, name='index'),
    path('captcha/', include('captcha.urls')),
    path('register/', register, name='register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('log_out/', log_out, name='log_out'),
]


