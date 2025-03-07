from django.contrib.auth import logout, login
from django.shortcuts import render, redirect

from webapp.forms import RegisterForm, OrderForm
from webapp.models import UserProfile


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')

def account(request):
    if request.user.is_superuser:
        return redirect('panel_admin')

    return render(request, 'account.html')

def panel_admin(request):
    if not request.user.is_superuser:
        return redirect('account')

    return render(request, 'panel_admin.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            fio = request.POST['fio']
            phone = request.POST['phone']
            user_profile = UserProfile.objects.create(user=user, fio=fio, phone=phone)
            user_profile.save()

            login(request, user)
            return redirect('account')

    context = {'form': form}
    return render(request, 'register.html', context)

def add_order_index(request):
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            return redirect('index')

    context = {'form': form}
    return render(request, 'index', context)

