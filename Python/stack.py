class Stack(object):
    def __init__(self):
        self.my_list = []

    def push(self, value):
        self.my_list.append(value)

    def pop(self):
        last_value = self.my_list[-1]
        self.my_list = self.my_list[:-1]
        return last_value
