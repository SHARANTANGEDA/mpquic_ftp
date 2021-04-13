import argparse

import pandas as pd

import mininet_utils
import utils

parser = argparse.ArgumentParser(description='Run Experiments Based on Machine ID')
parser.add_argument('--m_id', type=int, dest="m_id", help="Machine Id", default=0)
args = parser.parse_args()

dataset_split = args.m_id

df = None
if dataset_split == 1:
    df = pd.read_csv("part_1.csv")
elif dataset_split == 2:
    df = pd.read_csv("part_2.csv")
elif dataset_split == 3:
    df = pd.read_csv("part_3.csv")
elif dataset_split == 4:
    df = pd.read_csv("part_4.csv")
else:
    df = pd.read_csv("combinations.csv")

path_1, path_2, max_cnt, split_ratios_list, runs_per_combination = utils.load_config()

# Train and record split ratio for each combination
results, total_cnt, current_cnt = [], len(split_ratios_list) * len(df), 0
for idx, row in df.iterrows():
    for split_ratio in split_ratios_list:
        mininet_utils.run_exp_for_combination(row['path_1_bw'], row['path_1_delay'], row['path_1_loss'],
                                              row['path_2_bw'], row['path_2_delay'], row['path_2_loss'], split_ratio,
                                              runs_per_combination)
        current_cnt += 1
        print("Progress: {}/{}; {}% <==> {}/{}".format(current_cnt, total_cnt, current_cnt * 100 / total_cnt,
                                                       idx, len(df)))
