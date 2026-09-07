from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Opportunity
from .forms import OpportunityForm


def opportunity_list(request):
    query = request.GET.get("q", "")

    opportunities = Opportunity.objects.all()

    if query:
        opportunities = opportunities.filter(
            Q(company__company_name__icontains=query) |
            Q(contact__first_name__icontains=query) |
            Q(contact__last_name__icontains=query) |
            Q(title__icontains=query) |
            Q(stage__icontains=query)
        )

    paginator = Paginator(opportunities, 5)
    page_number = request.GET.get("page")
    opportunities = paginator.get_page(page_number)

    return render(
        request,
        "opportunities/opportunity_list.html",
        {
            "opportunities": opportunities,
            "query": query,
        },
    )


def add_opportunity(request):
    if request.method == "POST":
        form = OpportunityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("opportunity_list")
    else:
        form = OpportunityForm()

    return render(request, "opportunities/add_opportunity.html", {"form": form})


def edit_opportunity(request, id):
    opportunity = get_object_or_404(Opportunity, id=id)

    if request.method == "POST":
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            return redirect("opportunity_list")
    else:
        form = OpportunityForm(instance=opportunity)

    return render(request, "opportunities/add_opportunity.html", {"form": form})


def delete_opportunity(request, id):
    opportunity = get_object_or_404(Opportunity, id=id)
    opportunity.delete()
    return redirect("opportunity_list")