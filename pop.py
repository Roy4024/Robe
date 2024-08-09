import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient_email, subject, body, sender_email, sender_password):
    # Create the email headers and message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the body text to the email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the email server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(sender_email, sender_password)

        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)

        # Close the connection to the server
        server.quit()

        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def send_email_every_30_seconds():
    # Define email details
    recipient_email = "dinoroye24@gmail.com"  # Replace with the recipient's email address
    sender_email = "subbharoyendinesh@gmail.com"  # Replace with your email address
    sender_password = "Sunshine986999;"  # Replace with your email password
    subject = "Scheduled Email"
    body = "This is an automated email sent every 30 seconds."

    while True:
        send_email(recipient_email, subject, body, sender_email, sender_password)
        time.sleep(30)  # Wait for 30 seconds

# Run the function
send_email_every_30_seconds()
