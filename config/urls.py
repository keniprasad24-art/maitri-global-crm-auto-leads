"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
   path(
    "",
    auth_views.LoginView.as_view(
        template_name="dashboard_app/login.html"
    ),
    name="home",
),

path("dashboard/", include("dashboard_app.urls")),
    path("admin/", admin.site.urls),
    path(
    "login/",
    auth_views.LoginView.as_view(
       template_name="dashboard_app/login.html"
    ),
    name="login",
),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Companies
    path("companies/", include("companies.urls")),

    # Leads
    path("leads/", include("leads.urls")),

    # Opportunities
    path("opportunities/", include("opportunities.urls")),

    # Quotations
    path("quotations/", include("quotations.urls")),
    path("invoices/", include("invoices.urls")),
    path("reports/", include("reports.urls")),
    path("qualified/", include("qualified.urls")),
    path('workflow/', include('workflow.urls')),
    path("subscription/", include("subscription.urls")),
]