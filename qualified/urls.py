from django.urls import path
from . import views

urlpatterns = [
    path("", views.qualified_list, name="qualified_list"),
    path("add/", views.add_qualified, name="add_qualified"),
    path("edit/<int:id>/", views.edit_qualified, name="edit_qualified"),
    path("delete/<int:id>/", views.delete_qualified, name="delete_qualified"),
]