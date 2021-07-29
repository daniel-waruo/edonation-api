from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import AccountConfirmationTokenGenerator


def create_token(token_model, user, serializer):
    instance, token = token_model.objects.create(user=user)
    return token


def send_confirmation_email(user, use_https=False, token_generator=AccountConfirmationTokenGenerator()):
    """
    Send user an email which will be used to confirm their email address
    Args:
        user:
        use_https:
        token_generator:
    """
    # specify templates
    subject_template_name = 'pg_account/emails/email_confirm_subject.txt'
    email_template_name = 'pg_account/emails/user_confirmation_email.html'
    # get the encoded user id and the generated token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    # get the protocol that the use
    protocol = 'https' if use_https else 'http'
    base_url = f'{protocol}://{settings.API_DOMAIN}'
    context = {
        "user": user,
        "uid": uid,
        "token": token,
        "base_url": base_url,
        "company_name": settings.COMPANY_NAME
    }
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)
    html_email = loader.render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, None, [user.email])
    email_message.attach_alternative(html_email, 'text/html')
    email_message.send()
