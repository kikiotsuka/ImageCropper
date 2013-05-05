class linkedlist:
    def __init__(self, *args):
        if len(args) >= 1:
            self.value = args[0]
            if len(args) > 1:
                self.next = linkedlist(args[1:])
            else:
                self.next = None
        else:
            self.next = None
    def __setitem__(self, index, value):
        if index == 0:
            self.value = value
        else:
            self.next[index - 1] = value
    def __getitem__(self, index):
        if index == 0:
            return self.value
        return self.next[index - 1]
    def __str__(self):
        return '[' + self.tostring() + ']'
    def tostring(self):
        if self.next is None:
            try:
                return str(self.value)
            except:
                return ''
        return str(self.value) + ', ' + self.next.tostring()
    def __repr__(self): return str(self)
    def add(self, value):
        try:
            if self.value == None:
                self.value = value
                return None
        except:
            self.value = value
        if self.next == None:
            self.next = linkedlist(value)
        else:
            self.next.add(value)
