from contacts.models import ContactRequest


def unread_contacts(request):
    if request.user.is_authenticated and request.path.startswith('/panel'):
        return {'unread_contacts': ContactRequest.objects.filter(is_read=False).count()}
    return {}
