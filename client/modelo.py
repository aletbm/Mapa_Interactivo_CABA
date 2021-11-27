from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from smtplib import SMTP, SMTPRecipientsRefused
import os


def read_creds():
    """
    Lectura de ceredenciales

    Returns
    -------
    user : TYPE: string
    passw : TYPE: string

    """
    user = passw = ""
    with open(os.path.abspath("") + "/src/credentials.txt", "r") as f:
        file = f.readlines()
        user = file[0].strip()
        passw = file[1].strip()

    return user, passw


def send_email(email):
    """
    Envio de mail al usuario de su busqueda

    Parameters
    ----------
    email : string
        la funcion recibe el mail del usuario.

    Returns
    -------
    None.

    """
    sender, password = read_creds()
    msgRoot = MIMEMultipart("related")
    msgRoot["Subject"] = "Mapa Interactivo de CABA"
    msgRoot["From"] = sender
    msgRoot["To"] = email
    msgRoot.preamble = "Multi-part message in MIME format."

    msgAlternative = MIMEMultipart("alternative")
    msgRoot.attach(msgAlternative)

    message1 = 'Sr/Sra usuario:\nNuestro sistema automatico de correspondencia le ha enviado su busqueda en el mapa\n\n Atentamente, el equipo de Python'
    cuerpomail = MIMEText(message1, 'plain')
    msgAlternative.attach(cuerpomail)

    with open(os.path.abspath("") + "/src/mapa.html", 'rb') as arch:
        mapa = MIMEApplication(arch.read(), Name='mapa.html')
        mapa['Content-Disposition'] = 'attachment; filename=\"mapa.html\"'
        msgRoot.attach(mapa)

    with SMTP("smtp.office365.com", 587) as smtp:
        try: #Prueba de existenia del mail
            smtp.connect("smtp.office365.com", 587)
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sender, password)  # Username and Password of Account
            smtp.sendmail(sender, email, msgRoot.as_string())
            smtp.quit()
        except SMTPRecipientsRefused:
            print("ERROR: El email proporcionado no existe, reinicie la aplicacion e introduzca su email correctamente")
