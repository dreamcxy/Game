import random


class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


def random_a():
    x = 0
    y = random.randint(0, 800)
    return [x, y]


def random_b():
    y = 0
    x = random.randint(0, 600)
    return [x, y]


def random_c():
    x = 600
    y = random.randint(0, 800)
    return [x, y]


def random_d():
    x = random.randint(0, 600)
    y = 800
    return [x, y]


def random_born():
    situation = random.randint(0, 3)
    for case in Switch(situation):
        if case(0):
            return random_a()
            break
        if case(1):
            return random_b()
            break
        if case(2):
            return random_c()
            break
        if case(3):
            return random_d()
            break
        if case():
            return False


init_speed = [1, 1]
born = 3


def add_speed():
    init_speed[0] += 10
    init_speed[1] += 10


def add():
    global born
    born += 3


add()
print born

add_speed()
print init_speed
