from django.shortcuts import render, redirect
from .models import Invoice
from .forms import InvoiceForm

def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, "invoice_list.html", {"invoices": invoices})

def add_invoice(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("invoice_list")
    else:
        form = InvoiceForm()

    return render(request, "add_invoice.html", {"form": form})

def edit_invoice(request, id):
    invoice = Invoice.objects.get(id=id)

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect("invoice_list")
    else:
        form = InvoiceForm(instance=invoice)

    return render(request, "add_invoice.html", {"form": form})

def delete_invoice(request, id):
    invoice = Invoice.objects.get(id=id)
    invoice.delete()
    return redirect("invoice_list")