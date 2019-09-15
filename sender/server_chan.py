import json
import requests

import launch
from sender.msg_sender import MsgSender


class ServerChan(MsgSender):
    """
    Server酱推送服务
    接口文档：http://sc.ftqq.com/3.version
    仅支持一对一推送
    支持markdown语法
    """

    def __init__(self):
        pass

    def send_msg(self, to_user=None, title=None, content=None, **kwargs):
        """
        Server酱发送文本消息
        :param to_user:
        :param title:
        :param content:
        :param kwargs:
        :return:
        """
        if to_user is None:
            to_user = launch.config.get_config('server_chan_key', 'server_chan')
        for sc_key in to_user.split(','):
            if sc_key is '' or sc_key is None:
                continue
            url = "https://sc.ftqq.com/%s.send" % sc_key
            querystring = {"text": title}
            if content is not None:
                querystring["desp"] = content
            response = requests.request("GET", url, params=querystring)
            try:
                result = json.loads(response.text)
                errno = result['errno']
                if errno is not 0:
                    print("Server Chan Err - response[%s]" % response.text)
            except json.decoder.JSONDecodeError:
                print("Server Chan Decode Err - response[%s]" % response.text)
            except KeyError:
                print("Server Chan KeyError - response[%s]" % response.text)
        return True
