
class Stack(object):
    def __init__(self):
        self.my_list = []

    def push(self, value):
        self.my_list.append(value)

    def pop(self):
        last_value = self.my_list[-1]
        self.my_list = self.my_list[:-1]
        return last_value


def main():
    stack1 = Stack()
    stack1.push(50)
    stack1.push(5)
    stack1.push(45)
    stack1.push(80)
    print stack1.pop()
    print stack1.pop()

    stack2 = Stack()
    stack2.push(78)
    stack2.push(4)
    stack2.push(89)
    stack2.push(710)
    stack2.push(100)
    print stack2.pop()
    print stack2.pop()


if __name__ == '__main__':
    main()
