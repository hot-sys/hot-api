import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import threading
from dotenv import load_dotenv
load_dotenv()

def sendMail(targetMail, subject, content):
    def send():
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = os.getenv('SMTP_USER')  
        smtp_password = os.getenv('SMTP_PASSWORD') 

        if not smtp_user or not smtp_password:
            print("SMTP credentials are not set.")
            return

        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = targetMail
        msg['Subject'] = subject

        body = content
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            text = msg.as_string()
            server.sendmail(smtp_user, targetMail, text)
            print(f'Email sent successfully to {targetMail}')
        except Exception as e:
            print(f'Error sending email to {targetMail}:', e)
        finally:
            server.quit()

    # Run the send function in a new thread
    email_thread = threading.Thread(target=send)
    email_thread.start()
