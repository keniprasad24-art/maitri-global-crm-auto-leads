from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Contact
from companies.models import Company


def contact_list(request):
    query = request.GET.get("q", "")

    contacts = Contact.objects.all()

    if query:
        contacts = contacts.filter(
            Q(company__company_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    paginator = Paginator(contacts, 5)
    page_number = request.GET.get("page")
    contacts = paginator.get_page(page_number)

    return render(
        request,
        "contacts/contact_list.html",
        {
            "contacts": contacts,
            "query": query,
        },
    )


def add_contact(request):
    companies = Company.objects.all()

    if request.method == "POST":
        Contact.objects.create(
            company=Company.objects.get(id=request.POST["company"]),
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
        )
        return redirect("contact_list")

    return render(
        request,
        "contacts/add_contact.html",
        {"companies": companies},
    )


def edit_contact(request, id):
    contact = get_object_or_404(Contact, id=id)

    if request.method == "POST":
        contact.company = Company.objects.get(id=request.POST["company"])
        contact.first_name = request.POST["first_name"]
        contact.last_name = request.POST["last_name"]
        contact.email = request.POST["email"]
        contact.phone = request.POST["phone"]
        contact.save()

        return redirect("contact_list")

    return render(
        request,
        "contacts/add_contact.html",
        {
            "contact": contact,
            "companies": Company.objects.all(),
        },
    )


def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    return redirect("contact_list")