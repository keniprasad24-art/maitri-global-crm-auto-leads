from django.shortcuts import render
from django.db.models import Count
from leads.models import Lead
from companies.models import Company
from contacts.models import Contact
from opportunities.models import Opportunity
from quotations.models import Quotation
from invoices.models import Invoice


def report_dashboard(request):

    context = {
        # Dashboard Counts
        "lead_count": Lead.objects.count(),
        "company_count": Company.objects.count(),
        "contact_count": Contact.objects.count(),
        "opportunity_count": Opportunity.objects.count(),
        "quotation_count": Quotation.objects.count(),
        "invoice_count": Invoice.objects.count(),

        # Recent Records
        "recent_leads": Lead.objects.order_by("-id")[:5],
        "recent_companies": Company.objects.order_by("-id")[:5],
        "recent_contacts": Contact.objects.order_by("-id")[:5],
        "recent_opportunities": Opportunity.objects.order_by("-id")[:5],
        "recent_quotations": Quotation.objects.order_by("-id")[:5],
        "recent_invoices": Invoice.objects.order_by("-id")[:5],
    }

    return render(request, "reports/report_dashboard.html", context)