from datetime import datetime

from re import compile as re_compile

class Parser:
    "Parsing tools class."
    @staticmethod
    def parse_tags(text):
        """This method find #tags in messages."""
        myre = re_compile(r"#[^\s]+")
        tags = myre.findall(text)
        print("parsed tags:", tags)
        return "".join(tags)

    @staticmethod
    def message_type_parser(text):
        """This identifies user request (Remember information, Google, Wiki, translate etc."""
        print("message type parsing...")
        command = text.split(" ")[0]
        return command

    @staticmethod
    def date_conversion(date):
        """This method convert unixtime date to human-readable format"""
        return datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')
