import pandas as pd

import mininet_utils

df = pd.read_csv("sample_test.csv")

# Train and record split ratio for each combination
results, total_cnt, current_cnt = [], len(df), 0
for idx, row in df.iterrows():
    mininet_utils.run_exp_for_combination(row['path_1_bw'], row['path_1_delay'], row['path_1_loss'],
                                          row['path_2_bw'], row['path_2_delay'], row['path_2_loss'])
    current_cnt += 1
    print("Progress: {}/{}; {}% <==> {}/{} ".format(current_cnt, total_cnt, current_cnt * 100 / total_cnt, idx,
                                                    len(df)))
