from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from django.contrib import admin

api_name = 'api'
urlpatterns = [
    path('admin/', admin.site.urls),

    path(f'{api_name}/accounts/', include('accounts.urls')),
    path(f'{api_name}/exam/', include('exam.urls')),
    path(f'{api_name}/quiz/', include('quiz.urls')),

    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]