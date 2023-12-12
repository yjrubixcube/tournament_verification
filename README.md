- `utils.py`
    - some funtions and classes used for simulation
- `main.py`
    - The first version of implementation
    - Uses set to maintain states to merge states
    - Does not include other acceleration approaches
- `simulation_second.py`
    - Second version of implementation
    - Uses set and class with `__hash__` to implement merge states
    - Removes states from TODO set if the ranking order will not change, use 勝差

TODO

- Improve ranking detection `utils.Round_info.get_win_diff_matrix`