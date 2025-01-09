import IMAP4_prot
import sendMail
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMenu, QAction, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
os.system('python IMAP4_prot.py')
os.system('python sendMail.py')
y = IMAP4_prot.return_y()

star_list = []  # To hold starred emails
spam_list = []
trash_list = []

class Ui_MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.index = 0
        self.star_status = False
        self.current_email_index = None  # Store the index of the currently selected email

    def setupUi(self, MainWindow):
        self.index = 0
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 625)
        MainWindow.setStyleSheet("background-color: #f0f0f0;")

        # Add the menubar to the MainWindow
        menubar = MainWindow.menuBar()
        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")
        view_menu = menubar.addMenu("View")
        
        # Add actions to File menu
        open_action = QAction("Open", MainWindow)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        quit_action = QAction("Quit", MainWindow)
        quit_action.triggered.connect(MainWindow.close)
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
        
        self.css_on_click = ("QPushButton"
                    "{"
                    f"background-color : lightblue"
                    "}")

        self.css_other = ("QPushButton::hover"
                             "{"
                             "background-color : lightgray;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : lightblue;"
                             "}"
                             )

        # Compose Button
        self.composeButton = QtWidgets.QPushButton("Compose", central_widget)
        self.composeButton.move(0, 0)
        self.composeButton.resize(200, 60)
        self.composeButton.setStyleSheet(self.css_other)
        self.composeButton.clicked.connect(self.compose_box)
        
        # Inbox button
        self.inboxButton = QtWidgets.QPushButton("Inbox", central_widget)
        self.inboxButton.move(0, 60)
        self.inboxButton.resize(200, 60)
        self.inboxButton.clicked.connect(self.inbox_return)
        self.inboxButton.setStyleSheet(self.css_other)
        
        # Starred button
        self.starButton = QtWidgets.QPushButton("Starred", central_widget)
        self.starButton.move(0, 120)
        self.starButton.resize(200, 60)
        self.starButton.clicked.connect(self.show_starred_page)
        self.starButton.setStyleSheet(self.css_other)
        
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
        self.spamButton = QtWidgets.QPushButton("Spam", central_widget)
        self.spamButton.move(0, 480)
        self.spamButton.resize(200, 60)
        self.spamButton.clicked.connect(self.show_spam_page)
        self.spamButton.setStyleSheet(self.css_other)

        # Trash button
        trashButton = QtWidgets.QPushButton("Trash", central_widget)
        trashButton.move(0, 540)
        trashButton.resize(200, 60)
        trashButton.clicked.connect(self.show_trash_page)
        trashButton.setStyleSheet(self.css_other)
        
        self.button_list = [self.inboxButton, 0, self.starButton, self.composeButton, self.spamButton, trashButton, sentButton, draftButton, importantButton, scheduledButton, allButton]

        self.change_highlights(self.index)
        
        # Left QListWidget for subjects and senders
        self.listWidget = QtWidgets.QListWidget(central_widget)
        self.listWidget.setGeometry(QtCore.QRect(200, 0, 100, 100))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemClicked.connect(self.on_item_clicked)
        self.listWidget.resize(800, 600)
        
        # Right QWidget for email content (includes Back button)
        self.emailContentWidget = QtWidgets.QWidget(central_widget)
        self.emailContentWidget.setGeometry(QtCore.QRect(200, 0, 800, 600))
        
        # Layout for email content display
        self.emailContentLayout = QtWidgets.QVBoxLayout(self.emailContentWidget)

        self.listWidget_spam = QtWidgets.QListWidget(central_widget)
        self.listWidget_spam.setGeometry(QtCore.QRect(200, 0, 100, 100))
        self.listWidget_spam.setObjectName("listWidget_spam")
        self.listWidget_spam.itemClicked.connect(self.on_item_clicked_spam)
        self.listWidget_spam.resize(800, 600)
        # QWidget for Starred Email subjects and senders
        self.listWidget_star = QtWidgets.QListWidget(central_widget)
        self.listWidget_star.setGeometry(QtCore.QRect(200, 0, 100, 100))
        self.listWidget_star.setObjectName("listWidget_star")
        self.listWidget_star.itemClicked.connect(self.on_item_clicked_star)
        self.listWidget_star.resize(800, 600)


        self.listWidget_trash = QtWidgets.QListWidget(central_widget)
        self.listWidget_trash.setGeometry(QtCore.QRect(200, 0, 100, 100))
        self.listWidget_trash.setObjectName("listWidget_trash")
        self.listWidget_trash.itemClicked.connect(self.on_item_clicked_trash)
        self.listWidget_trash.resize(800, 600)

        # QWidget for the composition box
        self.composeWidget = QtWidgets.QWidget(central_widget)
        self.composeWidget.setGeometry(QtCore.QRect(220, 0, 760, 580))

        self.composeLayout = QtWidgets.QVBoxLayout(self.composeWidget)
        
        self.composeToLabel = QtWidgets.QLabel("To:", self.composeWidget)
        self.composeToLabel.setGeometry(QtCore.QRect(0,0,50,30))
        
        self.ToCompose = QtWidgets.QLineEdit(self.composeWidget)
        self.ToCompose.setGeometry(QtCore.QRect(75,0,200,30))
        self.ToCompose.setObjectName("subjectCompose")
        
        self.composeSubjectLabel = QtWidgets.QLabel("Subject:", self.composeWidget)
        self.composeSubjectLabel.setGeometry(QtCore.QRect(0,30,50,30))
        
        self.subjectCompose = QtWidgets.QLineEdit(self.composeWidget)
        self.subjectCompose.setGeometry(QtCore.QRect(75,30,200,30))
        self.subjectCompose.setObjectName("subjectCompose")

        self.listWidget_compose = QtWidgets.QTextEdit(self.composeWidget)
        self.listWidget_compose.setGeometry(QtCore.QRect(0, 80, 740, 540))
        self.listWidget_compose.setObjectName("listWidget_Compose")
        self.listWidget_compose.resize(740, 450)

        self.sendButton = QtWidgets.QPushButton("Send", self.composeWidget)
        self.sendButton.clicked.connect(self.send_mail)
        self.sendButton.setVisible(False)
        self.sendButton.setGeometry(QtCore.QRect(300, 550, 100, 30))
        
        # Back Button (hidden initially)
        self.backButton = QtWidgets.QPushButton("Back", self.emailContentWidget)
        self.backButton.clicked.connect(self.show_email_list)
        self.backButton.setVisible(False)  
        self.backButton.move(0,0)
        self.backButton.setIcon(QIcon("images/back_arrow.png"))

        # Starred Button
        self.starredButton = QtWidgets.QPushButton("", self.emailContentWidget)
        self.starredButton.clicked.connect(self.change_star)
        self.starredButton.setVisible(False)
        self.starredButton.move(100, 0)
        self.update_star_icon()


        self.trashButton = QtWidgets.QPushButton("Trash", self.emailContentWidget)
        self.trashButton.clicked.connect(self.trash_email)
        self.trashButton.setVisible(False)
        self.trashButton.move(200,0)


        # Scroll Area for email content
        self.scrollArea = QtWidgets.QScrollArea(self.emailContentWidget)
        self.scrollArea.setWidgetResizable(True)  
        self.scrollArea.setWidget(QtWidgets.QWidget())  
        self.scrollArea.setGeometry(QtCore.QRect(0, 30, 800, 560))  
        
        # Layout for content inside the scroll area
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollArea.widget())
        
        # Label for email subject and sender
        self.subjectLabel = QtWidgets.QLabel(self.scrollArea.widget())
        self.subjectLabel.setWordWrap(True)  
        self.subjectLabel.setAlignment(QtCore.Qt.AlignTop)  
        self.scrollLayout.addWidget(self.subjectLabel)
        
        # Label for email body content
        self.bodyLabel = QtWidgets.QLabel(self.scrollArea.widget())
        self.bodyLabel.setWordWrap(True)  
        self.bodyLabel.setAlignment(QtCore.Qt.AlignTop)  
        self.scrollLayout.addWidget(self.bodyLabel)

        # Stack Lists
        self.stacked_layout = QtWidgets.QStackedLayout()
        self.stacked_layout.addWidget(self.listWidget)
        self.stacked_layout.addWidget(self.emailContentWidget)
        self.stacked_layout.addWidget(self.listWidget_star)
        self.stacked_layout.addWidget(self.composeWidget)
        self.stacked_layout.addWidget(self.listWidget_spam)
        self.stacked_layout.addWidget(self.listWidget_trash)


        # Populate the left list with subject and sender
        self.populate_left_list()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def change_highlights(self, index):
        if index != 1:
            temp_item = self.button_list[index]
            temp_item.setStyleSheet(self.css_on_click)
        else:
            pass
        for i in self.button_list:
            if i != self.button_list[index] and i != self.button_list[1]:
                i.setStyleSheet(self.css_other)


    def change_star(self):
        if self.current_email_index is not None:
            y[self.current_email_index][3] = not y[self.current_email_index][3]  # Toggle star status
            if y[self.current_email_index][3]:
                if y[self.current_email_index] not in star_list:
                    star_list.append(y[self.current_email_index])  # Add to starred list
            else:
                if y[self.current_email_index] in star_list:
                    star_list.remove(y[self.current_email_index])  # Remove from starred list
            self.update_star_icon()
            self.populate_starred_list()  # Update the starred list view

    def update_star_icon(self):
        if self.current_email_index is not None:
            if y[self.current_email_index][3] == True:
                self.starredButton.setIcon(QIcon("images/star_on.png"))
            else:
                self.starredButton.setIcon(QIcon("images/star_off.png"))

    def populate_left_list(self):
        self.listWidget.clear()
        _translate = QtCore.QCoreApplication.translate
        for i in range(len(y)):
            item = QtWidgets.QListWidgetItem()
            if y[i][4] == 0:
                spam_res = "(SPAM RISK)"
            else:
                spam_res = ""
            item.setText(_translate("MainWindow", f"{y[i][0]}         {spam_res}\n{y[i][1]}"))
            self.listWidget.addItem(item)

    def inbox_return(self):
        self.index = 0
        self.stacked_layout.setCurrentIndex(self.index)
        self.change_highlights(self.index)
        self.populate_left_list()
        self.populate_spam_list()
        self.populate_starred_list()
    
    def compose_box(self):
        self.index = 3
        self.stacked_layout.setCurrentIndex(self.index)
        self.change_highlights(self.index)
        self.sendButton.setVisible(True)
    
        
    


    def populate_starred_list(self):
        self.listWidget_star.clear()  # Clear the list before repopulating
        _translate = QtCore.QCoreApplication.translate
    
        # Iterate over starred emails
        for item_data in star_list:
            item = QtWidgets.QListWidgetItem()
            try:
                if item_data[4] == 0:
                    spam_res = "(SPAM RISK)"
                else:
                    spam_res = ""
                item.setText(_translate("MainWindow", f"{item_data[0]}      {spam_res}\n{item_data[1]}"))
            except IndexError:
                item.clear()
            self.listWidget_star.addItem(item)


    def populate_spam_list(self):
        self.listWidget_spam.clear()  # Clear the list before repopulating
        _translate = QtCore.QCoreApplication.translate
    
        # Iterate over starred emails
        for item_data in y:
            item = QtWidgets.QListWidgetItem()
            try:
                if item_data[4] == 0:
                    spam_list.append(item_data)
                    spam_res = "(SPAM RISK)"
                    item.setText(_translate("MainWindow", f"{item_data[0]}      {spam_res}\n{item_data[1]}"))
                else:
                    continue
                
            except IndexError:
                item.clear()
            self.listWidget_spam.addItem(item)
    def populate_trash_list(self):
        self.listWidget_trash.clear()  # Clear the list before repopulating
        _translate = QtCore.QCoreApplication.translate

        # Iterate over the emails in the trash list
        for item_data in trash_list:
            item = QtWidgets.QListWidgetItem()
            try:
                if item_data[4] == 0:  # Assuming item_data[4] indicates spam status
                    spam_res = "(SPAM RISK)"
                else:
                    spam_res = ""
                item.setText(_translate("MainWindow", f"{item_data[0]}      {spam_res}\n{item_data[1]}"))
                self.listWidget_trash.addItem(item)
            except IndexError:
                item.clear()
                self.listWidget_trash.addItem(item)

    

    def show_starred_page(self):
        self.index = 2
        self.populate_starred_list()
        self.stacked_layout.setCurrentIndex(self.index)  # Switch to the Starred List
        self.change_highlights(self.index)
        self.populate_left_list()
        self.populate_spam_list()
        self.populate_starred_list()
    
    def show_spam_page(self):
        self.index = 4
        self.populate_spam_list()
        self.stacked_layout.setCurrentIndex(self.index)
        self.change_highlights(self.index)

    def show_trash_page(self):
        self.index = 5
        self.populate_trash_list()  # Populate the trash list
        self.stacked_layout.setCurrentIndex(self.index)  # Switch to the Trash List view
        self.change_highlights(self.index)  # Change the highlight for the trash button



    def on_item_clicked(self, item):
        index11 = self.listWidget.row(item)  
        self.current_email_index = index11  
        subject, sender, email_content, star_stats, spam_stats = y[index11]
        if spam_stats == 0:
            spam_res = "(SPAM RISK)"
        else:
            spam_res = ""
        self.update_star_icon()
        self.subjectLabel.setText(f"Subject: {subject}     {spam_res}")
        self.bodyLabel.setText(f"From: {sender}\n\n{email_content}")
        
        
        self.backButton.setVisible(True)
        self.starredButton.setVisible(True)
        self.trashButton.setVisible(True)

        self.stacked_layout.setCurrentIndex(1)

    


    def on_item_clicked_star(self, item):
        # Get the index from the starred list (listWidget_star)
        index_starred = self.listWidget_star.row(item)
        self.current_email_index = y.index(star_list[index_starred])  # Get the original index of the starred email

        subject, sender, email_content, star_statsm, spam_stats = y[self.current_email_index]

        self.update_star_icon()
        self.subjectLabel.setText(f"Subject: {subject}")
        self.bodyLabel.setText(f"From: {sender}\n\n{email_content}")
        
        
        self.backButton.setVisible(True)
        self.starredButton.setVisible(True)
        self.trashButton.setVisible(True)

        self.stacked_layout.setCurrentIndex(1)
    def on_item_clicked_spam(self, item):
        # Get the index from the starred list (listWidget_star)
        index_spam = self.listWidget_spam.row(item)
        self.current_email_index = y.index(spam_list[index_spam])  # Get the original index of the starred email

        subject, sender, email_content, star_statsm, spam_stats = y[self.current_email_index]

        self.update_star_icon()
        self.subjectLabel.setText(f"Subject: {subject}")
        self.bodyLabel.setText(f"From: {sender}\n\n{email_content}")
        
        
        self.backButton.setVisible(True)
        self.starredButton.setVisible(True)

        self.stacked_layout.setCurrentIndex(1)
    def on_item_clicked_trash(self, item):
        # Get the index from the starred list (listWidget_star)
        index_trash = self.listWidget_trash.row(item)
          # Get the original index of the starred email

        subject, sender, email_content, star_statsm, spam_stats = trash_list[index_trash]

        self.update_star_icon()
        self.subjectLabel.setText(f"Subject: {subject}")
        self.bodyLabel.setText(f"From: {sender}\n\n{email_content}")
        
        
        self.backButton.setVisible(True)
        self.starredButton.setVisible(True)

        self.stacked_layout.setCurrentIndex(1)
    
    def send_mail(self):
        sendTo = self.ToCompose.text()
        sendSubject = self.subjectCompose.text()
        sendContent = self.listWidget_compose.toPlainText()


        message = f"""\
        Subject: {sendSubject}

        {sendContent}"""
        sendMail.sendEmail(sendTo, message)

        self.ToCompose.clear()
        self.subjectCompose.clear()
        self.listWidget_compose.clear()

    def trash_email(self):
        # First, mark the email as trashed and remove it from star/spam lists
        email = y[self.current_email_index]
        if email not in trash_list:
            trash_list.append(email)
            if email in star_list:
                star_list.remove(email)
            if email in spam_list:
                spam_list.remove(email)
        
            # Remove the email from y (the main email list)
            y.pop(self.current_email_index)
    
        # Debug print to verify lists are updated
        print("Emails in 'y':", y)
        print("Starred emails:", star_list)
        print("Trash emails:", trash_list)

        # Now, populate the trash list
        self.populate_trash_list()


    def show_email_list(self):
        self.backButton.setVisible(False)
        self.stacked_layout.setCurrentIndex(self.index)
        self.starredButton.setVisible(False)
        self.change_highlights(self.index)
        self.populate_left_list()
        self.populate_starred_list()
        self.populate_spam_list

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

# Run the application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()  
    ui = Ui_MainWindow()  
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())