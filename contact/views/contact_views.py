from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.


def index(request):
    # Pegando todos os contatos da classe Contact
    contacts = Contact.objects.filter(show=True).order_by('id')

    paginacao = Paginator(contacts, 10)
    pag_number = request.GET.get("page")
    pag_obj = paginacao.get_page(pag_number)

    context = {
        'pag_obj_': pag_obj,
        'site_title': 'Contatos - '
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def search(request):
    search_value = request.GET.get('q', '').strip()
    print(f'Valor buscado: {search_value}')

    # Se o cara não digitar nada, eu volto para a tela que eu quiser
    if search_value == '':
        return redirect('contact:index')

    # Pegando todos os contatos da classe Contact
    contacts = Contact.objects\
        .filter(show=True)\
        .filter(
            # Usando a função Q, eu consigo filtrar o valor esperado em 2 campos diferentes (ou mais)
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(email__icontains=search_value)
        )\
        .order_by('id')

    print(f'Query usada: \n {contacts.query}')
    print(f'\nLista de contatos encontradas: {contacts.get}')

    paginacao = Paginator(contacts, 10)
    pag_number = request.GET.get("page")
    pag_obj = paginacao.get_page(pag_number)

    context = {
        'pag_obj_': pag_obj,
        'site_title': 'Procurar - '
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def contact(request, contact_id):
    # Pegando todos os contatos (e campos) da classe Contact
    # single_contact = Contact.objects.get(pk=contact_id)
    single_contact = get_object_or_404(
        Contact.objects, pk=contact_id, show=True)

    site_title = f'{single_contact.first_name} {single_contact.last_name} -'

    context = {
        'contatos_': single_contact,
        'site_title': site_title
    }

    return render(
        request,
        'contact/contact.html',
        context
    )
