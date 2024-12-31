# -*- coding: utf-8 -*-

import imaplib, email
import os
from email.header import decode_header
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets

# Initialize IMAP connection
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login('alexeyplagov@gmail.com', 'myjf xtbg oqkl pecj')

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

# Fetch emails and store details
for i in range(numOfMessages, numOfMessages - 20, -1):
    try:
        res, msg = imap.fetch(str(i), "(RFC822)")  # Fetch the email using its ID
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, From = obtain_header(msg)

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            var_x = body
                        elif "attachment" in content_disposition:
                            download_attachment(part)
                else:
                    content_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        var_x = body

                y.append(var_x)  # Store email body
    except TypeError:
        pass
imap.close()

# PyQt5 GUI
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)

        # Left QListWidget for subjects and senders
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 201, 301))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemClicked.connect(self.on_item_clicked)
        self.listWidget.resize(600,400)
        # Right QListWidget for email content
        self.listWidget_2 = QtWidgets.QListWidget(Dialog)
        self.listWidget_2.setGeometry(QtCore.QRect(400, 0, 201, 301))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.resize(600,400)

        # Populate the left list with subject and sender
        self.populate_left_list()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def populate_left_list(self):
        _translate = QtCore.QCoreApplication.translate
        for i in range(len(z)):
            item = QtWidgets.QListWidgetItem()
            item.setText(_translate("Dialog", f"{z[i][0]}\n{z[i][1]}"))
            self.listWidget.addItem(item)

    def on_item_clicked(self, item):
        # Get index of selected item
        index = self.listWidget.row(item)
        
        # Get the corresponding email content
        email_content = y[index]
        
        # Display the email content in the right QListWidget
        self.listWidget_2.clear()
        self.listWidget_2.addItem(email_content)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Email Viewer"))

# Run the application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
