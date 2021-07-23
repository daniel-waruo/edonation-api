from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm, UserModel
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class PasswordResetForm(BasePasswordResetForm):
    def save(self,
             domain_override=settings.API_DOMAIN,
             subject_template_name='pg_account/emails/password_reset_subject.txt',
             email_template_name='pg_account/emails/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None,
             html_email_template_name='pg_account/emails/password_reset_email.html',
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        email_field_name = UserModel.get_email_field_name()
        domain = domain_override
        company_name = settings.COMPANY_NAME
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            protocol = 'https' if use_https else 'http'
            endpoint = 'accounts/reset'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            password_reset_url = f'{protocol}://{domain}/{endpoint}/{uid}/{token}'
            print(token_generator.check_token(user, token))
            context = {
                'domain': domain,
                'password_reset_url': password_reset_url,
                'company_name': company_name,
                'user': user,
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )
