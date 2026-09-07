from django.urls import path
from . import views

urlpatterns = [
    path("", views.invoice_list, name="invoice_list"),
    path("add/", views.add_invoice, name="add_invoice"),
    path("edit/<int:id>/", views.edit_invoice, name="edit_invoice"),
    path("delete/<int:id>/", views.delete_invoice, name="delete_invoice"),
]