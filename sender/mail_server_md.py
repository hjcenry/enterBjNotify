# -*- coding: utf-8 -*-
import launch
from sender.mail_def import MailServer

__author__ = 'luoqian'

import mdmail

from sender.msg_sender import MsgSender


class MailMdSender(MsgSender):
    from_addr = ''
    password = ''
    smtp_server = None
    server = None

    def __init__(self, from_addr, from_password, from_smtp_server: MailServer):
        self.from_addr = from_addr
        self.password = from_password
        self.smtp_server = from_smtp_server

    def send_msg(self, to_user=None, title=None, content=None, **kwargs):
        """
        发送普通邮件
        :param to_user: 接收人email
        :param title: 标题
        :param content: 内容
        :param kwargs:
        :return:
        """
        smtp = {
            'host': self.smtp_server[0],
            'port': self.smtp_server[1],
            'user': self.from_addr,
            'password': self.password
        }
        if to_user is None:
            to_user = launch.config.get_config('mail_from_addr', 'mail')
        mdmail.send(content, subject=title, from_email=self.from_addr, to_email=to_user, smtp=smtp)
        print("发送成功 - [" + to_user + "] - [" + title + "]:\r\n" + content)
