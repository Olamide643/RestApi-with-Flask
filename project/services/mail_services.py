from threading import Thread
from flask_mail import Message

from project import app, mail
from project.error.errors import InternalServerError

def send_sync_mail(app,msg):
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise InternalServerError("[MAIL SERVER] not working")
            
def send_mail(subject,sender,recipients, text_body,html_body):
    msg = Message(subject,sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target= send_sync_mail, args=(app,msg)).start()



