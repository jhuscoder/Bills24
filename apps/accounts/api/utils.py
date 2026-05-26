import os
import threading
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template


class Utils:
    @staticmethod
    def send_mail(data):
        user = data['context']['user']

        # Prefer a plain template for the text body, or fallback to provided 'body'
        body = data.get('body')
        if data.get('template_plain'):
            tpl = get_template(data['template_plain'])
            body = tpl.render(data.get('context', {}))

        email = EmailMultiAlternatives(
            subject     = data.get('subject', ''),
            body        = body or '',
            from_email  = settings.EMAIL_HOST_USER,
            to          = [user.email]
        )

        # Attach HTML alternative if provided
        html_tpl = data.get('template_html') or data.get('template')
        if html_tpl:
            template = get_template(html_tpl)
            html_content = template.render(data.get('context', {}))
            email.attach_alternative(html_content, "text/html")

        email.send(fail_silently=True)

    @staticmethod
    def send_mail_threaded(data):
        # Create a new thread for sending the email
        t = threading.Thread(target=Utils.send_mail, args=(data,))
        # Set the thread as a daemon to ensure it doesn't block the main process
        t.setDaemon(True)
        # Start the thread
        t.start()