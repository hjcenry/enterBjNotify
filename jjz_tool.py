import requests
import jjz_interface
import json


def query_apply_status():
    url = "https://enterbj.zhongchebaolian.com/enterbj/platform/enterbj/entercarlist"
    config = jjz_interface.JjzInterface.config
    payload = "userid=%s" % config.get_config('userid', 'jjz')
    payload += "&appkey=%s" % config.get_config('appkey', 'jjz')
    payload += "&deviceid=%s" % config.get_config('deviceid', 'jjz')
    payload += "&timestamp=%s" % config.get_config('timestamp', 'jjz')
    payload += "&token=%s" % config.get_config('token', 'jjz')
    payload += "&sign=%s" % config.get_config('sign', 'jjz')
    payload += "&platform=%s" % config.get_config('platform', 'jjz')
    payload += "&appsource=%s" % config.get_config('appsource', 'jjz')
    headers = {
        'Host': "enterbj.zhongchebaolian.com",
        'Accept': "*/*",
        'X-Requested-With': "XMLHttpRequest",
        'Accept-Encoding': "br, gzip, deflate",
        'Accept-Language': "zh-cn",
        'Content-Type': "application/x-www-form-urlencoded",
        'Origin': "https://enterbj.zhongchebaolian.com",
        'Content-Length': "165",
        'Connection': "keep-alive",
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        'Referer': "https://enterbj.zhongchebaolian.com/enterbj/jsp/enterbj/index.html",
        'Cookie': config.get_config('cookie', 'jjz'),
        'Cache-Control': "no-cache",
        'Postman-Token': "df677cd5-e35c-401a-96aa-1809cfdd33ab,65137646-7dcb-48de-9d91-00592e031b0d",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    try:
        return json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
        print('json解析失败，返回内容:[%s] %s' % response.text, e.msg)
