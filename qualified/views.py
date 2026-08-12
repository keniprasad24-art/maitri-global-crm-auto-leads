from django.shortcuts import render, redirect, get_object_or_404
from .models import Qualified
from .forms import QualifiedForm
from django.db.models import Q

def qualified_list(request):
    query = request.GET.get("q", "")
    qualifieds = Qualified.objects.all().order_by("-id")
    
    if query:
        qualifieds = qualifieds.filter(
            Q(company__icontains=query) | Q(contact__person__icontains=query) | Q(requirement__icontains=query)
        )
    return render(request, "qualified/qualified_list.html", {"qualifieds": qualifieds, "query": query})

def add_qualified(request):
    if request.method == "POST":
        form = QualifiedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("qualified_list")
    else:
        form = QualifiedForm()
    return render(request, "qualified/qualified_form.html", {"form": form})

def edit_qualified(request, id):
    item = get_object_or_404(Qualified, id=id)
    if request.method == "POST":
        form = QualifiedForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("qualified_list")
    else:
        form = QualifiedForm(instance=item)
    return render(request, "qualified/qualified_form.html", {"form": form, "edit": True})

def delete_qualified(request, id):
    item = get_object_or_404(Qualified, id=id)
    item.delete()
    return redirect("qualified_list")