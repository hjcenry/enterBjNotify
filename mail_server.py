# -*- coding: utf-8 -*-
__author__ = 'luoqian'

from email.utils import formataddr
from email.mime.text import MIMEText
import smtplib
import mdmail


class MailServer(object):
    """
    邮箱服务器地址端口
    """
    NETEASY_163 = ['smtp.163.com', 25]
    QQ = ['smtp.qq.com', 25]
    GOOGLE = ['smtp.google.com', 25]


class MailSender(object):
    from_addr = ''
    password = ''
    smtp_server = ''
    from_name = ''
    server = None
    from_smtp_server = None

    def __init__(self, from_addr, from_name, from_password, from_smtp_server: MailServer):
        self.from_addr = from_addr
        self.from_name = from_name
        self.password = from_password
        self.smtp_server = from_smtp_server
        try:
            self.from_smtp_server = from_smtp_server
            self.server = smtplib.SMTP(from_smtp_server[0], from_smtp_server[1])
            self.server.set_debuglevel(1)
            self.server.login(from_addr, from_password)
        except smtplib.SMTPException:
            print('Login Error')

    def send_mail(self, to_addr, to_name, subject, content, use_md=False):
        """
        发送邮件
        :param to_addr: 收件人
        :param to_name: 收件名
        :param subject: 标题
        :param content: 内容
        :param use_md: 是否使用markdown语法
        :return:
        """
        if use_md:
            self.send_md_mail(to_addr, subject, content)
        else:
            self.send_text_mail(to_addr, to_name, subject, content)

    def send_text_mail(self, to_addr, to_name, subject, content):
        """
        发送普通邮件
        通过smtplib实现
        :param to_addr: 收件人
        :param to_name: 收件名
        :param subject: 标题
        :param content: 内容
        :return:
        """
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr([self.from_name, self.from_addr])
        msg['To'] = formataddr([to_name, to_addr])
        msg['Subject'] = subject
        try:
            self.server.sendmail(self.from_addr, [to_addr], msg.as_string())
        except smtplib.SMTPException:
            print('Send Error')

        print("发送成功 - [" + to_name + ":" + to_addr + "] - [" + subject + "]:\r\n" + content)

    def send_md_mail(self, to_addr, subject, content, ):
        """
        发送md格式邮件
        使用mdmail实现
        :param to_addr: 收件人
        :param subject: 标题
        :param content: 内容
        :return:
        """
        smtp = {
            'host': self.from_smtp_server[0],
            'port': self.from_smtp_server[1],
            'user': self.from_addr,
            'password': self.password
        }
        mdmail.send(content, subject=subject, from_email=self.from_addr, to_email=to_addr, smtp=smtp)
        print("发送成功 - [" + to_addr + "] - [" + subject + "]:\r\n" + content)
