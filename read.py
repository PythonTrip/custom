import pandas as pd
from os import walk


def to_float(data):
    return float(data.replace(',', '.'))


class Reader:
    def __init__(self):
        self.data = []
        self.directs = []

    def clear(self):
        self.data = []

    @staticmethod
    def walk_for_dir(direct) -> str:
        for (dir_path, _, filenames) in walk(direct):
            for filename in filenames:
                yield dir_path, filename

    @staticmethod
    def read_from_dir(direct, skip=2):
        for (dir_path, _, filenames) in walk(direct):
            for file in filenames:
                with open(dir_path + "\\" + file) as txt:
                    yield file, "".join(txt.readlines()[skip:])

    @staticmethod
    def file2txt(file):
        with open(file, encoding="utf-8") as txt:
            text = txt.read()
        return text

    @staticmethod
    def file2lines(file, skip=0):
        with open(file, encoding="utf-8") as txt:
            lines = txt.readlines()[skip:]
        return lines

    @staticmethod
    def create_table(data, cols, index=None, sort_index=None, sep="\s+"):
        if index is None:
            index = []
        for df in data:
            table = pd.read_csv(df, sep=sep, index_col=index, names=cols)
            if not sort_index is None:
                table = table.sort_values(sort_index)
            yield table
