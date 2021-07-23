from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountConfirmationTokenGenerator(PasswordResetTokenGenerator):
    """ Token Generator for creating account confirmation urls """

    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{user.password}{user.email_confirmed}{timestamp}'


account_activation_token = AccountConfirmationTokenGenerator()
