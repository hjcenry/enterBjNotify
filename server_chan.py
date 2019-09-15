import json


class ServerChan(object):
    # Server酱秘钥
    sc_key = None

    def __init__(self, sc_key):
        self.sc_key = sc_key

    def send_text(self, text, desp):
        '''
        Server酱发送文本消息
        :param text:
        :param desp:
        :return:
        '''
        import requests
        url = "https://sc.ftqq.com/%s.send" % self.sc_key
        querystring = {"text": text}
        if desp is not None:
            querystring["desp"] = desp
        response = requests.request("GET", url, params=querystring)
        result = json.loads(response.text)
        errno = result['errno']
        errmsg = result['errmsg']
        dataset = result['dataset']
        if errno is not 0:
            print("Server Chan Err - errno[%s] errmsg[%s] dataset[%s]") % (errno, errmsg, dataset)
            return False
        return True
