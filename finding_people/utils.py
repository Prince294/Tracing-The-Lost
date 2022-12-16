from django.conf import settings
from twilio.rest import Client
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
import os
from pathlib import Path
        
class Util:
    @staticmethod
    def send_email(data):
        
        contxt = {
            'username':data['username'],
            'OTP':data['otp']
        }
        message = get_template('mail.html').render(contxt)
        email = EmailMessage(
            subject='Verify Your Email',
            body=message,
            from_email="TTL - Verification "+os.environ.get('EMAIL_FROM'),
            to=[data['email_to']]
        )
        email.content_subtype = 'html'
        
        email.send(fail_silently=False)
        
        
    def send_sms(data):
        otp = data['otp']
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        message = f"Thank you for Choosing TTL. Your Verification OTP is: {otp}"
        sms = client.messages.create(body=message,from_='+16692087865',to=data['mobile'])
        
