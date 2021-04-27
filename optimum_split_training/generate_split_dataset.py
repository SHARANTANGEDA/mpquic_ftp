import random

import numpy as np

import utils

path_1, path_2, max_cnt, split_ratios_list, runs_per_combination = utils.load_config()
combinations = utils.generate_all_combinations(path_1['bandwidth_list'], path_1["delay_list"], path_1["loss_list"],
                                               path_2['bandwidth_list'], path_2["delay_list"], path_2["loss_list"])


# Limit Combinations with max_cnt
random.shuffle(combinations)
stripped_list = combinations[:max_cnt]
print("shuffled")
df = utils.save_combinations_as_df(stripped_list)
print("Combined Dataset")

df1, df2, df3, df4 = np.array_split(df, 4)

print("Part-1")
df1.to_csv("part_1.csv", index=False)
print("Part-2")
df2.to_csv("part_2.csv", index=False)
print("Part-3")
df3.to_csv("part_3.csv", index=False)
print("Part-4")
df4.to_csv("part_4.csv", index=False)
