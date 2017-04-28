from logging import basicConfig, DEBUG
from mindbot import MindBot


if __name__ == '__main__':
    basicConfig(
        format='%(levelname)s %(asctime)-15s %(message)s',
        level=DEBUG,
    )

    mindbot = MindBot()
    mindbot.run()
