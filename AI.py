import random


def random_move(validmoves):
    return validmoves[random.randint(0, len(validmoves)-1)]