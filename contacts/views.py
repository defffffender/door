import json

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.models import PageSeo
from .forms import ContactForm
from .models import ContactRequest
from .telegram import send_telegram_notification

RATE_LIMIT = 3        # заявок с одного IP
RATE_WINDOW = 600     # за 10 минут


def _client_ip(request):
    return (
        request.META.get('HTTP_X_REAL_IP')
        or request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
        or request.META.get('REMOTE_ADDR', '')
    )


def _is_spam(request, data=None):
    """Honeypot: скрытое поле 'website' заполняют только боты."""
    value = (data if data is not None else request.POST).get('website') or ''
    return bool(value.strip())


def _rate_limited(request):
    key = f'contact-rate:{_client_ip(request)}'
    if cache.add(key, 1, RATE_WINDOW):
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, RATE_WINDOW)
        return False
    return count > RATE_LIMIT


def contacts(request):
    if request.method == 'POST':
        # Спамерам отвечаем как при успехе, чтобы они не адаптировались
        if _is_spam(request) or _rate_limited(request):
            messages.success(request, 'Ваша заявка успешно отправлена!')
            return redirect('contacts')
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact_request = form.save()
            send_telegram_notification(contact_request)
            messages.success(request, 'Ваша заявка успешно отправлена!')
            return redirect('contacts')
    else:
        form = ContactForm()
    try:
        page_seo = PageSeo.objects.get(page='contacts')
    except PageSeo.DoesNotExist:
        page_seo = None
    return render(request, 'contacts/contacts.html', {'form': form, 'page_seo': page_seo})


@require_POST
def chat_submit(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Неверный формат'}, status=400)

    name = (data.get('name') or '').strip()
    phone = (data.get('phone') or '').strip()
    email = (data.get('email') or '').strip()
    message = (data.get('message') or '').strip()

    if not name or not phone:
        return JsonResponse({'success': False, 'error': 'Имя и телефон обязательны'}, status=400)

    if _is_spam(request, data) or _rate_limited(request):
        return JsonResponse({'success': True})

    contact = ContactRequest.objects.create(
        name=name, phone=phone, email=email, message=message,
    )
    send_telegram_notification(contact)
    return JsonResponse({'success': True})
