import random
from itertools import permutations, combinations, combinations_with_replacement

'''
4 teams
3 games each team each half
12 games total
state: {
    played: int
    teams:[
        {
            wins: int
            ties: int
            loss: int
            winrate: float
            diff: float
        }..
    ]
    
}
'''


TEAMS = 3
GAMES = 6
HALF = 2

# TEAMS = 4
# GAMES = 6
# HALF = 2

class Team:
    def __init__(self, prev_team=None) -> None:
        if prev_team == None:
            self.wins = 0
            self.ties = 0
            self.loss = 0
            self.winrate = 0
            self.diff = 0
        else:
            self.wins = prev_team.wins
            self.ties = prev_team.ties
            self.loss = prev_team.loss
            self.winrate = prev_team.winrate
            self.diff = prev_team.diff
    
    def __str__(self) -> str:
        # print(self.wins)
        r = f"Wins: {self.wins}\nTies: {self.ties}\nLoss: {self.loss}\nWinR: {self.winrate}\nDiff: {self.diff}"
        return r
    
    def update_WR(self):
        if self.wins + self.loss == 0:
            return 0
        self.winrate = self.wins / (self.wins + self.loss)

    def win(self):
        self.wins += 1
        self.update_WR()
    
    def tie(self):
        self.ties += 1
        self.update_WR()

    def lose(self):
        self.loss += 1
        self.update_WR()



class State:
    def __init__(self, prev_state=None) -> None:
        if prev_state == None:
            self.game_index = 0
            self.teams = []
            for _ in range(TEAMS):
                d = Team()
                self.teams.append(d)
        else:
            self.game_index = prev_state.game_index
            self.teams = []
            for t in prev_state.teams:
                self.teams.append(Team(t))

    def __str__(self) -> str:
        # print(f'Games played: {self.game_index}')
        r = f'Games played: {self.game_index}\n'
        for i, t in enumerate(self.teams):
            r += f"------\nTeam {i}\n{str(t)}\n"
        return r
    
    def fight(self, a:int, b:int, result: int):
        # result
        # 0: a win
        # 1: tie
        # 2: b win
        if result == 0:
            # a win
            self.teams[a].win()
            self.teams[b].lose()

        elif result == 1:
            # tie
            self.teams[a].tie()
            self.teams[b].tie()
        else:
            # b win
            self.teams[a].lose()
            self.teams[b].win()

    def get_high_winrate(self):
        high = self.teams[0].winrate
        ind = 0
        for i, t in enumerate(self.teams[1:]):
            if t.winrate > high:
                ind = i
                high = t.winrate
        return ind, high

    def get_winner(self):

        pass


state = State()

# print(state)

tournaments = tuple(combinations(range(TEAMS), 2))
total_games = len(tournaments)
print(total_games, tournaments)
# print(tournaments)

states = [state]
# (games played, (win, loss)*n)
end_states = []

while states:
    print("ind state")
    cur_state = states.pop(0)
    
    win_state = State(prev_state=cur_state)
    win_state.fight(*tournaments[win_state.game_index], 0)
    win_state.game_index += 1

    tie_state = State(prev_state=cur_state)
    tie_state.fight(*tournaments[tie_state.game_index], 1)
    tie_state.game_index += 1

    loss_state = State(prev_state=cur_state)
    loss_state.fight(*tournaments[loss_state.game_index], 2)
    loss_state.game_index += 1

    del cur_state

    if win_state.game_index < total_games - 1:
        states.append(win_state)
    else:
        end_states.append(win_state)

    if tie_state.game_index < total_games - 1:
        states.append(tie_state)
    else:
        end_states.append(tie_state)

    if loss_state.game_index < total_games - 1:
        states.append(loss_state)
    else:
        end_states.append(loss_state)

for s in end_states:
    print(s)
    print("===================================")
    # input()

    win_state = State(prev_state=s)
    win_state.fight(*tournaments[win_state.game_index], 0)
    win_state.game_index += 1

    tie_state = State(prev_state=s)
    tie_state.fight(*tournaments[tie_state.game_index], 1)
    tie_state.game_index += 1

    loss_state = State(prev_state=s)
    loss_state.fight(*tournaments[loss_state.game_index], 2)
    loss_state.game_index += 1
    # loss_state.get_winner()

print(len(end_states))