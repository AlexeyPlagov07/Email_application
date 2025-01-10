import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "ADD EMAIL ADDRESS HERE"  # Enter your address

password = ("ADD TEMP PASS HERE")

def sendEmail(receiver_email, message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)