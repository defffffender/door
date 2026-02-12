from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import PageSeo
from .forms import ContactForm
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
