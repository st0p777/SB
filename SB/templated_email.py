import os
import logging
from smtplib import SMTPException
from django.conf import settings
from django.utils.safestring import mark_safe

logger = logging.getLogger('helpdesk')


def send_templated_mail(template_name, context, recipients, sender=None, bcc=None, fail_silently=False, files=None, extra_headers=None):
    from django.core.mail import EmailMultiAlternatives
    from django.template import engines
    from_string = engines['django'].from_string

    from .models import EmailTemplate
    from .settings import HELPDESK_EMAIL_SUBJECT_TEMPLATE, HELPDESK_EMAIL_FALLBACK_LOCALE

    headers = extra_headers or {}

    locale = context['queue'].get('locale') or HELPDESK_EMAIL_FALLBACK_LOCALE

    try:
        t = EmailTemplate.objects.get(template_name__iexact=template_name, locale=locale)
    except EmailTemplate.DoesNotExist:
        try:
            t = EmailTemplate.objects.get(template_name__iexact=template_name, locale__isnull=True)
        except EmailTemplate.DoesNotExist:
            logger.warning('template "%s" does not exist, no mail sent', template_name)
            return

    subject_part = from_string(
        HELPDESK_EMAIL_SUBJECT_TEMPLATE % {
            "subject": t.subject
        }).render(context).replace('\n', '').replace('\r', '')

    footer_file = os.path.join('helpdesk', locale, 'email_text_footer.txt')

    text_part = from_string(
        "%s\n\n{%% include '%s' %%}" % (t.plain_text, footer_file)
    ).render(context)

    email_html_base_file = os.path.join('helpdesk', locale, 'email_html_base.html')
    if 'comment' in context:
        context['comment'] = mark_safe(context['comment'].replace('\r\n', '<br>'))

    html_part = from_string(
        "{%% extends '%s' %%}"
        "{%% block title %%}%s{%% endblock %%}"
        "{%% block content %%}%s{%% endblock %%}" %
        (email_html_base_file, t.heading, t.html)
    ).render(context)

    if isinstance(recipients, str):
        if recipients.find(','):
            recipients = recipients.split(',')
    elif type(recipients) != list:
        recipients = [recipients]

    msg = EmailMultiAlternatives(subject_part, text_part,
                                 sender or settings.DEFAULT_FROM_EMAIL,
                                 recipients, bcc=bcc,
                                 headers=headers)
    msg.attach_alternative(html_part, "text/html")

    if files:
        for filename, filefield in files:
            filefield.open('rb')
            content = filefield.read()
            msg.attach(filename, content)
            filefield.close()
    logger.debug('Sending email to: {!r}'.format(recipients))

    try:
        return msg.send()
    except SMTPException as e:
        logger.exception('SMTPException raised while sending email to {}'.format(recipients))
        if not fail_silently:
            raise e
        return 0
