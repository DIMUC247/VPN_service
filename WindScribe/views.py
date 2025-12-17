from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from faker import Faker
from django.shortcuts import redirect

from .models import Subscription, Service
from .forms import SubForm

# Create your views here.

fake =Faker()


def get_subscribtions_view(request: HttpRequest):
    form = SubForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        subscription = form.cleaned_data.get("sub")
        service, _= Service.objects.get_or_create(user=request.user)

        service.subscription = subscription
        service.ipv_4_local = fake.ipv4_private() if "ipv_4_local" in subscription.services else None
        service.ipv_4_ext = fake.ipv4_public() if "ipv_4_ext" in subscription.services else None
        service.ipv_6 = fake.ipv6() if "ipv_6" in subscription.services else None

        service.save()
        return redirect("index")
    return render(request, "subscription.html", dict(form=form))
