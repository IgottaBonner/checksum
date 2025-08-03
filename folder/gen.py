import random


def make1():
    r = random.randint(1, 9)
    while len(str(r)) < 32:
        r *= random.randint(1, 9)
    return r


def make2():
    r2 = random.randint(1, 9)
    while len(str(r2)) < 4:
        r2 *= random.randint(1, 9)
    return r2


c = 1
for b in range(1, 5):
    with open(f"{b}.txt", "w") as f:
        for i in range(c, c + 20):
            f.write(
                f"+--+--------------------------------+-------+--------------------------------+-------+--------------------------------+-------+\n|{i}|{make1()}|___{make2()}|{make1()}|___{make2()}|{make1()}|___{make2()}|\n"
            )
        c += 20
