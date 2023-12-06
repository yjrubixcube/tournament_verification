# 總冠軍(同) > 總冠軍(異) > 季後(異,勝) > 季後(同) > 季後(異,敗) > 其他

from itertools import combinations
import time
from tqdm import tqdm, trange

# progress = tqdm(total=1000000000)

TEAMS = 4
TOURAMENT = list(combinations(range(TEAMS), 2))
TOURAMENT = TOURAMENT*2
GAMES = len(TOURAMENT)

def get_winrate(state):
    if state[0][1] != GAMES:
        raise NotImplementedError
    
    # winrate = []
    total_winrate = []
    first_winrate = []
    second_winrate = []

    for team_stats in zip(state[1][0], state[1][1]):
        # team stats = ((first win, first loss), (second win, second loss))

        # total winrate
        if sum(team_stats[0]) + sum(team_stats[1]) == 0:
            total_winrate.append(0.0)
        else:
            total_winrate.append((team_stats[0][0] + team_stats[1][0])/(sum(team_stats[0]) + sum(team_stats[1])))

        # first
        if sum(team_stats[0]) == 0:
            first_winrate.append(0.0)
        else:
            first_winrate.append(team_stats[0][0]/sum(team_stats[0]))
        # second
        if sum(team_stats[1]) == 0:
            second_winrate.append(0.0)
        else:
            second_winrate.append(team_stats[1][0]/sum(team_stats[1]))


    return list(zip(total_winrate, first_winrate, second_winrate))

def rank_outcome(state, player: int):
    winrate = get_winrate(state)
    # winrate = ((total, first, second), ...)
    # 總冠軍(同) > 總冠軍(異) > 季後(異,勝) > 季後(同) > 季後(異,敗) > 其他
    player_winrate = list(enumerate(winrate))
    # player_winrate = ((index, (total, first, second)), ...)
    total_winner = sorted(player_winrate, key=lambda x: x[1][0], reverse=True)
    first_winner = sorted(player_winrate, key=lambda x: x[1][1], reverse=True)
    second_winner = sorted(player_winrate, key=lambda x: x[1][2], reverse=True)


    ''''''
    # win: [(No. teams, (team index, (total ,first, second))), ...]

    class Top3:
        def __init__(self, winners) -> None:
            # ((total, first, second), ...)
            # print(winners, type(winners), flush=True)
            self.rank1 = []
            self.rank2 = []
            self.rank3 = []

            self.top_teams = [[], [], []]
            cur = 1
            for w in winners:
                # print(f"{self.rank1=}, {self.rank2=}, {self.rank3=}, {w=}")
                if cur == 1:
                    if len(self.rank1) == 0 or self.rank1[-1][1][0] == w[1][0]:
                        self.rank1.append(w)
                        self.top_teams[0].append(w[0])
                    else:
                        cur += 1
                elif cur == 2:
                    if len(self.rank2) == 0 or self.rank2[-1][1][0] == w[1][0]:
                        self.rank2.append(w)
                        self.top_teams[1].append(w[0])
                    else:
                        cur += 1
                elif cur == 3:
                    if len(self.rank3) == 0 or self.rank3[-1][1][0] == w[1][0]:
                        self.rank3.append(w)
                        self.top_teams[2].append(w[0])
                    else:
                        break   
          

        def overlap(self, self_rank, other, other_rank):
            rtn = False
            for f in self.top_teams[self_rank]:
                if f in other.top_teams[other_rank]:
                    rtn = True
                    break
            
            return rtn
        
        def in_rank(self, player, rank):
            return player in self.top_teams[rank]



    total = Top3(total_winner)
    first = Top3(first_winner)
    second = Top3(second_winner)

    first_eq_second = Top3.overlap(first, 0, second, 0)

    if first_eq_second:
        # 同
        if total.in_rank(player, 0):
            # 總冠軍(同)
            return 6
        elif total.in_rank(player, 1) or total.in_rank(player, 2):
            # 季後(同)
            # return 3
            return 4
        else:
            # 其他
            return 1
    elif not first_eq_second:
        # (異)
        other_high_player = 0

        # if total_winner[0][0] != first_winner[0][0] and total_winner[0][0] != second_winner[0][0]:
        if not Top3.overlap(total, 0, first, 0) and not Top3.overlap(total, 0, second, 0):
            other_high_player = total_winner[0]
            other_high_player = total.top_teams[0]
        # elif total_winner[1][0] != first_winner[0][0] and total_winner[1][0] != second_winner[0][0]:
        elif not Top3.overlap(total, 1, first, 0) and not Top3.overlap(total, 1, second, 0):
            other_high_player = total_winner[1]
            other_high_player = total.top_teams[1]
        # elif total_winner[2][0] != first_winner[0][0] and total_winner[2][0] != second_winner[0][0]:
        elif not Top3.overlap(total, 2, first, 0) and not Top3.overlap(total, 2, second, 0):
            other_high_player = total_winner[2]
            other_high_player = total.top_teams[2]

        # if first_winner[0][1][0] > second_winner[0][1][0]:
            # 第一季冠軍的全季勝率 vs 第二季冠軍的全季勝率
        if max(first.rank1, key=lambda x:x[0]) > max(second.rank1, key=lambda x:x[0]):
            # higher_player = first_winner[0]
            # lower_player = second_winner[0]
            higher_player = first.top_teams[0]
            lower_player = second.top_teams[0]
        else:
            # higher_player = second_winner[0]
            # lower_player = first_winner[0]
            higher_player = second.top_teams[0]
            lower_player = first.top_teams[0]

        # if higher_player[0] == player:
        if player in higher_player:
            # 總冠軍(異)
            # return 5
            return 6
        # elif player == lower_player[0]:
        elif player in lower_player:
            # 季後(異,勝)
            return 4
        # elif player == other_high_player[0]:
        elif player in other_high_player:
            # 季後(異,敗)
            # return 2
            return 4
        else:
            # 其他
            return 1

