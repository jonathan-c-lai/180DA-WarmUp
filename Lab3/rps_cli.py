import random
import time

# 1 is Rock
# 2 is Paper
# 3 is Scissors
ROCK = '1'
PAPER = '2'
SCISSORS = '3'

def convert(val):
    returnval = ''
    if (val == ROCK):
        returnval = 'Rock'
    elif (val == PAPER):
        returnval = 'Paper'
    elif (val == SCISSORS):
        returnval = 'Scissors'
    return returnval

def rps_result(p1, p2):
    # rp, rs, pr, ps, sr, sp
    # 12, 13, 21, 23, 31, 32
    if (p1 == p2):
        return 'Tie'
    elif ((p1 == ROCK and p2 == PAPER) or (p1 == PAPER and p2 == SCISSORS) or (p1 == SCISSORS and p2 == ROCK)):
        return 'CPU Wins'
    elif ((p1 == ROCK and p2 == SCISSORS) or (p1 == PAPER and p2 == ROCK) or (p1 == SCISSORS and p2 == PAPER)):
        return 'User Wins'
    
score = 0
while (score < 3):
    user_input = input('Choose 1, 2, or 3, for Rock, Paper, or Scissors\n')

    CPU_input = str(random.randint(1,3))

    print('\n')
    print("You picked ", convert(user_input), ' and the CPU picked ', convert(CPU_input))
    print('\n')
    print('Result: ', rps_result(user_input,CPU_input))
    if (rps_result(user_input, CPU_input) == 'User Wins'):
        score += 1

    print('Score: ', score)

    time.sleep(1)
    for i in range(3):
        print('\n')