with open("input.txt", "r") as f:
    input = f.read()

elves = []

s = input
while s:
    part, token, rest = s.partition("\n\n")
    elves.append([int(x) for x in part.split()])
    s = rest

total_calories = sorted([sum(x) for x in elves])

# solution 1
print(total_calories[len(total_calories) - 1])

# solution 2
print(sum(total_calories[-3:]))