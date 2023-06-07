from django.contrib import admin
from contact import models

# Register your models here.


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    # Configurando o display que vai aparecer lá no admin
    list_display = 'id', 'first_name', 'last_name', 'phone', 'email', 'show'
    ordering = 'id',
    # list_filter = 'city'
    search_fields = 'first_name', 'last_name',
    list_per_page = 25
    list_max_show_all = 100
    # Editar campos na própria tela de display
    list_editable = 'phone', 'show'
    list_display_links = 'first_name', 'last_name',


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    # Configurando o display que vai aparecer lá no admin
    list_display = 'name',
    ordering = 'id',
