from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Subscription
from .forms import SubscriptionForm
import razorpay
from django.conf import settings

def subscription_list(request):
    query = request.GET.get("q")

    subscriptions = Subscription.objects.all()
    total = Subscription.objects.count()
    active = Subscription.objects.filter(status="Active").count()
    expired = Subscription.objects.filter(status="Expired").count()

    if query:
        subscriptions = subscriptions.filter(customer_name__icontains=query)

    paginator = Paginator(subscriptions, 10)
    page_number = request.GET.get("page")
    subscriptions = paginator.get_page(page_number)

    return render(request, "subscription/subscription_list.html", {
        "subscriptions": subscriptions,
        "total": total,
        "active": active,
        "expired": expired
    })


def add_subscription(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            subscription = form.save(commit=False)

            if subscription.end_date >= timezone.now().date():
                subscription.status = "Active"
            else:
                subscription.status = "Expired"

            subscription.save()
            return redirect("subscription_list")

    else:
        form = SubscriptionForm()

    return render(request, "subscription/subscription_form.html", {
        "form": form
    })


def edit_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)

    if request.method == "POST":
        form = SubscriptionForm(request.POST, instance=subscription)

        if form.is_valid():
            subscription = form.save(commit=False)

            if subscription.end_date >= timezone.now().date():
                subscription.status = "Active"
            else:
                subscription.status = "Expired"

            subscription.save()
            return redirect("subscription_list")

    else:
        form = SubscriptionForm(instance=subscription)

    return render(request, "subscription/subscription_form.html", {
        "form": form
    })


def delete_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    subscription.delete()
    return redirect("subscription_list")


def payment(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)

    order = {
        "id": "demo_order",
        "amount": int(subscription.amount * 100)
    }

    return render(request, "subscription/payment.html", {
        "subscription": subscription,
        "order": order,
        "razorpay_key": ""
    })

    order = client.order.create({
        "amount": int(subscription.amount * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, "subscription/payment.html", {
        "subscription": subscription,
        "order": order,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    })