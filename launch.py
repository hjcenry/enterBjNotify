import datetime
import sys

from config import Config
import jjz_interface

config = Config('config.ini')

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("params err")
        exit(1)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print("执行时间：%s" % now_time)
    jjz = jjz_interface.JjzInterface()
    only_can_apply = True if int(sys.argv[1]) == 1 else False
    sender_types = []
    for index in range(len(sys.argv)):
        if index <= 1:
            continue
        sender_types.append(sys.argv[index])
    jjz.get_apply_status(only_can_apply=only_can_apply, sender_types=sender_types)
