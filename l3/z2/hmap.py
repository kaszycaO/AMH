from math import floor

class hmap(object):
    def __init__(self, m):
        self.m = m
        self.data = [[] for _ in range(m)]

    def hash(self, element):
        helper = 0
        for el in element:
            helper += ord(el)
        return floor(self.m*((helper*0.75)%1))

    def insert(self, key):
        index = self.hash(key)
        self.data[index].append(key)

    def find(self, key):
        index = self.hash(key)
        if key in self.data[index]:
            return True
        else:
            return False

    def load(self, filename):
        counter = 0
        with open(filename, 'r') as f:
            content = f.read()
            content = content.split()
            for word in content:
                self.insert(word.lower())
