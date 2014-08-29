# -*- coding: utf-8 -*-



import smtplib
from email.mime.text import MIMEText
from settings import jinja_env

def send_mail(email, subject, text):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('noreply@webgenesis.ru', 'noreply13')
    msg = MIMEText(text.encode('utf-8'), 'html')
    msg['Subject'] = subject.encode('utf-8')
    msg['From'] = 'LifeRacing'
    msg['To'] = email
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    
    
def send_html_mail(email, subject, template_name, context):
    send_mail(email, subject, jinja_env.get_template(template_name).render(context))
