from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('add/', views.add_lead, name='add_lead'),
    path('edit/<int:id>/', views.edit_lead, name='edit_lead'),
    path('delete/<int:id>/', views.delete_lead, name='delete_lead'),
    path("api/capture/", views.api_capture_lead, name="api_capture_lead"),
    path("upload-excel/", views.upload_leads_excel, name="upload_leads_excel"),
]