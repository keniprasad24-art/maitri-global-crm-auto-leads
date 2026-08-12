from django.shortcuts import render, redirect, get_object_or_404
from .models import Quotation
from .forms import QuotationForm


def quotation_list(request):
    quotations = Quotation.objects.all()
    return render(request, "quotation_list.html", {"quotations": quotations})


def add_quotation(request):
    if request.method == "POST":
        form = QuotationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quotation_list")
    else:
        form = QuotationForm()

    return render(request, "add_quotation.html", {"form": form})


def edit_quotation(request, id):
    quotation = get_object_or_404(Quotation, id=id)

    if request.method == "POST":
        form = QuotationForm(request.POST, instance=quotation)
        if form.is_valid():
            form.save()
            return redirect("quotation_list")
    else:
        form = QuotationForm(instance=quotation)

    return render(request, "add_quotation.html", {"form": form})


def delete_quotation(request, id):
    quotation = get_object_or_404(Quotation, id=id)
    quotation.delete()
    return redirect("quotation_list")