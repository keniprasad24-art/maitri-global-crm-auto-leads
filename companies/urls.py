from django.urls import path
from . import views

urlpatterns = [
    path("", views.company_list, name="company_list"),
     path("add/", views.add_company, name="add_company"),
     path("edit/<int:id>/", views.edit_company, name="edit_company"),
      path("delete/<int:id>/", views.delete_company, name="delete_company"),
]