from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))
    message = f'Please use the following link to activate your account: {link}'
    mail_subject = 'Activate your account.'
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
