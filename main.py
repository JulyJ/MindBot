import time


import mindbot

def main():
    reader = mindbot.MsgEcho()
    last_update_id = None
    while True:
        updates = reader.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = reader.get_last_update_id(updates) + 1
            reader.echo_all(updates)
            reader.remember_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()