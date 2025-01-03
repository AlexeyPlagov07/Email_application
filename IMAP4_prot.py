import imaplib, email
import os
from email.header import decode_header

# Initialize IMAP connection
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login('alexeyplagov@gmail.com', 'lmas fwyf pgij mlzu')

# Select the inbox
status, messages = imap.select("INBOX")
numOfMessages = int(messages[0])

z = []  # List for storing subject and sender info
y = []  # List for storing email body content

def clean(text):
    # Clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def obtain_header(msg):
    # Decode the email subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)

    # Decode email sender
    From, encoding = decode_header(msg.get("From"))[0]
    if isinstance(From, bytes):
        From = From.decode(encoding)

    # Store subject and sender in z list
    z.append([subject, From])
    return subject, From

def download_attachment(part):
    # Download email attachment
    filename = part.get_filename()
    if filename:
        folder_name = clean(subject)
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
            filepath = os.path.join(folder_name, filename)
            open(filepath, "wb").write(part.get_payload(decode=True))

def extract_body(msg):
    # Function to extract the email body (handling both text/plain and text/html)
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            # If the part is plain text or html, extract the body
            try:
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    break  # We stop once we find the plain text body
                elif content_type == "text/html" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    break  # We stop once we find the html body
            except:
                continue
    else:
        # For non-multipart emails, directly extract the body
        body = msg.get_payload(decode=True).decode()

    return body

# Fetch emails and store details
for i in range(numOfMessages, numOfMessages - 100, -1):
    try:
        res, msg = imap.fetch(str(i), "(RFC822)")  # Fetch the email using its ID
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, From = obtain_header(msg)
                
                # Extract the body content
                body = extract_body(msg)
                if body:
                    y.append((subject, From, body))  # Store subject, sender, and body as a tuple
    except TypeError:
        pass
imap.close()

def return_y():
    return y
def return_z():
    return z