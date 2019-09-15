import json
import requests

import launch
from sender.msg_sender import MsgSender


class WxPusher(MsgSender):
    """
    微信推送服务
    接口文档：http://wxpusher.dingliqc.com/#part-1
    支持一对多推送
    支持HTML语法
    """

    def __init__(self):
        pass

    def send_msg(self, to_user=None, title=None, content=None, **kwargs):
        """
        WxPusher发送文本消息
        :param to_user: 接收用户的ID，多个用户ID请用英文半角逗号分隔开。就是关注号，发送给你的那个ID。
        :param title: 标题
        :param content: 内容
        :param kwargs: 消息携带的url，在微信里面点击可以直接打开这个url。为空会自动补充一个消息详情的链接，点击可以在网页中查看消息，方便复制。为了部分强迫症用户，可以传"nourl"，这样就不会携带默认的url。
        :return:
        """
        if to_user is None:
            to_user = launch.config.get_config('ids', 'wx_pusher')
        url = "http://wxmsg.dingliqc.com/send"
        detail_url = kwargs['url'] if 'url' in kwargs else 'nourl'
        querystring = {"title": title, "msg": content, "userIds": to_user, "url": detail_url}
        headers = {
            'User-Agent': "PostmanRuntime/7.16.3",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "96cfdeea-dc0c-491f-9804-7c5a0f5133b5,cd30bd5f-c1f1-4308-82fd-319b3a0997bf",
            'Host': "wxmsg.dingliqc.com",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        result = json.loads(response.text)
        code = result['code']
        msg = result['msg']
        data = result['data']
        if code is not 200:
            print("Wx Pusher Err - code[%s] msg[%s] data[%s]") % (code, msg, data)
            return False
        return True
