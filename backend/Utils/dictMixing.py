

#Key are strings, values are ints. If the key is in both dicts, value gets added, else, gets pushed.
def sym_diff_and_adding_intersec(dict_a, dict_b):
    if dict_a and len(dict_a) > 0:
        for key, value in dict_a.iteritems():
            if key in dict_b:
                value += dict_b[key]
            else:
                dict_a[key] = dict_b[key]
        return dict_a
    else:
        return dict_b


#Key are strings, values are ints. Returns highest int value among the keys.
def get_highest_value_key(candidate_dict):
    final_candidate = None
    final_candidate_value = 0
    for key, value in candidate_dict.iteritems():
        if value > final_candidate_value:
            final_candidate = key
            final_candidate_value = value
    return final_candidate
