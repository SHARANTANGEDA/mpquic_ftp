import argparse
from datetime import datetime

import pandas as pd

import mininet_utils
import utils

parser = argparse.ArgumentParser(description='Run Experiments Based on Machine ID')
parser.add_argument('--m_id', type=str, dest="m_id", help="Machine Id", default="0")
args = parser.parse_args()

dataset_split = args.m_id
start_time = datetime.now()
df = None
if not dataset_split == "0":
    df = pd.read_csv("part_"+dataset_split+".csv")
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
        print("Progress: {}/{}; {}% <==> {}/{} || Time Since Start: {} sec".format(current_cnt, total_cnt,
                                                                                   current_cnt * 100 / total_cnt,
                                                                                   idx, len(df), (
                                                                                               datetime.now() - start_time).total_seconds()))
