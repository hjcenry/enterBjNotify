# -*- coding: utf-8 -*-
import launch

__author__ = 'luoqian'

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from sender.msg_sender import MsgSender
from sender.mail_def import MailServer


class MailSmtpSender(MsgSender):
    from_addr = ''
    password = ''
    from_name = ''
    server = None

    def __init__(self, from_addr, from_name, from_password, from_smtp_server: MailServer):
        self.from_addr = from_addr
        self.from_name = from_name
        self.password = from_password
        try:
            self.server = smtplib.SMTP(from_smtp_server[0], from_smtp_server[1])
            self.server.set_debuglevel(1)
            self.server.login(from_addr, from_password)
        except smtplib.SMTPException:
            print('Login Error')

    def send_msg(self, to_user=None, title=None, content=None, **kwargs):
        """
        发送普通邮件
        :param to_user: 接收人
        :param title: 标题
        :param content: 内容
        :param kwargs:
        :return:
        """
        """
        Schema of to_user dict:
        name (str): user name
        addr (str): mail address
        """
        if to_user is None:
            to_user = {
                'name': self.from_name,
                'addr': launch.config.get_config('mail_from_addr', 'mail')
            }
        to_name = to_user['name']
        to_addr = to_user['addr']
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr([self.from_name, self.from_addr])
        msg['To'] = formataddr([to_name, to_addr])
        msg['Subject'] = title
        try:
            self.server.sendmail(self.from_addr, [to_addr], msg.as_string())
        except smtplib.SMTPException:
            print('Send Error')

        print("发送成功 - [" + to_name + ":" + to_addr + "] - [" + title + "]:\r\n" + content)

    def quit(self):
        self.server.quit()
