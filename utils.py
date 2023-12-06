from const import *
from copy import deepcopy
import random
from itertools import combinations
import numpy as np

def generate_tournament(m_teams: int, n_games: int, shuffle=False, seed=0) -> list[list[int]]:
    teams = list(combinations(range(m_teams), 2))
    teams *= n_games
    random.seed(seed)
    if shuffle:
        random.shuffle(teams)
    tournament = []
    # generate first half (already played)
    for away, home in teams:
        uniform = random.uniform(0, 1)
        if uniform > 1:
            draw = 1
            winner = loser = -1
        else:
            draw = 0
            winner = random.choice([away, home])
            loser = away if winner == home else home
        tournament.append([away, home, 1, winner, loser, draw])
    
    # for away, home in teams:
    #     tournament.append([away, home, 0, -1, -1, 0])
    # generate second half (not played)
    if shuffle:
        random.shuffle(teams)
    for away, home in teams:
        tournament.append([away, home, 0, -1, -1, 0])

    return tournament

class Round_info:
    def __init__(self, game_index, tournament: list[list[int]], prev_info=None, teams=TEAMS) -> None:
        if prev_info:
            assert prev_info.game_index + 1 == game_index
            self.game_index = game_index
            self.team_games_left = prev_info.team_games_left.copy()
            remove_game = tournament[game_index-1]
            self.team_games_left[remove_game[0]] -= 1
            self.team_games_left[remove_game[1]] -= 1
            assert self.team_games_left[remove_game[0]] >= 0
            assert self.team_games_left[remove_game[1]] >= 0
        else:
            self.team_games_left = [0 for _ in range(teams)]
            self.game_index = game_index
            for index in range(game_index, len(tournament)):
                round = tuple(tournament[index])

                self.team_games_left[round[0]] += 1
                self.team_games_left[round[1]] += 1

    def __str__(self) -> str:
        ret_str = ""
        ret_str += f"{self.game_index}"
        ret_str += f"{self.team_games_left}"

        return ret_str

