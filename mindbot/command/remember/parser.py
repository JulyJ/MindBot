from re import compile as re_compile
from typing import List


def parse_tags(text) -> List[str]:
    tags_finder = re_compile(r'#[^\s]+')
    return tags_finder.findall(text)
