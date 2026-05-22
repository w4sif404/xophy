class XophyEngine:
    def __init__(self, target):
        self.target = target
        self.results = {}

    def add(self, name, data):
        self.results[name] = data

    def get(self):
        return self.results
