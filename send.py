import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass
import time

# Input your email credentials
sender_email = 'sponsorship@harvardchina.org'
password = getpass('Enter your email password: ')

# Read email addresses from a CSV file
csv_file = 'email_list.csv'
reader = csv.DictReader(open(csv_file))
email_list = []
first_name = []
company_name = []
language = []
for row in reader:
    email_list.append(row['Email Address'])
    first_name.append(row['Name'])
    company_name.append(row['Company'])
    language.append(row['Language'])


# Read the HTML message from a file
html_message_english = open('message_english.html').read()
html_message_simplified = open('message_simplified.html').read()
html_message_traditional = open('message_traditional.html').read()

# Compose and send the email
subject = 'Harvard College China Forum Potentail Partnership'

for i, recipient in enumerate(email_list):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        
        # Check for language
        if(language[i] == 'English'):
            customized_message = html_message_english.format(name=first_name[i], company=company_name[i])
        elif(language[i] == 'Simplified'):
            customized_message = html_message_simplified.format(name=first_name[i], company=company_name[i])
        elif(language[i] == 'Traditional'):
            customized_message = html_message_traditional.format(name=first_name[i], company=company_name[i])

        msg.attach(MIMEText(customized_message, 'html'))
        server.sendmail(sender_email, recipient, msg.as_string())
        print(f"Email sent to {recipient}")
        
        # Disconnect from the server
        server.quit()

        time.sleep(2)
    except Exception as e:
        print(f"Failed to send email to {recipient}: {str(e)}")
