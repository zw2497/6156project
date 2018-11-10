from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


class Autoemail:
    host_server = 'smtp.qq.com'
    sender_qq = '451865085'
    pwd = 'Wzc123871@'
    sender_qq_mail = '451865085@qq.com'
    receiver = 'zw2497@columbia.edu'
    mail_content = 'Hello World'
    mail_title = 'Hello World'

    def __init__(self, receiver, mail_title, mail_content):
        self.receiver = receiver
        self.mail_content = mail_content
        self.mail_title = mail_title

    def send(self):
        smtp = SMTP_SSL(self.host_server)
        smtp.set_debuglevel(0)
        smtp.ehlo(self.host_server)
        smtp.login(self.sender_qq, self.pwd)

        msg = MIMEText(self.mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(self.mail_title, 'utf-8')
        msg["From"] = self.sender_qq_mail
        msg["To"] = self.receiver
        smtp.sendmail(self.sender_qq_mail, self.receiver, msg.as_string())
        smtp.quit()

