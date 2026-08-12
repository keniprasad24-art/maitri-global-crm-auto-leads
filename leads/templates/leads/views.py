from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import json
import openpyxl
import re

from datetime import datetime, date
from decimal import Decimal, InvalidOperation

from .models import Lead


def lead_list(request):
    query = request.GET.get("q", "")
    leads = Lead.objects.all().order_by("-id")

    if query:
        leads = leads.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
            | Q(client_name__icontains=query)
            | Q(email_id__icontains=query)
            | Q(mobile_no__icontains=query)
        )

    paginator = Paginator(leads, 10)
    page_number = request.GET.get("page")
    leads = paginator.get_page(page_number)

    return render(request, "leads/lead_list.html", {"leads": leads, "query": query})


def add_lead(request):
    if request.method == "POST":
        Lead.objects.create(
            name=request.POST.get("name", ""),
            email=request.POST.get("email", ""),
            phone=request.POST.get("phone", ""),
            company=request.POST.get("company", ""),
            source=request.POST.get("source", "manual"),
            status=request.POST.get("status", "New"),
            lead_pdf=request.FILES.get("lead_pdf"),
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
        lead.source = request.POST.get("source", "manual")
        lead.status = request.POST.get("status", "New")
        lead.save()
        return redirect("lead_list")

    return render(request, "leads/edit_lead.html", {"lead": lead})


def delete_lead(request, id):
    lead = get_object_or_404(Lead, id=id)
    lead.delete()
    return redirect("lead_list")


def upload_leads_excel(request):
    if request.method != "POST":
        return render(request, "leads/upload_excel.html")

    excel_file = request.FILES.get("excel_file")

    if not excel_file:
        messages.error(request, "Please select an Excel file.")
        return render(request, "leads/upload_excel.html")

    try:
        workbook = openpyxl.load_workbook(excel_file, data_only=True)
        sheet = workbook.active

        imported_count = 0
        skipped_count = 0
        errors = []

        def text(value):
            return "" if value is None else str(value).strip()

        def email(value):
            value = text(value)
            match = re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", value)
            return match.group(0) if match else ""

        def phone(value):
            if value is None:
                return ""
            if isinstance(value, float) and value.is_integer():
                return str(int(value))
            return text(value)

        def parse_date(value):
            if value in (None, ""):
                return None
            if isinstance(value, datetime):
                return value.date()
            if isinstance(value, date):
                return value

            value = text(value)
            for fmt in (
                "%d-%b-%Y", "%d-%B-%Y", "%d/%m/%Y",
                "%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y",
                "%d-%b-%y", "%d-%B-%y",
            ):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    pass
            return None

        def parse_decimal(value):
            if value in (None, ""):
                return None
            if isinstance(value, (int, float, Decimal)):
                return Decimal(str(value))

            value = text(value).replace("₹", "").replace(",", "")
            value = re.sub(r"\bLPM\b", "", value, flags=re.IGNORECASE)
            value = re.sub(r"[^0-9.\-]", "", value)

            if not value or value in (".", "-"):
                return None

            try:
                return Decimal(value)
            except (InvalidOperation, ValueError):
                return None

        valid_statuses = {"New", "Contacted", "Qualified", "Lost"}

        for row_number, row in enumerate(
            sheet.iter_rows(min_row=2, values_only=True), start=2
        ):
            if not row or all(value in (None, "") for value in row):
                continue

            try:
                values = list(row) + [None] * max(0, 21 - len(row))

                sr_no = values[0]
                current_requirements = values[1]
                lead_received_date = values[2]
                lead_source = values[3]
                reference_name = values[4]
                client_name = values[5]
                end_client = values[6]
                location = values[7]
                contact_person = values[8]
                designation = values[9]
                mobile_no = values[10]
                email_id = values[11]
                one_time_recurring = values[12]
                project_duration = values[13]
                consultant_name = values[14]
                consultant_cost = values[15]
                maitri_margin = values[16]
                lead_stage = values[17]
                next_follow_up_date = values[18]
                vendor_working_on = values[19]
                excel_status = values[20]

                name_value = text(client_name)
                email_value = email(email_id)
                phone_value = phone(mobile_no)
                company_value = text(end_client or client_name or "Not Provided")

                if not name_value and not email_value and not phone_value:
                    skipped_count += 1
                    continue

                try:
                    sr_value = int(float(sr_no)) if sr_no not in (None, "") else 0
                except (ValueError, TypeError):
                    sr_value = 0

                status_value = text(excel_status)
                if status_value not in valid_statuses:
                    status_value = "New"

                Lead.objects.create(
                    sr_no=sr_value,
                    current_requirements=text(current_requirements),
                    lead_received_date=parse_date(lead_received_date),
                    lead_source=text(lead_source),
                    reference_name=text(reference_name),
                    client_name=name_value,
                    end_client=text(end_client),
                    location=text(location),
                    contact_person=text(contact_person),
                    designation=text(designation),
                    mobile_no=phone_value,
                    email_id=email_value,
                    one_time_recurring=text(one_time_recurring),
                    project_duration=text(project_duration),
                    consultant_name=text(consultant_name),
                    consultant_cost=parse_decimal(consultant_cost),
                    maitri_margin=parse_decimal(maitri_margin),
                    lead_stage=text(lead_stage),
                    next_follow_up_date=parse_date(next_follow_up_date),
                    vendor_working_on=text(vendor_working_on),
                    status=status_value,
                    name=name_value,
                    email=email_value,
                    phone=phone_value,
                    company=company_value,
                    source="import",
                )

                imported_count += 1

            except Exception as row_error:
                skipped_count += 1
                errors.append(
                    f"Row {row_number}: {type(row_error).__name__}: {row_error}"
                )

        if imported_count:
            messages.success(
                request,
                f"{imported_count} leads uploaded and saved successfully.",
            )

        if skipped_count:
            messages.warning(request, f"{skipped_count} rows were skipped.")

        if errors:
            messages.error(
                request,
                "First import errors: " + " | ".join(errors[:3]),
            )

        return render(
            request,
            "leads/upload_excel.html",
            {
                "imported_count": imported_count,
                "skipped_count": skipped_count,
                "errors": errors[:10],
                "upload_complete": True,
            },
        )

    except Exception as exc:
        messages.error(
            request,
            f"Excel upload failed: {type(exc).__name__}: {exc}",
        )
        return render(
            request,
            "leads/upload_excel.html",
            {
                "upload_complete": True,
                "errors": [f"{type(exc).__name__}: {exc}"],
            },
        )


@csrf_exempt
def api_capture_lead(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            Lead.objects.create(
                name=data.get("name", ""),
                email=data.get("email", ""),
                phone=data.get("phone", ""),
                company=data.get("company", "Online Inquiry"),
                source=data.get("source", "website"),
                status="New",
            )
            return JsonResponse({"status": "success"}, status=201)
        except Exception:
            return JsonResponse({"status": "error"}, status=400)

    return JsonResponse(
        {"status": "error", "message": "Only POST allowed"},
        status=405,
    )


def lead_simulator(request):
    return render(request, "leads/lead_simulator.html")