import random


def generate_new_password():
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    return new_password
