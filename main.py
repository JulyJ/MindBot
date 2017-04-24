from time import sleep

import msglistener


def main():
    """Let's run this bot while true!"""
    reader = msglistener.MsgListener()
    last_update_id = None
    while True:
        updates = reader.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = reader.get_last_update_id(updates) + 1
            print(updates)
            reader.parse_message(updates)
        sleep(1)

if __name__ == '__main__':
    main()
