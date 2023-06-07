from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [

    path('search/', views.search, name='search'),  # type: ignore
    path('', views.index, name='index'),  # type: ignore

    # contact (CRUD)
    path('contact/<int:contact_id>/detail/',
         views.contact, name='contact'),  # type: ignore
    path('contact/create/', views.create, name='create'),  # type: ignore
    path('contact/<int:contact_id>/update/',
         views.update, name='update'),  # type: ignore
    path('contact/<int:contact_id>/delete/',
         views.delete, name='delete'),  # type: ignore

    # users (CRUD)
    path('user/create/', views.register, name='register'),  # type: ignore
    path('user/login/', views.login_view, name='login'),  # type: ignore
    path('user/logout', views.logout_view, name='logout'),  # type: ignore
    path('user/update', views.user_update, name='user_update'),  # type: ignore

]
