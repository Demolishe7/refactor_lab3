def num_map(value, old_max, old_min, new_max, new_min):
    return (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
