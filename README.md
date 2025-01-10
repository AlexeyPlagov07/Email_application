# Email Application
This applciation allows users to access their email as you would be able to do so with GMAIL and other platforms. Features include starring/liking emails, reading inbox,
trashing and archiving emails, detecting spam emails using ML model, and sending out emails.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Installation
1. Clone the repository:
```bash
 git clone https://github.com/AlexeyPlagov07/Email_application.git
```

2. Install dependencies:
```bash
 "YOUR DIRECTORY"/file_down.bat
 ```

## Usage
To run the project, use the following command once:
```bash
python IMAP4_prot.py
python spam_detect.py
python sendMail.py
```
Then to run the actual window, run:
```bash
python Email_app.py
```

## Adjusting to the User
### When using the software, you are able to use your gmail account after a few steps
1.) Go to your gmail settings and click "see all settings"
2.) Go to Forwarding and POP/IMAP
3.) Make sure IMAP is enabled
4.) Then in your gmail account, go to Security
5.) Enable Two-Step Verification
6.) Click App Passwords and create new app called Python Email Reader (doesn't have to be exact)
7.) Copy the temporary code given to you and paste it into the IMAP4_prot.py and sendMail.py files in the PASS HERE area

### Email Amount
Depends on how many emails you want, you can change "5" in the line:
```Python
last_50_email_ids = email_ids[-5:]
```
to the number of emails you want to appear in the UI

## Edits
If there are any issues in the code, please let me know in the Issues section of thre repo or create a branch and make edits as needed. Thank you!! :)
