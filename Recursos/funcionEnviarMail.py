import smtplib, os
from email.mime.image import MIMEImage
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(email_subject, receiver_email_address, username, password):
    sender_email_address = "carlos.anthonio.15.07@gmail.com" 
    email_smtp = "smtp.gmail.com"
    email_password = "inhrxgeuxurwleqa" 

    message = MIMEMultipart()
    message['Subject'] = email_subject
    message['From'] = sender_email_address
    message['To'] = receiver_email_address

    # Crea una parte HTML del mensaje
    mensaje_html = """
    <html>
        <body>
            <div style="font-family: Arial, sans-serif; background-color: #f4f4f4;">
                <h1 style="color: #0073e6;">Credenciales de Acceso</h1>
                <p style="font-size: 18px;">¡Bienvenido a nuestra plataforma!</p>
                <p style="font-size: 18px;">A continuación, te proporcionamos tus credenciales de acceso:</p>
                <p style="font-size: 18px;">Nombre de usuario: <strong>{}</strong></p>
                <p style="font-size: 18px;">Contraseña: <strong>{}</strong></p>
                <p style="font-size: 18px;">Por favor, guárdalos en un lugar seguro.</p>
                <p style="font-size: 18px; background-color: #0073e6; color: #ffffff; padding: 10px; border-radius: 5px;">Accede a la plataforma mediante el script proporcionado por tu gestor local</p>
            </div>
        </body>
    </html>
    """.format(username, password)

    # Convierte el contenido HTML en un objeto MIMEText
    mensaje_html_part = MIMEText(mensaje_html, 'html')

    # Agrega la parte HTML al mensaje
    message.attach(mensaje_html_part)

    server = smtplib.SMTP(email_smtp, 587)
    server.ehlo()
    server.starttls()
    server.login(sender_email_address, email_password)
    server.sendmail(sender_email_address, receiver_email_address, message.as_string())
    server.quit()


def send_user_slice(email_subject, receiver_email_address, username, credenciales, imagen):
    sender_email_address = "carlos.anthonio.15.07@gmail.com" 
    email_smtp = "smtp.gmail.com"
    email_password = "inhrxgeuxurwleqa" 

    message = MIMEMultipart()
    message['Subject'] = email_subject
    message['From'] = sender_email_address
    message['To'] = receiver_email_address
    format_credentials = formatear(credenciales)
    # Crea una parte HTML del mensaje
    mensaje_html = """
    <html>
        <body>
            <div style="font-family: Arial, sans-serif; background-color: #f4f4f4;">
                <h1 style="color: #0073e6;">Credenciales de Acceso a su Slice</h1>
                <p style="font-size: 18px;">¡Bienvenido a nuestra plataforma {}!</p>
                <p style="font-size: 18px;">A continuación, te proporcionamos tus credenciales de acceso a los equipos de tu proyecto:</p>
                {}
                <p style="font-size: 18px;">Asimismo, te adjuntamoos una imagen de visualización de tu topología creada</p>
                <p style="font-size: 18px; background-color: #0073e6; color: #ffffff; padding: 10px; border-radius: 5px;">Accede a la plataforma mediante el script proporcionado por tu gestor local</p>
            </div>
        </body>
    </html>
    """.format(username, format_credentials)

    # Convierte el contenido HTML en un objeto MIMEText
    mensaje_html_part = MIMEText(mensaje_html, 'html')

    # Agrega la parte HTML al mensaje
    message.attach(mensaje_html_part)

    # Agrega la imagen
    with open(imagen, 'rb') as imagen_file:
        imagen_data = imagen_file.read()
        imagen_part = MIMEImage(imagen_data, name = imagen)
        message.attach(imagen_part)
    
    server = smtplib.SMTP(email_smtp, 587)
    server.ehlo()
    server.starttls()
    server.login(sender_email_address, email_password)
    server.sendmail(sender_email_address, receiver_email_address, message.as_string())
    server.quit()
    os.remove(imagen)

def formatear(credenciales):
    resultado = ""
    for vm in credenciales:
        nombre_o_alias = vm["alias"] if vm["alias"] else vm["nombre"]
        resultado += f"<p><strong>{nombre_o_alias}:</strong> <a href='{vm['linkAcceso']}' target='_blank'>Acceso</a></p>"
    return resultado