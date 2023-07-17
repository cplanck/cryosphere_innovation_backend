from dataclasses import field

from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import exceptions, serializers

from general.models import UpdatesAndChanges


class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    def get_email_options(self):

        user = User.objects.get(
            email=self.context['request'].data['email'])
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        domain = str(settings.WEBSITE_ROOT),
        frontend_domain = settings.STANDALONE_FRONTEND_ROOT

        return {
            'subject_template_name': 'registration/password_reset_subject.txt',
            'html_email_template_name': 'registration/password_reset_email.html',
            'extra_email_context': {'user': 'Cameron', 'backend_domain': domain[0], 'frontend_domain': frontend_domain, 'uid': uid, 'token': token}
        }


class UpdatesAndChangesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpdatesAndChanges
        fields = '__all__'
