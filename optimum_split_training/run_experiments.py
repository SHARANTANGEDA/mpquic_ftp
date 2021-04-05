import random

import mininet_utils
import utils

path_1, path_2, max_cnt, split_ratios_list = utils.load_config()

combinations = utils.generate_all_combinations(path_1['bandwidth_list'], path_1["delay_list"], path_1["loss_list"],
                                               path_2['bandwidth_list'], path_2["delay_list"], path_2["loss_list"])

df = utils.save_combinations_as_df(combinations)

# Limit Combinations with max_cnt
random.shuffle(combinations)
stripped_list = combinations[:max_cnt]

# Train and record split ratio for each combination
results, total_cnt, current_cnt = [], len(split_ratios_list) * len(stripped_list), 0
for idx, row in enumerate(stripped_list):
    for split_ratio in split_ratios_list:
        mininet_utils.run_exp_for_combination(row[0], row[1], row[2], row[3], row[4], row[5], split_ratio)
        current_cnt += 1
        print("Progress: {}/{}; {}% <==> {}/{}".format(current_cnt, total_cnt, current_cnt * 100 / total_cnt,
                                                       idx, len(stripped_list)))
