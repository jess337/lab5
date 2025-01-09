from django.contrib import admin
# Импорт модели MyModel из текущего каталога (".")
from .models import MedicalData
# Регистрация модели MyModel для административного сайта
admin.site.register(MedicalData)
# Register your models here.
