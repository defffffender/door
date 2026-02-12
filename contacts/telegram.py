import logging
import threading
import urllib.request
import urllib.parse

logger = logging.getLogger(__name__)


def send_telegram_notification(contact_request):
    """Send contact request notification to Telegram in background thread."""
    from core.models import SiteSettings
    settings = SiteSettings.load()

    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return

    token = settings.telegram_bot_token
    chat_id = settings.telegram_chat_id

    text = (
        f"📩 <b>Новая заявка с сайта</b>\n\n"
        f"👤 <b>Имя:</b> {contact_request.name}\n"
        f"📞 <b>Телефон:</b> {contact_request.phone}\n"
    )
    if contact_request.email:
        text += f"📧 <b>Email:</b> {contact_request.email}\n"
    if contact_request.message:
        text += f"💬 <b>Сообщение:</b>\n{contact_request.message}\n"
    text += f"\n🕐 {contact_request.created_at:%d.%m.%Y %H:%M}"

    def _send():
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = urllib.parse.urlencode({
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML',
            }).encode()
            req = urllib.request.Request(url, data=data)
            urllib.request.urlopen(req, timeout=10)
            logger.info("Telegram notification sent for request #%s", contact_request.pk)
        except Exception as e:
            logger.error("Failed to send Telegram notification: %s", e)

    thread = threading.Thread(target=_send, daemon=True)
    thread.start()
