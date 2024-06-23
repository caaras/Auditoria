from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import EmailForm, PasswordForm, CustomUserCreationForm
from .models import CustomUser


# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register/register.html', {'form': form})


def login_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                request.session['user_id'] = user.id
                return redirect('login_password')
            except CustomUser.DoesNotExist:
                form.add_error('email', 'El correo electrónico no existe.')
    else:
        form = EmailForm()
    return render(request, 'login/login_email.html', {'form': form})


def login_password(request):
    if 'user_id' not in request.session:
        return redirect('login_email')

    user_id = request.session.get('user_id')
    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(request, username=user.email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error('password', 'Contraseña incorrecta.')
    else:
        form = PasswordForm()
    return render(request, 'login/login_password.html', {'form': form, 'email': user.email})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        if 'update_name' in request.POST:
            new_full_name = request.POST['full_name']
            request.user.full_name = new_full_name
            request.user.save()
            messages.success(request, 'Nombre actualizado con éxito a {}'.format(new_full_name))
            return redirect('edit_profile')
        elif 'update_email' in request.POST:
            new_email = request.POST['email']
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'Correo actualizado con éxito a {}'.format(new_email))
            return redirect('edit_profile')
        elif 'update_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Contraseña actualizada con éxito')
            else:
                messages.error(request, 'Por favor, corrija los errores en el formulario de contraseña')
            return redirect('edit_profile')
    else:
        password_form = PasswordChangeForm(request.user)

    return render(request, 'profile/edit_profile.html', {'password_form': password_form})


def log_out(request):
    logout(request)
    return redirect('index')


