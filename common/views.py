from common.models import Users, IPmodel, IpDayCount
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from common.backends import AuthBackend
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from datetime import date
import requests
import json

# Create your views here.
def home(request):
    context = {}
    return render(request, 'common/home.html', context)

def signup(request):
    context = {}
    if request.method == "POST":
        user = Users()
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.pswd_token = request.POST['pswd']
        user.password = make_password(request.POST['pswd'])
        user.save()
        messages.success(request, "Registered Successfully.")
        return redirect('addIp', user.id)
    return render(request, 'common/signup.html', context)

def signin(request):
    context = {}
    if request.method == "POST":
        ip_response = requests.get("https://api.ipify.org/?format=json".replace(" ", ""))
        ip_response = json.loads(ip_response.content.decode())
        ip_address = ip_response['ip']
        username = request.POST['username']
        password = request.POST['pswd']
        user = AuthBackend.authenticate(request, username=username, password=password)
        if user:
            check_api_limit_response = checkApiLimit(user.ipmodel_set.all()[0].start_ip, user.ipmodel_set.all()[0].end_ip, ip_address)
            check_api_limit_response = json.loads(check_api_limit_response.content.decode())
            if (check_api_limit_response['code'] == 200):
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, check_api_limit_response['message'])
                return redirect('signin')
    return render(request, 'common/signin.html', context)

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

def signout(request):
    logout(request)
    try:
        del request.session
    except:
        pass
    try:
        storage = messages.get_messages(request)
        for message in storage:
            message = ''
        storage.used = False
    except:
        pass
    messages.warning(request, 'Logout Successfully.')
    return redirect('signin')


def addIp(request, user_id):
    context = {'user_id' : user_id}
    if request.method == "POST":
        try:
            obj = IPmodel.objects.get(user_id=request.POST['user_id'])
            obj.start_ip = request.POST['start_ip']
            obj.end_ip = request.POST['end_ip']
            obj.save()
            messages.error(request, "IP Updated Successfully.")
        except IPmodel.DoesNotExist:
            obj = IPmodel(user_id=request.POST['user_id'], start_ip=request.POST['start_ip'], end_ip=request.POST['end_ip'])
            obj.save()
            messages.error(request, "IP Added Successfully.")
        return redirect('signin')
    return render(request, 'common/add_ip.html', context)

def dashboard(request):
    context = {}
    return render(request, 'common/dashboard.html', context)

def checkApiLimit(start_ip, end_ip, user_ip):
    user_ip = user_ip.replace(".","")
    # user = Users.objects.prefetch_related('ipmodel_set').filter(ipmodel__start_ip__lte=user_ip, ipmodel__end_ip__gte=user_ip)
    start_ip = start_ip.replace(".", "")
    end_ip = end_ip.replace(".", "")
    if (int(start_ip) <= int(user_ip) and int(end_ip) >= int(user_ip)):
        day_count = IpDayCount.objects.filter(day=date.today()).first()
        if (day_count is None):
            day_count = IpDayCount()
            day_count.day = date.today()
            day_count.count = 0
            day_count.save()
            return JsonResponse({
                'code': 200,
                'status': 'SUCCESS',
                'message': "Count is less than 0"
            })
        else:
            if day_count.count < 100:
                day_count.count = day_count.count + 1
                day_count.save()
                return JsonResponse({
                    'code': 200,
                    'status': 'SUCCESS',
                    'message': "Count is less than 0"
                })
            else:
                return JsonResponse({
                    'code': 500,
                    'status': 'Failure',
                    'message': "Login count is exceed the limit 100"
                })
    else:
        return JsonResponse({
            'code': 501,
            'status': 'Failure',
            'message': "IP address is not matching"
        })