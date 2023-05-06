# user marko library for parsing markdown files

import os
import re
from pathlib import Path

import marko
from marko import block, inline
from rich import print


class MarkoDocParse:
    def __init__(self, file_path):
        """ Parse markdown file using marko library
        :param file_path: path to markdown file
        """
        self.checked_types = dict()
        self.seen_words = set()
        self.ignore_types = {
            block.BlankLine,  # doesn't have children
            block.HTMLBlock,  # represents comments
            block.ThematicBreak,  # represents lines with ---
            inline.Image,  # does not count as readable words
        }
        self.parse_md_file(file_path)

    def parse_md_file(self, file_path):
        with open(file_path, "r") as f:
            text = f.read()
        self.md_doc = marko.parse(text)

    def count_words(self):
        self.word_count = 0
        self.count_words_recursive(self.md_doc)
        return self.word_count

    def count_words_recursive(self, md_doc):
        for node in md_doc.children:
            if type(node) in self.ignore_types:
                continue

            self.checked_types[type(node)] = 1 + self.checked_types.get(
                type(node), 0
            )
            if isinstance(node.children, str):
                element_words = re.findall(r"\w+", node.children)
                self.seen_words.update(set(element_words))
                self.word_count += len(element_words)
            else:
                self.count_words_recursive(node)


def parse_md_file(file_path):
    res = 0
    dir = Path(file_path)

    for root, _, files in os.walk(dir):
        for file in files:
            if not file.endswith(".md"):
                continue
            file = os.path.join(root, file)
            res += MarkoDocParse(file).count_words()
    return res


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Count words in markdown files"
    )
    parser.add_argument(
        "path",
        metavar="path",
        type=str,
        help="path to directory with markdown files",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(parse_md_file(args.path))