class State:
    '''
    scores: [[0 team wins first, 0 team loss first, 0 team wins second, 0 team loss second] * n]
    '''
    def __init__(self, other=None, tournament=None):
        '''
        scores: [[0 team wins first, 0 team loss first, 0 team wins second, 0 team loss second] * n]
        '''
        if tournament:
            # initialize state based on a existing tourament result
            # self = State()
            self.first_half_played = 0
            self.second_half_played = 0
            self.team_scores = []
            for _ in range(TEAMS):
                self.team_scores.append([0, 0, 0, 0])

            for round_index in range(len(tournament)):
                round = tournament[round_index]
                # round = (Away, Home, f: played? 0, 1, w: (A, H, -1), l: (A, H, -1), d: draw? 0, 1)
                if round[2] == 1:
                    # played
                    if round_index < GAMES:
                        # first half
                        self.first_half_played += 1
                        if round[5] == 0:
                            # not draw
                            self.team_scores[round[3]][0] += 1
                            self.team_scores[round[4]][1] += 1
                        else:
                            # draw
                            pass
                    else:
                        # second half
                        self.second_half_played += 1
                        if round[5] == 0:
                            # not draw
                            self.team_scores[round[3]][2] += 1
                            self.team_scores[round[4]][3] += 1
                        else:
                            # draw
                            pass
                else:
                    # not played yet
                    break
            
        elif other:
            # inherit from another state
            self.first_half_played = other.first_half_played
            self.second_half_played = other.second_half_played
            # scores: [[0 team wins first, 0 team loss first, 0 team wins second, 0 team loss second] * n]
            self.team_scores = deepcopy(other.team_scores)
            
        else:
            # make new state
            self.first_half_played = 0
            self.second_half_played = 0
            self.team_scores = []
            for _ in range(TEAMS):
                self.team_scores.append([0, 0, 0, 0])

    def __eq__(self, other) -> bool:
        first_half_eq = self.first_half_played == other.first_half_played
        second_half_eq = self.second_half_played == other.second_half_played
        scores_eq = self.team_scores == other.team_scores

        return first_half_eq and second_half_eq and scores_eq
    
    def __hash__(self) -> int:
        first_half = self.first_half_played
        second_half = self.second_half_played
        scores = self.team_scores

        hash_str = f"1{first_half}{second_half}"
        for team_score in scores:
            hash_str += f"{team_score[0]}{team_score[1]}{team_score[2]}{team_score[3]}"

        return int(hash_str)
    
    def __str__(self) -> str:
        first_half = self.first_half_played
        second_half = self.second_half_played
        scores = self.team_scores

        hash_str = f"{first_half}{second_half}"

        ret_str = f"State\t{first_half}\t{second_half}\n"
        for team_score in scores:
            hash_str += f"{team_score[0]}{team_score[1]}{team_score[2]}{team_score[3]}"
            ret_str += f"{team_score[0]} {team_score[1]} {team_score[2]} {team_score[3]}\n"


        # return hash_str
        return ret_str

    def get_winrate(self, half=None) -> list[list[float]]:
        """
        Takes a state and returns a list of all teams' winrate for a half or all seasons
        
        half = 1, 2, X
        """
        winrates = []
        if half == 1:
            # first half winrate
            for team_score in self.team_scores:
                wins = team_score[0]
                loss = team_score[1]
                if wins + loss == 0:
                    winrates.append(0)
                else:
                    winrates.append((wins)/(wins+loss))

        elif half == 2:
            # second half winrate
            for team_score in self.team_scores:
                wins = team_score[2]
                loss = team_score[3]
                if wins + loss == 0:
                    winrates.append(0)
                else:
                    winrates.append((wins)/(wins+loss))
        else:
            # overall winrate
            for team_score in self.team_scores:
                wins = team_score[0] + team_score[2]
                loss = team_score[1] + team_score[3]
                if wins + loss == 0:
                    winrates.append(0)
                else:
                    winrates.append((wins)/(wins+loss))

        return winrates
    
    def get_win_diff_matrix(self, half=None) -> list[list[float]]:
        '''
        return the matrix of win difference for a half, leave None for full season.
        half = 1, 2, X
        M[i][j] = (i_win - j_win) + (j_loss - i_loss) / 2
        M[i][i] = 0
        '''
        matrix = [[0 for _ in range(TEAMS)] for _ in range(TEAMS)]

        
        if half == 1:
            # first half win diff
            for i in range(TEAMS):
                for j in range(TEAMS):
                    if i == j:
                        matrix[i][j] = INFINITY
                        continue
                    i_win, i_loss = self.team_scores[i][0:2]
                    j_win, j_loss = self.team_scores[j][0:2]
                    matrix[i][j] = (i_win - j_win + j_loss - i_loss) / 2 

        elif half == 2:
            # second half win diff
            for i in range(TEAMS):
                for j in range(TEAMS):
                    if i == j:
                        matrix[i][j] = INFINITY
                        continue
                    i_win, i_loss = self.team_scores[i][2:4]
                    j_win, j_loss = self.team_scores[j][2:4]
                    matrix[i][j] = (i_win - j_win + j_loss - i_loss) / 2 
        else:
            # overall win diff
            for i in range(TEAMS):
                for j in range(TEAMS):
                    if i == j:
                        matrix[i][j] = INFINITY
                        continue
                    i_win, i_loss = self.team_scores[i][0]+self.team_scores[i][2], self.team_scores[i][1]+self.team_scores[i][3]
                    j_win, j_loss = self.team_scores[j][0]+self.team_scores[j][2], self.team_scores[j][1]+self.team_scores[j][3]
                    matrix[i][j] = (i_win - j_win + j_loss - i_loss) / 2 

        return matrix

    def end_simulation_early(self, half=None, output=False) -> bool:
        '''
        half = 1, 2, X
        End simulation if:
        0. In the rest of the tournament, every 2 teams AB has win diff > (games A have + games B have)/2
        1. In the rest of the tournament, every 2 teams that plays against each other have win difference > rounds that they are together
        2. In the rest of the tournament, every team that playes have win difference > rounds that they have games
        '''
        win_diff_second = self.get_win_diff_matrix(2)
        win_diff_total = self.get_win_diff_matrix()
        # assume only second half
        assert half != 1
        if self.first_half_played < GAMES:
            # first half not done, should not be accessed
            print("You screwed up lol")
            return False
        elif self.first_half_played == GAMES:
            # first half done

            if self.second_half_played < GAMES:
                # second half not done, should all be here
                current_game_index = self.first_half_played + self.second_half_played
                # score_index = 2
                for i in range(TEAMS):
                    for j in range(i+1, TEAMS):
                        if output:
                            print(i, j, (round_infos[current_game_index].team_games_left[i]+round_infos[current_game_index].team_games_left[j])/2, win_diff_second[i][j])
                            # exit()
                        if abs(win_diff_second[i][j]) <= (round_infos[current_game_index].team_games_left[i]+round_infos[current_game_index].team_games_left[j])/2:
                            return False
                        if abs(win_diff_total[i][j]) <= (round_infos[current_game_index].team_games_left[i]+round_infos[current_game_index].team_games_left[j])/2:
                            return False
                        
                return True
                        
            else:
                # second half done, should not be accessed
                print("U R too late")
                return False
        
    def enter_playoff(self, player: int) -> bool:
        '''
        Takes a state and a player, return if the player can enter playoffs(be in top teams) or not
        If there are ties, all possible combinations will be counted, if player is in any of them, return yes
        '''
        
        first_winrate = self.get_winrate(1)
        second_winrate = self.get_winrate(2)
        total_winrate = self.get_winrate()

        # [(team_id, wr)]
        first_ordered = sorted(enumerate(first_winrate), key=lambda x:x[1], reverse=True)
        second_ordered = sorted(enumerate(second_winrate), key=lambda x:x[1], reverse=True)
        total_ordered = sorted(enumerate(total_winrate), key=lambda x:x[1], reverse=True)

        def to_rank(order: list):
            cur_wr = order[0][1]

            output = [[]]
            for team, wr in order:
                if wr == cur_wr:
                    output[-1].append(team)
                else:
                    output.append([team])
                    cur_wr = wr
            return output
        
        # [[no1, no1], [no2]..]
        first_ranked = to_rank(first_ordered)
        second_ranked = to_rank(second_ordered)
        total_ranked = to_rank(total_ordered)
        # champs = set()
        for first_winner in first_ranked[0]:
            for second_winner in second_ranked[0]:
                if player == first_winner or player == second_winner:
                    return True
                if first_winner == second_winner:
                    # first & second half winners are the same
                    count = 1
                    for next_winners in total_ranked:
                        if count >= 3:
                            break
                        for next_winner in next_winners:
                            if next_winner != first_winner:
                                count += 1
                                if next_winner == player:
                                    return True

                    pass
                else:
                    # first & second half winners are different
                    count = 2
                    for next_winners in total_ranked:
                        if count >= 3:
                            break
                        for next_winner in next_winners:
                            if next_winner != first_winner and next_winner != second_winner:
                                count += 1
                                if next_winner == player:
                                    return True
        return False

