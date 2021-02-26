from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .forms import Deposit_form
from .forms import Withdrawl_form
from django.core.mail import send_mail
from banking.settings import EMAIL_HOST_USER


def home(request):
    return render(request, 'accounts/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Create a Bank Account"
        form = UserRegistrationForm(
            request.POST or None,
            request.FILES or None
            )

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)

            return HttpResponseRedirect("/Banking/")

        context = {"title": title, "form": form}

        return render(request, "accounts/form.html", context)


def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('user_success'))
        else:
            context["error"] = "Provide valid credentials !!"
            return render(request, "accounts/login.html", context)
    else:
        return render(request, "accounts/login.html", context)


@login_required(login_url="/login/")
def success(request):
    context = {}
    context['user'] = request.user
    return render(request, "accounts/success.html", context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/Banking/')


def deposit(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Deposit"
        form = Deposit_form(request.POST or None,
                            request.FILES or None)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            # adds users deposit to balance.
            deposit.user.balance += deposit.amount
            deposit.user.save()
            deposit.save()
            # After Depositing Amount User gets the email notification
            subject = "Transaction Details"
            message = 'You Have Deposited {} $.'.format(deposit.amount)
            recepient = request.user.email
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            messages.success(request, 'You Have Deposited {} $.'
                             .format(deposit.amount))
            return HttpResponseRedirect("/Banking/account_details/")

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "accounts/form.html", context)


def withdrawl(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Withdrawl"
        form = Withdrawl_form(request.POST or None)

        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user

            if withdrawal.user.balance >= withdrawal.amount:

                withdrawal.user.balance -= withdrawal.amount
                withdrawal.user.save()
                withdrawal.save()
                # After Withdrawl Amount User gets the email notification
                subject = "Transaction Details"
                message = 'You Have Withdrawl {} $.'.format(withdrawal.amount)
                recepient = request.user.email
                send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
                return HttpResponseRedirect("/Banking/account_details/")

            else:
                return render(request, "accounts/withdraw_error.html")

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "accounts/form.html", context)


@login_required(login_url="/login/")
def account_details(request):
    # if request.user.is_authenticated:
    return render(request, "accounts/account_details.html")
