import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.models import PageSeo
from .forms import ContactForm
from .models import ContactRequest
from .telegram import send_telegram_notification


def contacts(request):
    if request.method == 'POST':
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

    contact = ContactRequest.objects.create(
        name=name, phone=phone, email=email, message=message,
    )
    send_telegram_notification(contact)
    return JsonResponse({'success': True})
