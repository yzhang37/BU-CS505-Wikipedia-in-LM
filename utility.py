import ujson as json


def load_json(path):
    with open(path, 'r') as fin:
        return json.load(fin)


def save_json(data, path):
    with open(path, 'w') as fout:
        json.dump(data, fout, ensure_ascii=False)
