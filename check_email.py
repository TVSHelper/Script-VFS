import re
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup


# https://www.youtube.com/watch?v=ByfMn_zgm5o
def extract_html(text):
    """Extracts HTML content from the given text."""
    match = re.search(r'(<html>.*</html>)', str(text), re.DOTALL)
    return match.group(0) if match else None

def extract_otp(text):
    html_text = extract_html(text)
    """Extracts OTP from the given HTML content."""
    soup = BeautifulSoup(html_text, 'html.parser')
    match = re.search(r'VFS Global is (\d+)', soup.get_text())
    return match.group(1) if match else None

def check_email(email_user, email_pass):
    # Connect to Gmail's IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to the account
    mail.login(email_user, email_pass)

    # Select the mailbox you want to check (inbox)
    mail.select("inbox")

    # Search for all unseen emails
    status, messages = mail.search(None, 'FROM', '"VFS Global "', "UNSEEN")

    # Get the list of email IDs
    email_ids = messages[0].split()

    # Loop through each email ID to fetch the email data
    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # Decode the email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        # Get the email sender
        from_ = msg.get("From")

        try:
            return int(extract_otp(msg))
        except Exception as e:
            print(e)


    # Logout from the account
    mail.logout()

