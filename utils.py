def num_map(value, old_max, old_min, new_max, new_min):
    old_range = old_max - old_min
    new_range = new_max - new_min
    return (((value - old_min) * new_range) / old_range) + new_min
