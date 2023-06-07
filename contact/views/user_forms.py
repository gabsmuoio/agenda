from django.shortcuts import render, redirect
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.contrib import messages


def register(request):
    form_ = RegisterForm()

    # Estilos de mensagem
    # messages.info(request, 'Um texto qualquer')
    # messages.success(request, 'Um texto qualquer')
    # messages.warning(request, 'Um texto qualquer')
    # messages.error(request, 'Um texto qualquer')

    if request.method == 'POST':
        form_ = RegisterForm(request.POST)

        if form_.is_valid():
            form_.save()
            messages.success(request, 'Usuário registrado')
            return redirect('contact:login')

    return render(
        request,
        'contact/register.html',
        {
            'form': form_
        }
    )

# Decorator para só mostrar essa view quando o user estiver logado


@login_required(login_url='contact:login')
def user_update(request):
    form_ = RegisterUpdateForm(instance=request.user)

    if request.method == 'POST':
        form_ = RegisterUpdateForm(data=request.POST, instance=request.user)

        if form_.is_valid():
            form_.save()
            messages.success(request, 'Usuário alterado com sucesso!')
            print('Usuário alterado com sucesso!')
            return redirect('contact:user_update')

    return render(
        request,
        'contact/user_update.html',
        {
            'form': form_
        }
    )


def login_view(request):
    form_ = AuthenticationForm(request)

    if request.method == 'POST':
        form_ = AuthenticationForm(request, data=request.POST)

        if form_.is_valid():
            messages.success(request, 'Login efetuado com sucesso!')
            user_ = form_.get_user()
            print(user_)
            auth.login(request, user_)  # Aqui eu faço o login do usuário
            return redirect('contact:index')

        messages.error(request, 'Login inválido!')

    return render(
        request,
        'contact/login.html',
        {
            'form': form_
        }
    )

# Decorator para só mostrar essa view quando o user estiver logado


@login_required(login_url='contact:login')
def logout_view(request):
    auth.logout(request)

    return redirect('contact:login')
