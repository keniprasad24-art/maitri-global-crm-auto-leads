from django.urls import path
from . import views

urlpatterns = [
    path("", views.opportunity_list, name="opportunity_list"),
    path("add/", views.add_opportunity, name="add_opportunity"),
    path("edit/<int:id>/", views.edit_opportunity, name="edit_opportunity"),
    path("delete/<int:id>/", views.delete_opportunity, name="delete_opportunity"),
]