# health_data_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health_data/', include('health_data_app.urls')),
    path('', lambda request: HttpResponseRedirect('health_data/save/')),  # Перенаправление на страницу сохранения данных
]
