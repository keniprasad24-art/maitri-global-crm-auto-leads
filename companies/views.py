from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Company


def company_list(request):
    query = request.GET.get("q", "")

    companies = Company.objects.all()

    if query:
        companies = companies.filter(
            Q(company_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(country__icontains=query)
        )

    paginator = Paginator(companies, 5)
    page_number = request.GET.get("page")
    companies = paginator.get_page(page_number)

    return render(
        request,
        "companies/company_list.html",
        {
            "companies": companies,
            "query": query,
        },
    )


def add_company(request):
    if request.method == "POST":
        Company.objects.create(
            company_name=request.POST["company_name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            website=request.POST["website"],
            address=request.POST["address"],
            city=request.POST["city"],
            state=request.POST["state"],
            country=request.POST["country"],
        )
        return redirect("company_list")

    return render(request, "companies/add_company.html")


def edit_company(request, id):
    company = get_object_or_404(Company, id=id)

    if request.method == "POST":
        company.company_name = request.POST["company_name"]
        company.email = request.POST["email"]
        company.phone = request.POST["phone"]
        company.website = request.POST["website"]
        company.address = request.POST["address"]
        company.city = request.POST["city"]
        company.state = request.POST["state"]
        company.country = request.POST["country"]
        company.save()
        return redirect("company_list")

    return render(request, "companies/add_company.html", {"company": company})


def delete_company(request, id):
    company = get_object_or_404(Company, id=id)
    company.delete()
    return redirect("company_list")