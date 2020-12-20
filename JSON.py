import json


class JSON_Data:
    def __init__(self):
        pass

    @staticmethod
    def dump(data):
        return json.dumps(data, sort_keys=False, ensure_ascii=False, indent=None).encode("utf-8")

    @staticmethod
    def read(data):
        return json.loads(data.decode("utf-8"))

    @staticmethod
    def dump_file(data, file_name):
        with open(file_name, 'w') as fopen:
            return json.dump(data, fopen, sort_keys=False, ensure_ascii=False, indent=4)

    @staticmethod
    def read_file(file_name):
        with open(file_name, 'r') as fopen:
            return json.load(fopen)
