from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from diplom import settings
from webapp.views import index, about, contact, services, account, register, logout_view, panel_admin, add_order, \
    get_models, add_reviews, download_order, waiting, agreement, at_work, ready, given, cancel, change_order, \
    get_models_add_auto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('services/', services, name='services'),
    path('account/', account, name='account'),
    path('panel_admin/', panel_admin, name='panel_admin'),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('add_order/', add_order, name='add_order'),
    path('get_models/', get_models),
    path('get_models_add_auto/', get_models_add_auto),
    path('add_reviews/', add_reviews, name='add_reviews'),
    path('order/<int:order_id>/download/', download_order, name='download_order'),
    path('waiting/<int:order_id>/', waiting, name='waiting'),
    path('agreement/<int:order_id>/', agreement, name='agreement'),
    path('at_work/<int:order_id>/', at_work, name='at_work'),
    path('ready/<int:order_id>/', ready, name='ready'),
    path('given/<int:order_id>/', given, name='given'),
    path('cancel/<int:order_id>/', cancel, name='cancel'),
    path('change_order/<int:order_id>/', change_order, name='change_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