global round_infos
round_infos = []
def simulate(tournament, end_early_check):
    '''
    Simulate a game tree based on a state and TOURNAMENT
    '''
    # print(TEAMS, GAMES)
    # assert len(tournament) == 2*GAMES

    # initialize a state based on tournament
    states = set()
    states.add(State(tournament=tournament))
    
    # global round_infos
    # round_infos = []
    round_infos.clear()
    for i in range(len(tournament)):
        try:
            prev_info = round_infos[-1]
        except IndexError:
            prev_info = None
        round_infos.append(Round_info(i, tournament, prev_info))

    # a set to store end states that have lose2win
    end_states = set()
    early_states = set()

    while states:
        # loop until the set is empty
        current_state = states.pop()

        final = False
        if current_state.first_half_played < GAMES:
            # first half not done
            current_game_index = current_state.first_half_played
            score_index = 0
            current_state.first_half_played += 1
            pass
        elif current_state.first_half_played == GAMES:
            # first half done
            
            if current_state.second_half_played < GAMES:
                # second half not done
                current_game_index = current_state.first_half_played + current_state.second_half_played
                score_index = 2
                # if current_state.end_simulation_early():
                #     pass
                current_state.second_half_played += 1
                if current_game_index == 2*GAMES -1:
                    final = True
                
            else:
                # second half done
                print("Why are you even here?")
                return
            
        round = tournament[current_game_index]
        # home win
        home_state = State(current_state)
        home_state.team_scores[round[0]][score_index] += 1
        home_state.team_scores[round[1]][score_index+1] += 1
                                         
        # away win
        away_state = State(current_state)
        away_state.team_scores[round[1]][score_index] += 1
        away_state.team_scores[round[0]][score_index+1] += 1

        # draw
        draw_state = State(current_state)
        if final:
            # if any of the last players have lose2win
            p_home = round[1]
            p_away = round[0]
            # print(current_state)
            # print(home_state)
            # print(away_state)
            # exit()
            if (not home_state.enter_playoff(p_home) and away_state.enter_playoff(p_home)) or \
                (not away_state.enter_playoff(p_away) and home_state.enter_playoff(p_away)):
                # current_state.second_half_played -= 1
                end_states.add(current_state)
        else:
            if end_early_check:
                if not home_state.end_simulation_early():
                    states.add(home_state)
                else:
                    early_states.add(home_state)
                if not away_state.end_simulation_early():
                    states.add(away_state)
                else:
                    early_states.add(away_state)
                if not draw_state.end_simulation_early():
                    states.add(draw_state)
                else:
                    early_states.add(draw_state)
            else:
                states.add(home_state)
                states.add(away_state)
                states.add(draw_state)
    # print(end_states)
    return end_states, early_states