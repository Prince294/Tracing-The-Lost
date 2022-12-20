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
        subject = ''
        message = ''
        email_name = ''
        
        typeof_mail = data['type']
        if typeof_mail == 'otp':
            contxt = {
                'username':data['username'],
                'OTP':data['otp']
            }
            message = get_template('mail.html').render(contxt)
            subject = 'Verify Your Email'
            email_name = "TTL - Verification "
            
        elif typeof_mail == 'police_verification':
            contxt = {
                'name':data['name'],
                'verify_link':data['verify_link']
            }
            message = get_template('police-verification.html').render(contxt)
            subject='Found a Suspect in Your Location'
            email_name = 'TTL - Suspect Verification '
        
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=email_name+os.environ.get('EMAIL_FROM'),
            to=[data['email_to']]
        )
        email.content_subtype = 'html'
        
        email.send(fail_silently=False)
        
        
    def send_sms(data):
        otp = data['otp']
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        message = f"Thank you for Choosing TTL. Your Verification OTP is: {otp}"
        sms = client.messages.create(body=message,from_='+16692087865',to=data['mobile'])
        
