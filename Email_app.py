# -*- coding: utf-8 -*- 

import imaplib, email
import os
from email.header import decode_header
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMenu, QAction, QMainWindow

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

# Fetch emails and store details
for i in range(numOfMessages, numOfMessages - 100, -1):
    try:
        res, msg = imap.fetch(str(i), "(RFC822)")  # Fetch the email using its ID
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, From = obtain_header(msg)

                var_x = None  # Initialize var_x to None

                # Check if the email is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        # Extract body content
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            body = None  # Handle case if decoding fails

                        # If the part is plain text and not an attachment
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            var_x = body
                        elif "attachment" in content_disposition:
                            download_attachment(part)

                else:
                    # If email is not multipart, extract the body directly
                    content_type = msg.get_content_type()
                    try:
                        body = msg.get_payload(decode=True).decode()
                    except:
                        body = None  # Handle case if decoding fails
                    if content_type == "text/plain":
                        var_x = body

                if var_x:
                    y.append((subject, From, var_x))  # Store subject, sender, and body as a tuple
    except TypeError:
        pass
imap.close()

# PyQt5 GUI
class Ui_MainWindow(QMainWindow):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 625)

        MainWindow.setStyleSheet("background-color: #f0f0f0;")

        # Add the menubar to the MainWindow
        menubar = MainWindow.menuBar()  # Create a menu bar
        file_menu = menubar.addMenu("File")  # Create "File" menu
        edit_menu = menubar.addMenu("Edit")  # Create "Edit" menu
        view_menu = menubar.addMenu("View")  # Create "View" menu
        
        # Add actions to File menu
        open_action = QAction("Open", MainWindow)
        file_menu.addAction(open_action)
        file_menu.addSeparator()  # Add a separator
        quit_action = QAction("Quit", MainWindow)
        quit_action.triggered.connect(MainWindow.close)  # Connect quit action to close the dialog
        file_menu.addAction(quit_action)

        # Add actions to Edit menu
        cut_action = QAction("Cut", MainWindow)
        edit_menu.addAction(cut_action)
        copy_action = QAction("Copy", MainWindow)
        edit_menu.addAction(copy_action)
        paste_action = QAction("Paste", MainWindow)
        edit_menu.addAction(paste_action)

        # Add actions to View menu
        full_screen_action = QAction("Full Screen", MainWindow)
        view_menu.addAction(full_screen_action)
        full_screen_action.triggered.connect(MainWindow.showMaximized)

        # Set up the central widget layout for displaying the email list and content
        central_widget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(central_widget)
        
        # Inbox button
        inboxButton = QtWidgets.QPushButton("Inbox", central_widget)
        inboxButton.move(0, 0)
        inboxButton.resize(200, 60)

        # Starred button
        starButton = QtWidgets.QPushButton("Starred", central_widget)
        starButton.move(0, 60)
        starButton.resize(200, 60)

        # Snoozed button
        snoozedButton = QtWidgets.QPushButton("Snoozed", central_widget)
        snoozedButton.move(0, 120)
        snoozedButton.resize(200, 60)

        # Sent button
        sentButton = QtWidgets.QPushButton("Sent", central_widget)
        sentButton.move(0, 180)
        sentButton.resize(200, 60)

        # Drafts button
        draftButton = QtWidgets.QPushButton("Drafts", central_widget)
        draftButton.move(0, 240)
        draftButton.resize(200, 60)

        # Important button
        importantButton = QtWidgets.QPushButton("Important", central_widget)
        importantButton.move(0, 300)
        importantButton.resize(200, 60)

        # Scheduled button
        scheduledButton = QtWidgets.QPushButton("Scheduled", central_widget)
        scheduledButton.move(0, 360)
        scheduledButton.resize(200, 60)

        # All Mail button
        allButton = QtWidgets.QPushButton("All Mail", central_widget)
        allButton.move(0, 420)
        allButton.resize(200, 60)

        # Spam button
        spamButton = QtWidgets.QPushButton("Spam", central_widget)
        spamButton.move(0, 480)
        spamButton.resize(200, 60)

        # Trash button
        trashButton = QtWidgets.QPushButton("Trash", central_widget)
        trashButton.move(0, 540)
        trashButton.resize(200, 60)

        # Left QListWidget for subjects and senders
        self.listWidget = QtWidgets.QListWidget(central_widget)
        self.listWidget.setGeometry(QtCore.QRect(200, 0, 100, 100))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemClicked.connect(self.on_item_clicked)
        self.listWidget.resize(800, 600)
        
        # Right QListWidget for email content
        self.listWidget_2 = QtWidgets.QListWidget(central_widget)
        self.listWidget_2.setGeometry(QtCore.QRect(200, 0, 100, 100))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.resize(800, 600)

        # Stack Lists
        self.stacked_layout = QtWidgets.QStackedLayout()
        self.stacked_layout.addWidget(self.listWidget)
        self.stacked_layout.addWidget(self.listWidget_2)

        # Populate the left list with subject and sender
        self.populate_left_list()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def populate_left_list(self):
        _translate = QtCore.QCoreApplication.translate
        for i in range(len(z)):
            item = QtWidgets.QListWidgetItem()
            item.setText(_translate("MainWindow", f"{z[i][0]}\n{z[i][1]}"))
            self.listWidget.addItem(item)

    def on_item_clicked(self, item):
        # Get index of selected item
        index = self.listWidget.row(item)  # Changed to self.listWidget.row() to match clicked item

        # Get the corresponding email content (subject, sender, body)
        subject, sender, email_content = y[index-1]

        # Display the email content in the right QListWidget
        self.listWidget_2.clear()
        self.listWidget_2.addItem(f"Subject: {subject}")
        self.listWidget_2.addItem(f"From: {sender}")
        self.listWidget_2.addItem(f"\n{email_content}")  # Display the body content
        self.stacked_layout.setCurrentIndex(1)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Email Viewer"))

# Run the application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()  # Use QMainWindow instead of QDialog
    ui = Ui_MainWindow()  # Use Ui_MainWindow
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())