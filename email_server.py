from flask import Flask, request, jsonify
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Gmail SMTP settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("GMAIL_USER")  # Set in .env file
SMTP_PASSWORD = os.getenv("GMAIL_PASSWORD")  # Use an App Password

@app.route("/api/send-email", methods=["POST"])
def send_email():
    data = request.json
    recipient_email = data.get("recipient_email")
    recipient_name = data.get("recipient_name", "Customer")

    if not recipient_email:
        return jsonify({"error": "Recipient email is required"}), 400

    try:
        # Create email
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = recipient_email
        msg["Subject"] = "Access Wajud FZCO's Pricing & Catalog"

        # Email body
        body = f"""
        Hi {recipient_name},

        Thank you for your interest in Wajud FZCO.  
        You can access our **pricing and catalog** by logging into our portal:

        🔗 **[www.wajudportal.com](https://www.wajudportal.com)**

        If you have any questions, feel free to reach out.

        Best Regards,  
        **Wajud FZCO Team**
        """

        msg.attach(MIMEText(body, "plain"))

        # Send email via Gmail SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, recipient_email, msg.as_string())
        server.quit()

        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)