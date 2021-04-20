import pandas as pd

import mininet_utils

df = pd.read_csv("sample_test.csv")

# Train and record split ratio for each combination
results, total_cnt, current_cnt = [], len(df), 0
for idx, row in df.iterrows():
    mininet_utils.run_exp_for_combination(row['path_1_bw'], row['delay_1'], row['loss_1'],
                                          row['path_2_bw'], row['delay_2'], row['loss_2'])
    current_cnt += 1
    print("Progress: {}/{}; {}% <==> {}/{} ".format(current_cnt, total_cnt, current_cnt * 100 / total_cnt, idx,
                                                    len(df)))
