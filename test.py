from utils import *

tournament = generate_tournament(4, 1)
ri = []
# print(ri[-1])
for i in range(len(tournament)):
    try:
        prev_info = ri[-1]
    except IndexError:
        prev_info = None
    ri.append(Round_info(i, tournament, prev_info=prev_info))

# print(ri)
for i in ri:
    print(i.team_games_left)