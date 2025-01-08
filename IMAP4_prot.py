import imaplib
import email
from email.header import decode_header
import spam_detect

y = []

# Connect to the server
mail = imaplib.IMAP4_SSL("imap.gmail.com")

# Login to your account
username = "alexeyplagov@gmail.com"
password = "lmas fwyf pgij mlzu"
mail.login(username, password)

# Select the mailbox you want to use (in this case, the inbox)
mail.select("inbox")

# Search for all emails in the mailbox
status, messages = mail.search(None, "ALL")

# Convert messages to a list of email IDs
email_ids = messages[0].split()

# Get the last 50 email IDs (if there are less than 50, it'll fetch all)
last_50_email_ids = email_ids[-200:]

# Iterate through each of the last 50 emails
try:
    for email_id in last_50_email_ids:
        # Fetch the email by ID
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        # Initialize variables for plain text and HTML
        plain_text_body = ""
        html_body = ""

        # Get the email content
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):  
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg.get("From")

                # If the email message is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        # Check if the part is plain text
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            try:
                                # Extract plain text body
                                plain_text_body = part.get_payload(decode=True).decode()
                            except:
                                pass
                        # Check if the part is HTML
                        elif content_type == "text/html" and "attachment" not in content_disposition:
                            try:
                                # Extract HTML body
                                html_body = part.get_payload(decode=True).decode()
                            except:
                                pass
                else:
                    # If the email is not multipart, extract the body
                    content_type = msg.get_content_type()

                    # If the content type is plain text, decode the body
                    if content_type == "text/plain":
                        plain_text_body = msg.get_payload(decode=True).decode()
                    # If the content type is HTML, decode the body
                    elif content_type == "text/html":
                        html_body = msg.get_payload(decode=True).decode()

                # Use the spam detection function on the plain text body
                spam_return = spam_detect.test_data(plain_text_body)

                # Append the email data (subject, sender, plain text body, HTML body, spam result) to the list
                y.append([subject, from_, plain_text_body, False, spam_return])
except TypeError:
    pass

# Close the connection and logout
mail.close()
mail.logout()

def return_y():
    return y
