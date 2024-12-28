from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

urlpatterns = [
    path(
        route='',
        view=include('blog.urls')
    ),
    path(
        route='pages/',
        view=include('pages.urls')
    ),
    path(
        route='admin/',
        view=admin.site.urls
    ),
    path(
        route='auth/registration/',
        view=CreateView.as_view(
            form_class=UserCreationForm,
            template_name='registration/registration_form.html',
            success_url=reverse_lazy('blog:index')
        ),
        name='registration',
    ),
    path(
        route='auth/',
        view=include('django.contrib.auth.urls')
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'pages.views.csrf_permission_denied'

handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.server_failure'
