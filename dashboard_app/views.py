from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

from leads.models import Lead
from companies.models import Company
from opportunities.models import Opportunity
from quotations.models import Quotation
from invoices.models import Invoice
from qualified.models import Qualified
from subscription.models import Subscription


@login_required
def dashboard(request):
    recent_leads = Lead.objects.order_by('-id')[:5]

    lead_chart_labels = ["New", "Qualified", "Lost"]
    lead_chart_data = [
        Lead.objects.filter(status="New").count(),
        Lead.objects.filter(status="Qualified").count(),
        Lead.objects.filter(status="Lost").count(),
    ]

    opp_chart_labels = ["Open", "Won", "Lost"]
    opp_chart_data = [
        Opportunity.objects.filter(status="Open").count(),
        Opportunity.objects.filter(status="Won").count(),
        Opportunity.objects.filter(status="Lost").count(),
    ]

    context = {
        "lead_count": Lead.objects.count(),
        "company_count": Company.objects.count(),
        "opportunity_count": Opportunity.objects.count(),
        "quotation_count": Quotation.objects.count(),
        "invoice_count": Invoice.objects.count(),
        "qualified_count": Qualified.objects.count(),

        "won_count": Opportunity.objects.filter(status="Won").count(),
        "lost_count": Opportunity.objects.filter(status="Lost").count(),

        "total_subscriptions": Subscription.objects.count(),
        "active_subscriptions": Subscription.objects.filter(status="Active").count(),
        "expired_subscriptions": Subscription.objects.filter(status="Expired").count(),

        "lead_chart_labels": lead_chart_labels,
        "lead_chart_data": lead_chart_data,
        "opp_chart_labels": opp_chart_labels,
        "opp_chart_data": opp_chart_data,

        "recent_leads": recent_leads,
    }

    return render(request, "dashboard_app/dashboard.html", context)


@login_required
def profile_settings(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        current_password = request.POST.get("current_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username:
            messages.error(request, "Username cannot be empty.")
            return render(request, "dashboard_app/profile.html")

        if username != user.username:
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, "This username is already taken.")
                return render(request, "dashboard_app/profile.html")

        if new_password or confirm_password or current_password:
            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
                return render(request, "dashboard_app/profile.html")

            if new_password != confirm_password:
                messages.error(request, "New password and confirm password do not match.")
                return render(request, "dashboard_app/profile.html")

            if len(new_password) < 6:
                messages.error(request, "Password must be at least 6 characters.")
                return render(request, "dashboard_app/profile.html")

            user.set_password(new_password)

        user.username = username
        user.save()

        if new_password:
            update_session_auth_hash(request, user)

        messages.success(request, "Profile updated successfully.")
        return render(request, "dashboard_app/profile.html")

    return render(request, "dashboard_app/profile.html")
