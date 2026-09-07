from django.urls import path
from . import views

urlpatterns = [
    path("", views.quotation_list, name="quotation_list"),
    path("add/", views.add_quotation, name="add_quotation"),
    path("edit/<int:id>/", views.edit_quotation, name="edit_quotation"),
    path("delete/<int:id>/", views.delete_quotation, name="delete_quotation"),
]