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
                        
                    # 4. Personalization
                    student_name = recipient.get('name', 'Future Pythonista')
                    personalized_html = html_content.replace('{{NAME}}', student_name)

                    # Create FRESH message for every recipient
                    msg = MIMEMultipart()
                    msg['From'] = self.sender_email
                    msg['Subject'] = final_subject
                    msg.attach(MIMEText(personalized_html, 'html'))
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
            
    def send_welcome_email(self, email, name, password):
        """
        Sends initial credentials to manually added students.
        """
        subject = "🐍 Welcome to PyDaily! Here are your login details."
        
        html_content = f"""
        <div style="font-family: Helvetica, Arial, sans-serif; max-width:600px; margin:0 auto; border:1px solid #e0e0e0; border-radius:10px; overflow:hidden;">
            <div style="background-color:#4F46E5; color:white; padding:20px; text-align:center;">
                <h1 style="margin:0;">Welcome to PyDaily! 🚀</h1>
            </div>
            <div style="padding:30px; color:#333; line-height:1.6;">
                <p>Hi {name},</p>
                <p>You have been enrolled in the <strong>PyDaily Python Cohort</strong>.</p>
                <p>We're excited to help you master Python, one day at a time.</p>
                
                <div style="background-color:#fef3c7; border-left:4px solid #f59e0b; padding:15px; margin:20px 0;">
                    <strong>Your Temporary Credentials:</strong><br>
                    Email: {email}<br>
                    Password: <code>{password}</code>
                </div>
                
                <p>Please log in and start your journey!</p>
                <a href="https://pydaily.streamlit.app/" style="display:inline-block; background-color:#4F46E5; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; font-weight:bold;">Login Now</a>
            </div>
        </div>
        """
        
        # Reuse generic sender logic by wrapping single recipient
        recipient_list = [{'email': email, 'name': name}]
        return self.send_email(recipient_list, subject, html_content)
    @staticmethod
    def format_quiz_for_email(quiz_json):
        """
        Converts Structured JSON Quiz -> Static HTML for Email Fallback.
        """
        import json
        try:
            if isinstance(quiz_json, str):
                data = json.loads(quiz_json)
            else:
                data = quiz_json
                
            questions_html = ""
            for q in data.get('questions', []):
                options_html = ""
                for opt in q.get('options', []):
                    options_html += f'<li style="margin-bottom:5px;">{opt}</li>'
                    
                questions_html += f"""
                <div style="margin-bottom:20px; border:1px solid #eee; padding:15px; border-radius:8px;">
                    <div style="font-weight:bold; margin-bottom:10px;">Q{q.get('id')}: {q.get('question')}</div>
                    <ul style="padding-left:20px; color:#555;">{options_html}</ul>
                    <details style="margin-top:10px; color:#4F46E5; cursor:pointer;">
                        <summary>Reveal Answer</summary>
                        <div style="margin-top:5px; padding:10px; background:#f0f9ff; border-radius:5px;">
                            <strong>Answer: {q.get('answer')}</strong><br>
                            <em>{q.get('explanation')}</em>
                        </div>
                    </details>
                </div>
                """
                
            return f"""
            <div style="font-family: Helvetica, Arial, sans-serif; max-width:600px; margin:0 auto; border:1px solid #e0e0e0; border-radius:10px; overflow:hidden;">
                 <div style="background-color:#4F46E5; color:white; padding:20px; text-align:center;">
                   <h2>🎯 {data.get('title', 'Daily Quiz')}</h2>
                   <p>Test your knowledge below or take the interactive version on the dashboard!</p>
                 </div>
                 
                 <div style="padding:20px; color:#333;">
                    {questions_html}
                    
                    <div style="text-align:center; margin-top:30px;">
                        <a href="https://pydaily.streamlit.app/" style="background-color:#F59E0B; color:white; padding:12px 24px; text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block;">
                           🎮 Take Interactive Quiz & Get Scored
                        </a>
                    </div>
                 </div>
            </div>
            """
        except Exception as e:
            return f"<p>Error formatting quiz: {e}</p>"
