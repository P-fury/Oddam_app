from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator


def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))
    message = f'Jeśli zakładałeś konto na Oddam App użyj linku do aktywacji konta: {link}'
    mail_subject = 'Aktywuj konto Oddam App.'
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def send_reset_password_email(user, request):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    link = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
    message = f"""Została wysłana prośba o restart hasła jeżeli to ty klinkij w : {link}
                    Jesli nie zignoruj wiadmość
                    """
    mail_subject = 'Reset hasłą Oddam App.'
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
