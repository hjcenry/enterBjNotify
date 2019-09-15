from jjz_interface import JjzInterface
import sys
import datetime

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("params err")
        exit(1)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print("执行时间：%s" % now_time)
    jjz = JjzInterface()
    only_can_apply = True if int(sys.argv[1]) == 1 else False
    send_mail = True if int(sys.argv[2]) == 1 else False
    send_server_chan = True if int(sys.argv[3]) == 1 else False
    jjz.get_apply_status(only_can_apply=only_can_apply, send_mail=send_mail, send_server_chan=send_server_chan)
