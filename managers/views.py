from django.http import HttpResponseRedirect, HttpResponse
import xlwt
from accounts.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from managers.forms import ManagerForm


def home(request):
    return render(request, 'managers/home.html')


def register(request):
    if request.method == "POST":
        form = ManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/managers/')
    else:
        form = ManagerForm()
    return render(request, 'managers/register.html', {"form": form})


def managers_login(request):
    if request.method == "POST":
        user_email = request.POST.get('email')
        password = request.POST.get("password")
        user_manager = authenticate(request, email=user_email, password=password)
        if user_manager is not None:
            login(request, user_manager)
            return HttpResponseRedirect('/managers/')
        else:
            return render(request, "managers/login.html", {"error": "Provide valid credentials"})

    return render(request,"managers/login.html")


def managers_logout(request):
    logout(request)
    return HttpResponseRedirect('/managers/')


def login_success(request):
    context={}
    context['user'] = request.user
    return render(request, "accounts/success_login.html", context)



# Excel Download Functionality
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="profiles.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('User_Profiles')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['full_name',  'email', 'contact_no', 'account_no', 'balance']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = UserProfile.objects.all().values_list('full_name',  'email', 'contact_no', 'account_no',
                                                 'balance')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response