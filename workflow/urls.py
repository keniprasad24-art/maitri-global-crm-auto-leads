from django.urls import path
from . import views

urlpatterns = [
    # Initial Contact URLs
    path("contacts/", views.contact_list, name="contact_list"),
    path("contacts/add/", views.add_contact, name="add_contact"),
    
    # Discovery Meeting URLs
    path("discovery/", views.discovery_list, name="discovery_list"),
    path("discovery/add/", views.add_discovery, name="add_discovery"),
    path("discovery/add/<int:lead_id>/", views.add_discovery, name="add_discovery_for_lead"),
    path("analysis/", views.analysis_list, name="analysis_list"), 
    path("analysis/add/", views.add_analysis, name="add_analysis"),
    path("contact/<int:pk>/", views.contact_detail, name="contact_detail"),
    path("discovery/<int:pk>/", views.discovery_detail, name="discovery_detail"),
    path("analysis/<int:pk>/", views.analysis_detail, name="analysis_detail"),
]
