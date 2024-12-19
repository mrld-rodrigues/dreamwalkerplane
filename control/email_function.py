import smtplib
import ssl
from email.message import EmailMessage
from control.email_config import login, senha, email_receiver

class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem

def send_email(contato):
    msg = EmailMessage()
    msg['Subject'] = f'Visitante do DreamWalker Plane - {contato.nome}'
    msg['From'] = login
    msg['To'] = email_receiver   
    body = f"""
    Nome: {contato.nome}\n
    Email: {contato.email}\n
    Mensagem:\n              {contato.mensagem}
    """
    msg.set_content(body)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(login, senha)
        smtp.send_message(msg)
