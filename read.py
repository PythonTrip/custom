import pandas as pd
from os import walk


def to_float(data):
    return float(data.replace(',', '.'))


class Data:
    def __init__(self):
        self.data = []
        self.directs = []

    def clear(self):
        self.data = []

    @staticmethod
    def read_from_dir(direct, skip=2):
        for (dir_path, _, filenames) in walk(direct):
            for file in filenames:
                with open(dir_path + "\\" + file) as txt:
                    yield file, "".join(txt.readlines()[skip:])

    @staticmethod
    def read_from_data(data):
        for txt in data:
            yield "".join(txt)

    @staticmethod
    def lines_read(file, skip=2):
        with open(file) as txt:
            lines = txt.readlines()[skip:]
            txt.close()
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
