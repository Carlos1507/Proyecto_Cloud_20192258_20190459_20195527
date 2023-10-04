import smtplib 
from email.message import EmailMessage 

def send_email(email_subject, receiver_email_address, cc_address, content):
    sender_email_address = "carlos.anthonio.15.07@gmail.com" 
    email_smtp = "smtp.gmail.com" 
    email_password = "inhrxgeuxurwleqa" 

    message = EmailMessage() 



    

    message['Subject'] = email_subject 
    message['From'] = sender_email_address 
    message['To'] = receiver_email_address 
    message['Cc'] = cc_address

    message.set_content(content) 
    server = smtplib.SMTP(email_smtp, '587') 
    server.ehlo() 
    server.starttls() 
    server.login(sender_email_address, email_password) 
    server.send_message(message) 
    server.quit()