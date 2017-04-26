from logging import basicConfig, ERROR
from mindbot import MindBot


if __name__ == '__main__':
    basicConfig(
        format='%(levelname)s %(asctime)-15s %(message)s',
        level=ERROR,
    )

    mindbot = MindBot()
    mindbot.run()
