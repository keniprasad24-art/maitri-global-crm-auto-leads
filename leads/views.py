from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import json
import os
import re

import openpyxl
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import Lead


SOURCE_ALIASES = {
    "facebook": "facebook",
    "facebook ads": "facebook",
    "instagram": "instagram",
    "instagram ads": "instagram",
    "99acres": "99acres",
    "magicbricks": "magicbricks",
    "magic bricks": "magicbricks",
    "housing": "housing",
    "housing.com": "housing",
    "nobroker": "nobroker",
    "no broker": "nobroker",
    "phone": "phone",
    "call": "phone",
    "phone call": "phone",
    "whatsapp": "whatsapp",
    "website": "website",
    "manual": "manual",
    "import": "import",
}


def normalize_source(value):
    raw = str(value or "manual").strip()
    return SOURCE_ALIASES.get(raw.lower(), raw[:50] or "manual")


def clean_text(value):
    return "" if value is None else str(value).strip()


def clean_phone(value):
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return clean_text(value)


def clean_email(value):
    value = clean_text(value)
    match = re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", value)
    return match.group(0) if match else ""


def parse_date(value):
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    value = clean_text(value)
    for fmt in (
        "%d-%b-%Y", "%d-%B-%Y", "%d/%m/%Y", "%d-%m-%Y",
        "%Y-%m-%d", "%d.%m.%Y", "%d-%b-%y", "%d-%B-%y",
    ):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    return None


def parse_money(value):
    if value in (None, ""):
        return None
    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value))
    text = clean_text(value).replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None
    number = Decimal(match.group(0))
    if "LPM" in text.upper() or "LPA" in text.upper():
        number *= Decimal("100000")
    elif "K" in text.upper():
        number *= Decimal("1000")
    return number


def lead_exists(phone="", email=""):
    q = Q()
    found = False
    if phone:
        q |= Q(phone=phone) | Q(mobile_no=phone)
        found = True
    if email:
        q |= Q(email__iexact=email) | Q(email_id__iexact=email)
        found = True
    return Lead.objects.filter(q).exists() if found else False


def lead_list(request):
    query = request.GET.get("q", "")
    leads = Lead.objects.all().order_by("-id")
    if query:
        leads = leads.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
            | Q(phone__icontains=query) | Q(client_name__icontains=query)
            | Q(email_id__icontains=query) | Q(mobile_no__icontains=query)
        )
    paginator = Paginator(leads, 10)
    leads = paginator.get_page(request.GET.get("page"))
    return render(request, "leads/lead_list.html", {"leads": leads, "query": query})


def add_lead(request):
    if request.method == "POST":
        Lead.objects.create(
            name=request.POST.get("name", ""), email=request.POST.get("email", ""),
            phone=request.POST.get("phone", ""), company=request.POST.get("company", ""),
            source=normalize_source(request.POST.get("source", "manual")),
            status=request.POST.get("status", "New"), lead_pdf=request.FILES.get("lead_pdf"),
        )
        return redirect("lead_list")
    return render(request, "leads/add_lead.html")


def edit_lead(request, id):
    lead = get_object_or_404(Lead, id=id)
    if request.method == "POST":
        lead.name = request.POST.get("name", "")
        lead.email = request.POST.get("email", "")
        lead.phone = request.POST.get("phone", "")
        lead.company = request.POST.get("company", "")
        lead.source = normalize_source(request.POST.get("source", "manual"))
        lead.status = request.POST.get("status", "New")
        lead.save()
        return redirect("lead_list")
    return render(request, "leads/edit_lead.html", {"lead": lead})


def delete_lead(request, id):
    get_object_or_404(Lead, id=id).delete()
    return redirect("lead_list")


