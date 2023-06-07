from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse  # Para conseguir passar urls para dentro
from django.contrib.auth.decorators import login_required

from contact.forms import ContactForm
from contact.models import Contact


# Create your views here.

# Decorator para só mostrar essa view quando o user estiver logado


@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')

    # Esse 'first_name' é o nome que eu dei para o input lá no create.html
    if request.method == 'POST':
        fn = request.POST.get('first_name')
        print(f'Primeiro nome enviado: {fn}')

        form = ContactForm(data=request.POST, files=request.FILES)

        context = {
            'form': form,
            'form_action': form_action,
        }

        # Só retorna True se o form não tiver nenhum erro
        if form.is_valid():
            print('Formulário válido')
            # Salvando na base de dados

            # Aqui primeiro eu salvo na memória, mas ainda não dou o commit \
            # para subir para o BD
            # Se eu não quiser mudar nada, dou o .save() direto
            form_edit = form.save(commit=False)
            # Incluindo o owner como o usuário logado
            form_edit.owner = request.user
            form_edit.save()

            # O redirect é para limpar os dados da página após enviar os dados
            # ou como neste caso, para enviar para outra página
            return redirect('contact:update', contact_id=form_edit.pk)

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )

# Decorator para só mostrar essa view quando o user estiver logado


@login_required(login_url='contact:login')
def update(request, contact_id):
    # Pegando um contato para atualizar
    contact_upd = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user
    )
    form_action = reverse('contact:update', args=(contact_id,))

    # Esse 'first_name' é o nome que eu dei para o input lá no create.html
    if request.method == 'POST':
        print(f'Registro atualizado {contact_id}')

        form = ContactForm(data=request.POST,
                           files=request.FILES, instance=contact_upd)

        context = {
            'form': form,
            'form_action': form_action,
        }

        # Só retorna True se o form não tiver nenhum erro
        if form.is_valid():
            form_edit = form.save()
            # O redirect é para limpar os dados da página após enviar os dados
            # ou como neste caso, para enviar para outra página
            return redirect('contact:update', contact_id=form_edit.pk)

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(instance=contact_upd),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )

# Decorator para só mostrar essa view quando o user estiver logado


@login_required(login_url='contact:login')
def delete(request, contact_id):
    contact_del = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user
    )
    confirmation_ = request.POST.get('confirmation', 'no')

    if confirmation_ == 'yes':
        contact_del.delete()
        return redirect('contact:index')

    return render(
        request,
        'contact/contact.html',
        {
            'contatos_': contact_del,
            'confirmation': confirmation_,
        }
    )
