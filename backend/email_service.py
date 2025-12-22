import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

class EmailService:
    def __init__(self, sender_email, sender_password, test_mode=False, admin_email=""):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.test_mode = test_mode
        self.admin_email = admin_email
        self.smtp_server = "smtp.gmail.com" # Default to Gmail for now, customizable later
        self.smtp_port = 587

    def send_email(self, recipient_list, subject, html_content):
        if not self.sender_email or not self.sender_password:
             return False, "Credentials missing"

        try:
            # 1. Connect & Login
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            # 2. Iterate and Send
            failed = []
            for recipient in recipient_list:
                try:
                    # SANDBOX LOGIC
                    target_email = recipient['email']
                    final_subject = subject

                    if self.test_mode:
                        if not self.admin_email:
                            print(f"⚠️ Test Mode ON but no Admin Email set! Skipping {target_email}")
                            continue
                        print(f"🧪 [TEST MODE] Redirecting {target_email} -> {self.admin_email}")
                        target_email = self.admin_email
                        final_subject = f"[TEST MODE] {subject}"

                    # Create FRESH message for every recipient
                    msg = MIMEMultipart()
                    msg['From'] = self.sender_email
                    msg['Subject'] = final_subject
                    msg.attach(MIMEText(html_content, 'html'))
                    msg['To'] = target_email
                    
                    server.send_message(msg)
                    print(f"✅ Sent email to {target_email}")
                    
                except Exception as e:
                    print(f"❌ Failed to send to {target_email}: {e}")
                    failed.append(f"{target_email}: {str(e)}")

            # 3. Quit
            server.quit()
            
            if failed:
                return False, f"Partial failure: {', '.join(failed)}"
            return True, "Emails sent successfully!"

        except Exception as e:
            return False, str(e)

    def test_connection(self):
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.quit()
            return True, "Connection Successful"
        except Exception as e:
            return False, str(e)
