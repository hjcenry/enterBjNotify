import jjz_tool as JjzTool
from mail_server import *
from server_chan import *
import datetime
from config import *


class JjzInterface(object):
    data = None
    # 是否可申请状态
    can_apply = False
    # 是否可申请状态文本
    can_apply_text = None
    # 车牌号
    license_no = None
    # 进京证数据
    car_apply_arr = None
    # 进京证数量
    apply_size = None
    # 邮箱
    mail_sender = None
    mail_from_addr = None
    mail_name = "进京证"
    mail_pwd = None
    mail_server = None
    # Server酱
    server_chan = None
    server_chan_key = None
    # config
    config = Config('config.ini')

    def __init__(self):
        self.read_config()
        apply_status = JjzTool.query_apply_status()
        print(apply_status)
        self.data = apply_status['datalist'][0]
        self.can_apply = True if self.data['applyflag'] == '1' else False
        self.can_apply_text = '可申请' if self.can_apply else '已申请'
        self.license_no = self.data['licenseno']
        self.car_apply_arr = self.data['carapplyarr']
        self.apply_size = len(self.car_apply_arr)
        self.mail_sender = MailSender(self.mail_from_addr, self.mail_name, self.mail_pwd, self.mail_server)
        self.server_chan = ServerChan(self.server_chan_key)

    def read_config(self):
        self.mail_from_addr = JjzInterface.config.get_config('mail_from_addr', 'mail')
        self.mail_pwd = JjzInterface.config.get_config('mail_pwd', 'mail')
        self.mail_server = eval(JjzInterface.config.get_config('mail_server', 'mail'))
        self.server_chan_key = JjzInterface.config.get_config('server_chan_key', 'server_chan')

    def get_apply_status(self, only_can_apply=False, send_mail=False, send_server_chan=False):
        if not self.can_apply and only_can_apply:
            return
        status_text_color = "#FF0000" if self.can_apply else "#00FF00"
        notify_string = "### 当前进京证状态为:<font color='%s'>%s</font>\n" % (status_text_color, self.can_apply_text)
        notify_string += "- 车牌号:%s\n" % self.license_no
        notify_string += "- 当前进京证数量:%d\n" % self.apply_size
        now_time = datetime.datetime.now()
        for car_apply in self.car_apply_arr:
            enter_bj_start = car_apply['enterbjstart']
            enter_bj_end = car_apply['enterbjend']
            notify_string += "\t- 进京证日期:%s ~ %s\n" % (enter_bj_start, enter_bj_end)
            notify_string += "\t- 今日日期:%s\n" % now_time.strftime('%Y-%m-%d')
            enter_bj_end_arr = enter_bj_end.split('-')
            end_date_time = datetime.datetime(int(enter_bj_end_arr[0]), int(enter_bj_end_arr[1]),
                                              int(enter_bj_end_arr[2]))
            days = (end_date_time - now_time).days + 1
            days_color = '#FF0000' if days <= 2 else "#00FF00"
            notify_string += "\t- 距离到期天数:<font color='%s'>%d</font>\n" % (days_color, days)
            notify_string += "\n"
            notify_string += "---"

        title = "快去办进京证了！" if self.can_apply else "进京证状态"
        if send_mail:
            self.mail_sender.send_mail(to_addr=self.mail_from_addr, to_name="进京证", subject=title, content=notify_string,
                                       use_md=True)
        if send_server_chan:
            self.server_chan.send_text(text=title, desp=notify_string)
