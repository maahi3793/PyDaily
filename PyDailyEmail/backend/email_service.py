import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

class EmailService:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com" # Default to Gmail for now, customizable later
        self.smtp_port = 587

    def send_email(self, recipient_list, subject, html_content):
        if not self.sender_email or not self.sender_password:
             return False, "Credentials missing"

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            # Send to all (BCC recommended for privacy, but individual is better for personalization. 
            # For simplicity, we loop here or send as BCC. Looping is safer to avoid spam flags on BCC).
            
            failed = []
            for recipient in recipient_list:
                try:
                    # Create unique header for each to avoid "undisclosed recipients" issues if treating individually
                    # But simpler:
                    del msg['To']
                    msg['To'] = recipient['email']
                    server.sendmail(self.sender_email, recipient['email'], msg.as_string())
                except Exception as e:
                    failed.append(f"{recipient['email']}: {str(e)}")

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
