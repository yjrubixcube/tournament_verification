'''
Start from second half of the game
'''

from tqdm import tqdm
from const import *
from utils import *
from time import time
# number of teams
# TEAMS = 3
# number of games in a half
# GAMES = 3

def main():
    # initialize a state based on tournament
    # ends = simulate()
    # print(len(ends))
    
    TOURAMENT = generate_tournament(TEAMS, 1, True, random.randint(1, 2000000))

    # print(TOURAMENT)
    # for t in TOURAMENT:
    #     print(t)
    t1 = time()
    ends, early = simulate(TOURAMENT, False)
    t2 = time()
    print(len(ends), len(early), t2-t1)
    t3 = time()
    ends, early = simulate(TOURAMENT, True)
    t4 = time()
    print(len(ends), len(early), t4-t3)

    # no end early: 3617
    # print(ends.pop())
    # print(e:=early.pop())
    # wdm2 = e.get_win_diff_matrix(2)
    # wdm = e.get_win_diff_matrix()
    # print("wdm")
    # for line in wdm:
    #     print(line)

    # print("wd2")
    # for line in wdm2:
    #     print(line)
    # # print(round_infos)
    # for info in round_infos:
    #     print(info)

    # print(e.end_simulation_early(output=True))

if __name__ == "__main__":
    main()