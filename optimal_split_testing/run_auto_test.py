import argparse

import pandas as pd

import mininet_utils

parser = argparse.ArgumentParser(description='Run Automated Testing')
parser.add_argument('--scheduler', type=str, dest="scheduler", help="Scheduler Name", default="optimum_split")
parser.add_argument('--split_ratio', type=str, dest="split_ratio", help="Split Ratio", default="1.0")
args = parser.parse_args()

df = pd.read_csv("t1_sample.csv")

# Train and record split ratio for each combination
results, total_cnt, current_cnt = [], len(df), 0
for idx, row in df.iterrows():
    mininet_utils.run_exp_for_combination(row['path_1_bw'], row['delay_1'], row['loss_1'], row['path_2_bw'],
                                          row['delay_2'], row['loss_2'], args.scheduler, args.split_ratio)
    current_cnt += 1
    print("Progress: {}/{}; {}% <==> {}/{} ".format(current_cnt, total_cnt, current_cnt * 100 / total_cnt, idx,
                                                    len(df)))
