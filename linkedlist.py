class linkedlist:
    def __init__(self, value):
        self.value = value
        self.next = None
    def set(self, index, value):
        if index == 0:
            self.value = value
        else:
            self.next.set(index - 1, value)
    def get(self, index):
        if index == 0:
            return self.value
        return self.next.get(index - 1)
    def to_string(self):
        if self.next == None:
            return self.value
        return self.value + ' ' + self.next.to_string()
    def add(self, value):
        if self.next == None:
            self.next = linkedlist(value)
        else:
            self.next.add(value)