def upload_leads_excel(request):
    if request.method != "POST":
        return render(request, "leads/upload_excel.html")
    excel_file = request.FILES.get("excel_file")
    if not excel_file:
        messages.error(request, "Please select an Excel file.")
        return redirect("lead_list")

    try:
        wb = openpyxl.load_workbook(excel_file, data_only=True, read_only=True)
        sheet = wb.active
        rows_to_create = []
        skipped = 0
        duplicate = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row or all(v in (None, "") for v in row):
                continue
            values = list(row) + [None] * max(0, 21 - len(row))
            sr_no, current_requirements, received, lead_source, reference_name = values[:5]
            client_name, end_client, location, contact_person, designation = values[5:10]
            mobile_no, email_id, recurring, duration, consultant_name = values[10:15]
            consultant_cost, maitri_margin, lead_stage, followup, vendor, status = values[15:21]

            name = clean_text(client_name)
            phone = clean_phone(mobile_no)
            email = clean_email(email_id)
            company = clean_text(end_client or client_name or "Not Provided")
            if not name and not email and not phone:
                skipped += 1
                continue
            if lead_exists(phone, email):
                duplicate += 1
                continue

            rows_to_create.append(Lead(
                sr_no=int(sr_no) if isinstance(sr_no, (int, float)) and float(sr_no).is_integer() else 0,
                current_requirements=clean_text(current_requirements),
                lead_received_date=parse_date(received),
                lead_source=clean_text(lead_source),
                reference_name=clean_text(reference_name), client_name=name,
                end_client=clean_text(end_client), location=clean_text(location),
                contact_person=clean_text(contact_person), designation=clean_text(designation),
                mobile_no=phone, email_id=email, one_time_recurring=clean_text(recurring),
                project_duration=clean_text(duration), consultant_name=clean_text(consultant_name),
                consultant_cost=parse_money(consultant_cost), maitri_margin=parse_money(maitri_margin),
                lead_stage=clean_text(lead_stage), next_follow_up_date=parse_date(followup),
                vendor_working_on=clean_text(vendor), status=clean_text(status) or "New",
                name=name, email=email, phone=phone, company=company, source="import",
            ))

        with transaction.atomic():
            Lead.objects.bulk_create(rows_to_create, batch_size=500)
        messages.success(request, f"{len(rows_to_create)} leads imported successfully. {duplicate} duplicates skipped, {skipped} empty rows skipped.")
    except Exception as exc:
        messages.error(request, f"Excel upload failed: {exc}")
    return redirect("lead_list")


@csrf_exempt
def api_capture_lead(request):
    """Generic webhook endpoint for authorised lead sources/telephony providers.
    POST JSON: name, phone, email, company, source, requirement, external_id.
    Configure LEAD_CAPTURE_TOKEN in environment and send X-Lead-Token.
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

    expected = os.environ.get("LEAD_CAPTURE_TOKEN", "")
    supplied = request.headers.get("X-Lead-Token", "")
    if expected and supplied != expected:
        return JsonResponse({"status": "error", "message": "Invalid token"}, status=403)

    try:
        if request.content_type and "application/json" in request.content_type:
            data = json.loads(request.body or "{}")
        else:
            data = request.POST.dict()
        name = clean_text(data.get("name") or data.get("full_name"))
        phone = clean_phone(data.get("phone") or data.get("mobile") or data.get("mobile_no"))
        email = clean_email(data.get("email") or data.get("email_id"))
        if not name and not phone and not email:
            return JsonResponse({"status": "error", "message": "name, phone or email is required"}, status=400)
        if lead_exists(phone, email):
            return JsonResponse({"status": "duplicate", "message": "Lead already exists"}, status=200)

        lead = Lead.objects.create(
            name=name, client_name=name, phone=phone, mobile_no=phone,
            email=email, email_id=email,
            company=clean_text(data.get("company") or "Online Inquiry") or "Online Inquiry",
            end_client=clean_text(data.get("company")),
            current_requirements=clean_text(data.get("requirement") or data.get("message") or data.get("current_requirement")),
            lead_source=clean_text(data.get("source") or "online"),
            source=normalize_source(data.get("source") or "website"),
            status="New",
        )
        return JsonResponse({"status": "success", "lead_id": lead.id, "source": lead.source}, status=201)
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({"status": "error", "message": "Invalid request data"}, status=400)
    except Exception as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)
