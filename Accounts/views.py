from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .forms import ProfileForm, UserForm
from .serializers import ProfileSerializer

from .forms import LoginForm

from .models import Profile
# Create your views here.


def sign_up(request:HttpRequest):
    form = SignUpForm(data=request.POST or None)
    if request.method == "POST" :
        if form.is_valid():
            form.save()
            # messages.success(request=request, message="Реєстрація пройшла успішно")
            # return redirect("sign_in")
            return JsonResponse(dict(status="success"),status=200)
        else:
            return JsonResponse(dict(status="error",errors=form.errors),status=400)
    return render(request, "sign_up.html", dict(form=form))


def sign_in(request:HttpRequest):
    form = LoginForm(request,data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )
        if not user:
            messages.error(request=request, message="Неправильний логін або пароль")
            return redirect("sign_in")

        login(request=request, user=user)
        if not form.cleaned_data.get("remember"):
            request.session.set_expiry(None)

        return redirect("index")
    return render(request, "sign_in.html", dict(form=form))

@login_required
def index(request:HttpRequest):
    return render(request, "index.html")

@login_required
def logout_user(request:HttpRequest):
    logout(request)
    return redirect("sign_in")


@login_required
@require_GET
# @cache_page(30)
def profile_get(request:HttpRequest):
    # user = cache.get(f"user_form{request.user.username}")
    # profile = cache.get(f"profile_form{request.user.username}")

    # if not user:
    #     user = request.user
    #     cache.set(f"user_form{request.user.username}",user,30)

    # if not profile:
    #     profile = request.user.details
    #     cache.set(f"profile_form{request.user.username}", profile,30)

    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.details)

    return render(request, "profile.html", context=dict(user_form=user_form, profile_form=profile_form))


@login_required
@require_POST
def profile_post(request:HttpRequest):
    user_form = UserForm(data=request.POST, instance=request.user)
    profile_form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.details)
    messages.info(request=request, message="Профіль успішно оновлено")

    if profile_form.is_valid():

        if user_form.is_valid() and user_form.changed_data:
            user_form.save()

        if profile_form.changed_data:
            profile_form.save()
    else:
        messages.error(request=request, message="Невірна капча. Спробуйте ще раз.")

    return redirect("profile")


@api_view(['GET'])
def test_api(request:HttpRequest):
    profile = Profile.objects.get(user=request.user)
    data = ProfileSerializer(profile)
    return Response(data.data)

