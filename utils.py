import string
import random


def create_random_string():
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(30))