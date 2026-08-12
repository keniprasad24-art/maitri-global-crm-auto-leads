from django.urls import path
from . import views

urlpatterns = [
    path("", views.subscription_list, name="subscription_list"),
    path("add/", views.add_subscription, name="add_subscription"),
    path("edit/<int:pk>/", views.edit_subscription, name="edit_subscription"),
    path("delete/<int:pk>/", views.delete_subscription, name="delete_subscription"),

     # Razorpay Payment
    path("payment/<int:pk>/", views.payment, name="subscription_payment"),
]