# 直接列舉最後一場的可能

from itertools import combinations
from tqdm import tqdm

TEAMS = 5
TOURAMENT = list(combinations(range(TEAMS), 2))
GAMES = len(TOURAMENT)

