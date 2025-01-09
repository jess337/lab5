from django.urls import path
from . import views

urlpatterns = [
    path('save/', views.save_data, name='save_data'),
    path('load/', views.load_data, name='load_data'),
    path('list/', views.list_data, name='list_data'),
    path('edit/<str:patient_id>/', views.edit_data, name='edit_data'),
    path('delete/<str:patient_id>/', views.delete_data, name='delete_data'),
]
