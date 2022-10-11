import smtplib, ssl


class Mail:
    def __init__(self):
        self.port = 465  # For SSL
        self.sender_email = ""
        self.password = "Password"
        self.context = ssl.create_default_context()


    def send(self,receiver_email,msg):
        message = """\
        Smart Receptionist Message


""" + msg
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message)



if __name__ == "__main__":
    a = Mail()