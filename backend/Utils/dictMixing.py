

#Key are strings, values are ints. If the key is in both dicts, value gets added, else, gets pushed.
def sym_diff_and_adding_intersection(dict_a, dict_b):
    if dict_a and len(dict_a) > 0 and (not dict_b or len(dict_b) is 0):
        return dict_a
    elif dict_b and len(dict_b) > 0 and (not dict_a or len(dict_a) is 0):
        return dict_b
    else:
        dict_final = dict()
        keys = set(dict_a.keys()).union(set(dict_b.keys()))
        for key in keys:
            dict_final[key] = dict_a.get(key, 0) + dict_b.get(key, 0)
        return dict_final

#Key are strings, values are ints. Returns highest int value among the keys.
def get_highest_value_key(candidate_dict):
    final_candidate = None
    final_candidate_value = 0
    for key, value in candidate_dict.iteritems():
        if value > final_candidate_value:
            final_candidate = key
            final_candidate_value = value
    return final_candidate
