#coding=utf-8
__author__ = 'Administrator'

import smtplib
from email.mime.text import MIMEText


def mail(to_mail, mail_msg):
    user = "raspcloud@126.com"
    pwd = "@raspcloud"

    msg = MIMEText(mail_msg, _subtype='plain', _charset='utf8')
    msg["Subject"] = "RaspCloud意见建议"
    msg["From"] = user
    msg["To"] = to_mail

    s = smtplib.SMTP("smtp.126.com")
    s.login(user, pwd)
    s.sendmail(user, to_mail, msg.as_string())
    s.close()