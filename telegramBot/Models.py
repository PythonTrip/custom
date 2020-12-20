from matplotlib import pyplot as plt
from numpy import *
from custom import JSON


def clear():
    JSON.dump_file([], "QA.json")


class FunctionsHandle:
    def __init__(self):
        self.x = None
        self.y = None

    def create_func(self, f: str, x0: str, x1: str, epsilon):
        x = arange(float(x0), float(x1) + epsilon, epsilon)
        f = f.replace("^", "**")
        for i, c in enumerate(f):
            if c == "x" and not f[i - 1] in ['*', "/", "+", "-", "(", ")"] and i > 0:
                f = f[0:i] + "*" + f[i:len(f)]
        y = eval(f"{f}")
        self.x = x[~isnan(y)]
        self.y = y[~isnan(y)]
        del x, y

    def create_plot(self):
        if self.x is None or self.y is None: return False
        plt.plot(self.x, self.y)
        plt.savefig('pic.png')
        plt.close()
        return True


class NLP:
    @staticmethod
    def set_question(text, id):
        dialogs = JSON.read_file("QA.json")
        new_dialog = {"id": id, "q": text, "a": ""}
        elements = [[i, x] for i, x in enumerate(dialogs) if x['id'] == id and x['a'] == ""]
        if len(elements) > 0:
            dialogs.pop(elements[0][0])
        dialogs.append(new_dialog)
        dialogs.sort(key=lambda k: (k['id'], k['a']))
        JSON.dump_file(dialogs, "QA.json")

    @staticmethod
    def set_answer(text, id):
        dialogs = JSON.read_file("QA.json")
        elements = [[i, x] for i, x in enumerate(dialogs) if x['id'] == id and x['a'] == ""]
        if len(elements) == 0:
            return False
        i, x = elements[0]
        dialogs[i]['a'] = text
        JSON.dump_file(dialogs, "QA.json")
        return True


