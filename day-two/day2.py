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



def part1():
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

#part1()


class GameResult(IntEnum):
    WIN = 1
    LOSS = 2
    DRAW = 3

game_result_code_to_enum = {
    "X" : GameResult.LOSS,
    "Y" : GameResult.DRAW,
    "Z" : GameResult.WIN,
}


wins = { losses[k]:k for k in losses } # I'm lazy, what can I say

def part2():
    total_score = 0
    for line in input:
        theirs, result = line.split()
        their_move = opponent_move_code_to_types[theirs]
        game_result = game_result_code_to_enum[result]
        if game_result == GameResult.DRAW:
            total_score += 3
            total_score += scores[their_move]
        elif game_result == GameResult.WIN:
            total_score += 6
            my_move = losses[their_move]
            total_score += scores[my_move]
        elif game_result == GameResult.LOSS:
            my_move = wins[their_move]
            total_score += scores[my_move]

    print(total_score)

part2()