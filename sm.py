import smtplib, ssl

port = 465  # For SSL
#password = input("Type your password and press enter: ")

email = "jadhav.chinmay.17ee5016@gmail.com"
password = 'anu@85186'

sender_email = "jadhav.chinmay.17ee5016@gmail.com"
receiver_email = "cjadhav132@gmail.com"
message =""" some""" + " Thing In Subject" + "\n\n" + "Is this in subject"


# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)