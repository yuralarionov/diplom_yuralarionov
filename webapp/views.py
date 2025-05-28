import os
from datetime import datetime, timedelta
from io import BytesIO

from django.contrib.auth import logout, login
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from docxtpl import DocxTemplate
from urllib.parse import urlparse

from webapp.forms import RegisterForm, OrderForm, AutoForm, ReviewsForm, OrderFormAnon
from webapp.models import UserProfile, Auto, Order, Mark, AutoModel, Reviews, ServiceCategory


def index(request):
    form_order = OrderForm(user=request.user) if request.user.is_authenticated else None
    form_order_anon = OrderFormAnon() if not request.user.is_authenticated else None

    form_reviews = ReviewsForm()

    reviews = Reviews.objects.all().order_by('-datetime')[:6]

    service_categories = ServiceCategory.objects.prefetch_related('services').all().order_by('order')

    context = {
        'form_order': form_order,
        'form_order_anon': form_order_anon,
        'form_reviews': form_reviews,
        'reviews': reviews,
        'service_categories': service_categories}
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    form_order = OrderForm(user=request.user) if request.user.is_authenticated else None
    form_order_anon = OrderFormAnon() if not request.user.is_authenticated else None
    service_categories = ServiceCategory.objects.prefetch_related('services').all().order_by('order')

    context = {
        'form_order': form_order,
        'form_order_anon': form_order_anon,
        'service_categories': service_categories}

    return render(request, 'contact.html', context)


def services(request):
    form_order = OrderForm(user=request.user) if request.user.is_authenticated else None
    form_order_anon = OrderFormAnon() if not request.user.is_authenticated else None
    service_categories = ServiceCategory.objects.prefetch_related('services').all().order_by('order')

    context = {
        'form_order': form_order,
        'form_order_anon': form_order_anon,
        'service_categories': service_categories}

    return render(request, 'services.html', context)


def account(request):
    if request.user.is_superuser:
        return redirect('panel_admin')

    userprofile = UserProfile.objects.get(user=request.user)
    user_autos = Auto.objects.filter(user=request.user)
    order = Order.objects.filter(user=request.user).order_by("-create_date")[:30]
    marks = Mark.objects.all()
    service_categories = ServiceCategory.objects.prefetch_related('services').all().order_by('order')

    if request.method == 'POST' and 'add_auto' in request.POST:
        form_auto = AutoForm(request.POST)
        if form_auto.is_valid():
            auto = form_auto.save(commit=False)
            auto.user = request.user
            auto.save()
            messages.success(request, 'Вы успешно добавили автомобиль!')
        else:
            messages.error(request, 'Произошла ошибка! Проверьте данные!')

        return redirect('account')
    else:
        form_auto = AutoForm()

    context = {
        'form_order': OrderForm(user=request.user),
        'form_auto': form_auto,
        'userprofile': userprofile,
        'auto': user_autos,
        'order': order,
        'marks': marks,
        'service_categories': service_categories
    }
    return render(request, 'account.html', context)


def get_models(request):
    mark_id = request.GET.get('mark_id')
    models = AutoModel.objects.filter(mark_id=mark_id).values('id', 'model')
    return JsonResponse({'models': list(models)})


def get_models_add_auto(request):
    mark_id = request.GET.get('mark_id')
    models = AutoModel.objects.filter(mark_id=mark_id).values('id', 'model')
    return JsonResponse(list(models), safe=False)


def panel_admin(request):
    if not request.user.is_superuser:
        return redirect('account')
    now = datetime.now()
    five_days_ago = now - timedelta(days=31)
    order = Order.objects.filter(create_date__gte=five_days_ago).order_by('-create_date')
    context = {'order': order}
    return render(request, 'panel_admin.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из учётной записи!')
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
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('account')
        else:
            messages.error(request, 'Произошла ошибка! Проверьте данные!')

    context = {'form': form}
    return render(request, 'register.html', context)


def is_safe_url(url, allowed_hosts):
    if not url:
        return False
    try:
        parsed = urlparse(url)
        return (not parsed.netloc or parsed.netloc in allowed_hosts)
    except:
        return False


def add_order(request):
    next_url = request.POST.get('next', None)
    if request.method == 'POST':
        if not request.user.is_anonymous:
            form = OrderForm(request.POST, user=request.user)
        else:
            form = OrderFormAnon(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if not request.user.is_anonymous:
                order.user = request.user
            order.save()

            selected_services = form.cleaned_data['service']
            order.service.set(selected_services)

            if next_url and is_safe_url(next_url, allowed_hosts={request.get_host()}):
                messages.success(request, 'Вы успешно оставили заявку!')
                return redirect(next_url)
        else:
            if next_url and is_safe_url(next_url, allowed_hosts={request.get_host()}):
                messages.error(request, 'Произошла ошибка! Проверьте данные!')
                return redirect(next_url)


def add_reviews(request):
    form = ReviewsForm()

    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            reviews = form.save(commit=False)
            if not request.user.is_anonymous:
                reviews.user = request.user
            else:
                reviews.user = None
            reviews.save()
            messages.success(request, 'Вы успешно оставили отзыв!')
        else:
            messages.error(request, 'Произошла ошибка! Проверьте данные!')

        return redirect('index')


def download_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    template_path = os.path.join('templates', 'template.docx')
    doc = DocxTemplate(template_path)

    services = order.service.all()
    service_names = [service.name for service in services]
    service_prices = [service.price for service in services]

    total_price = sum(service_prices)

    if order.comment:
        comment = order.comment
    else:
        comment = 'Не указано'

    context = {
        'id': order.id,
        'create_date': order.create_date.strftime('%d.%m.%Y'),
        'datetime': order.datetime.strftime('%d.%m.%Y %H:%M'),
        'fio': order.user.userprofile.fio,
        'phone': order.user.userprofile.phone,
        'mark': order.auto.mark_model.mark.mark,
        'model': order.auto.mark_model.model,
        'released_year': order.auto.released_year,
        'gos_num': order.auto.gos_num,
        'engine_num': order.auto.engine_num,
        'vin_num': order.auto.vin_num,
        'comment': comment,
        'services': service_names,
        'prices': service_prices,
        'total_price': total_price,
        'worker': order.worker
    }

    doc.render(context)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type='order/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename=order_{order.id}.docx'

    return response


def waiting(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = '1'
    order.save()
    messages.success(request, 'Успешное выполнение операции!')
    return redirect('panel_admin')


def agreement(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = '2'
    order.save()
    messages.success(request, 'Успешное выполнение операции!')
    return redirect('panel_admin')


def at_work(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = '3'
    order.save()
    messages.success(request, 'Успешное выполнение операции!')
    return redirect('panel_admin')


def ready(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = '4'
    order.save()
    messages.success(request, 'Успешное выполнение операции!')
    return redirect('panel_admin')


def given(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = '5'
    order.save()
    messages.success(request, 'Успешное выполнение операции!')
    return redirect('panel_admin')


def cancel(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.reason = request.POST['reason']
        order.status = '6'
        order.save()
        messages.success(request, 'Успешное выполнение операции!')
        return redirect('panel_admin')

    return render(request, 'panel_admin')


def change_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        if request.POST['datetime'] != '':
            order.datetime = request.POST['datetime']
        order.worker = request.POST['worker']
        order.info = request.POST['info']
        order.save()
        messages.success(request, 'Успешное выполнение операции!')
        return redirect('panel_admin')

    return render(request, 'panel_admin')

