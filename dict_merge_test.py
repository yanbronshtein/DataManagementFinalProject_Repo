def merge_dicts(dict1, dict2):
    new_dict = {**dict1, **dict2}
    return new_dict

dict1 = {'user_id': 1, 'other_field':567}
dict2 = {'user_id': 1, 'mama_field':578}

merged_dict = merge_dicts(dict1, dict2)
print(merged_dict)