def simulate(states: set, half):
    # half = 0 or 1
    end_states = set()

    while states:
        cur_state = states.pop()

        cur_game_index = cur_state[0][half]
        # print(cur_game_index, half)
        cur_game = TOURAMENT[cur_game_index]

        cur_scores = list(cur_state[1][half])

        # win
        win_scores = cur_scores[:]
        win_scores[cur_game[0]] = (cur_scores[cur_game[0]][0]+1, cur_scores[cur_game[0]][1])
        win_scores[cur_game[1]] = (cur_scores[cur_game[1]][0], cur_scores[cur_game[1]][1]+1)
        if half == 0:
            win_state = ((cur_game_index+1, 0), (tuple(win_scores), tuple((0, 0) for _ in range(TEAMS))))
        else:
            win_state = ((cur_state[0][0], cur_game_index+1), (cur_state[1][0], tuple(win_scores)))

        # tie
        # tie_scores = cur_scores[:]
        # # tie_state = (cur_game_index+1, tuple(tie_scores))
        # if half == 0:
        #     tie_state = ((cur_game_index+1, 0), (tuple(tie_scores), tuple((0, 0) for _ in range(TEAMS))))
        # else:
        #     tie_state = ((cur_state[0][0], cur_game_index+1), (cur_state[1][0], tuple(tie_scores)))

        # loss
        loss_scores = cur_scores[:]
        loss_scores[cur_game[0]] = (cur_scores[cur_game[0]][0], cur_scores[cur_game[0]][1]+1)
        loss_scores[cur_game[1]] = (cur_scores[cur_game[1]][0]+1, cur_scores[cur_game[1]][1])
        # loss_state = (cur_game_index+1, tuple(loss_scores))
        if half == 0:
            loss_state = ((cur_game_index+1, 0), (tuple(loss_scores), tuple((0, 0) for _ in range(TEAMS))))
        else:
            loss_state = ((cur_state[0][0], cur_game_index+1), (cur_state[1][0], tuple(loss_scores)))

        if cur_game_index == GAMES - 2 and half == 1:
            # last game
            end_states.add(win_state)
            # end_states.add(tie_state)
            end_states.add(loss_state)
        elif cur_game_index == GAMES - 1 and half == 0:
            end_states.add(win_state)
            # end_states.add(tie_state)
            end_states.add(loss_state)
        else:
            states.add(win_state)
            # states.add(tie_state)
            states.add(loss_state)
        # progress.update(1)
        
    return end_states

# ((half games played, half games played), ((win, loss)*n, .))
states = set()
last_states = set()
end_states = set()

first_state = ((0, 0), (tuple((0, 0) for _ in range(TEAMS)), tuple((0, 0) for _ in range(TEAMS))))

states.add(first_state)
print(TOURAMENT)
t1 = time.time()
first_half_states = simulate(states, 0)
t2 = time.time()
print(t2 - t1)
print(len(first_half_states))
# exit(0)
second_half_states = simulate(first_half_states, 1)
print(len(second_half_states))
count = 0
for s in tqdm(second_half_states):
# for s in second_half_states:
    cur_game_index = s[0][1]
    cur_game = TOURAMENT[cur_game_index]

    cur_scores = list(s[1][1])

    # win
    win_scores = cur_scores[:]
    win_scores[cur_game[0]] = (cur_scores[cur_game[0]][0]+1, cur_scores[cur_game[0]][1])
    win_scores[cur_game[1]] = (cur_scores[cur_game[1]][0], cur_scores[cur_game[1]][1]+1)
    # win_state = (cur_game_index+1, tuple(win_scores))
    win_state = ((s[0][0], cur_game_index+1), (s[1][0], tuple(win_scores)))
    # tie

    # tie_scores = cur_scores[:]
    # # tie_state = (cur_game_index+1, tuple(tie_scores))
    # tie_state = ((s[0][0], cur_game_index+1), (s[1][0], tuple(tie_scores)))


    # loss
    loss_scores = cur_scores[:]
    loss_scores[cur_game[0]] = (cur_scores[cur_game[0]][0], cur_scores[cur_game[0]][1]+1)
    loss_scores[cur_game[1]] = (cur_scores[cur_game[1]][0]+1, cur_scores[cur_game[1]][1])
    # loss_state = (cur_game_index+1, tuple(loss_scores))
    loss_state = ((s[0][0], cur_game_index+1), (s[1][0], tuple(loss_scores)))


    # cur player = TOURAMENT[-1][0]
    cur_player = TOURAMENT[-1][0]

    win_outcome = rank_outcome(win_state, cur_player)
    # tie_outcome = rank_outcome(tie_state, cur_player)
    loss_outcome = rank_outcome(loss_state, cur_player)

    if win_outcome < loss_outcome:
        # print("win", win_outcome, win_state)
        # print("los", loss_outcome, loss_state)
        # print("===============================")
        # pass
        count += 1
    # elif win_outcome < tie_outcome:
    #     print("win", win_outcome, win_state)
    #     print("tie", tie_outcome, tie_state)
    #     print("===============================")
    # if tie_outcome < loss_outcome:
    #     print("tie", tie_outcome, tie_state)
    #     print("los", loss_outcome, loss_state)
    #     print("===============================")

t3 = time.time()
print(t3-t2, count)