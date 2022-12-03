from enum import IntEnum

with open("input.txt") as f:
    input = f.readlines()

class MoveType(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

opponent_move_code_to_types = {
    "A" : MoveType.ROCK,
    "B" : MoveType.PAPER,
    "C" : MoveType.SCISSORS,
}

player_move_code_to_types = {
    "X" : MoveType.ROCK,
    "Y" : MoveType.PAPER,
    "Z" : MoveType.SCISSORS,
}

scores = {
    MoveType.ROCK : 1,
    MoveType.PAPER : 2,
    MoveType.SCISSORS : 3
}

# my kingdom for a switch statement ... I don't know why I've decided to stick with Python, but here goes
losses = {
    MoveType.ROCK : MoveType.PAPER,
    MoveType.PAPER : MoveType.SCISSORS,
    MoveType.SCISSORS : MoveType.ROCK,
}


def solution1():
    total_score = 0
    for line in input:
        theirs, mine = line.split()
        their_move = opponent_move_code_to_types[theirs]
        my_move = player_move_code_to_types[mine]

        score = scores[my_move]
        if losses[their_move] == my_move:
            score += 6
        elif losses[my_move] != their_move:
            score += 3
        total_score += score

    print(total_score)

solution1()