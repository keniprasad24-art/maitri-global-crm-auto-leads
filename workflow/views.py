from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import InitialContact, DiscoveryMeeting, RequirementAnalysis
from .forms import InitialContactForm, DiscoveryMeetingForm, RequirementAnalysisForm
from leads.models import Lead
from django.db.models import Q

def contact_list(request):
    query = request.GET.get("q", "")
    contacts = InitialContact.objects.all().order_by("-id")
    if query:
        contacts = contacts.filter(Q(lead_nameicontains=query) | Q(contact_person_icontains=query))
    return render(request, "workflow/contact_list.html", {"contacts": contacts, "query": query})

def add_contact(request):
    if request.method == "POST":
        form = InitialContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact saved!")
            return redirect("contact_list")
    else:
        form = InitialContactForm()
    return render(request, "workflow/workflow_form.html", {"form": form, "title": "Add Initial Contact"})

def discovery_list(request):
    query = request.GET.get("q", "")
    meetings = DiscoveryMeeting.objects.all().order_by("-id")
    if query:
        meetings = meetings.filter(lead_name_icontains=query)
    return render(request, "workflow/discovery_list.html", {"meetings": meetings, "query": query})

def add_discovery(request, lead_id=None):
    lead = get_object_or_404(Lead, id=lead_id) if lead_id else None
    if request.method == "POST":
        form = DiscoveryMeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("discovery_list")
    else:
        form = DiscoveryMeetingForm(initial={'lead': lead} if lead else {})
    return render(request, "workflow/workflow_form.html", {"form": form, "title": "Add Discovery Meeting"})

def analysis_list(request):
    query = request.GET.get("q", "")
    analyses = RequirementAnalysis.objects.all().order_by("-id")
    if query:
        analyses = analyses.filter(lead_name_icontains=query)
    return render(request, "workflow/analysis_list.html", {"analyses": analyses, "query": query})

def add_analysis(request):
    if request.method == "POST":
        form = RequirementAnalysisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("analysis_list")
    else:
        form = RequirementAnalysisForm()
    return render(request, "workflow/workflow_form.html", {"form": form, "title": "Add Requirement Analysis"})

def contact_detail(request, pk):
    contact = get_object_or_404(InitialContact, pk=pk)
    return render(request, "workflow/contact_detail.html", {"contact": contact})

def discovery_detail(request, pk):
    meeting = get_object_or_404(DiscoveryMeeting, pk=pk)
    return render(request, "workflow/discovery_detail.html", {"meeting": meeting})

def analysis_detail(request, pk):
    analysis = get_object_or_404(RequirementAnalysis, pk=pk)
    return render(request, "workflow/analysis_detail.html", {"analysis": analysis})