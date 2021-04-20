import os

import pandas as pd

import utils

_, _, _, _, runs_per_combination = utils.load_config()

results_df = pd.DataFrame(columns=["path_1_bw", "delay_1", "loss_1", "path_2_bw", "delay_2", "loss_2", "split_ratio",
                                   "transfer_time"])
path_1_col, delay_1_col, loss_1_col, path_2_col, delay_2_col, loss_2_col, split_ratios_list,  tr_col = [], [], [], [], \
                                                                                                       [], [], [], []
samples = os.listdir(f'./experiments/')
samples.remove(".gitkeep")
# samples.remove(".DS_Store")
for idx, case in enumerate(samples):
    avg_transfer_time, avail_cnt, excep_cnt = 0, 0, 0
    for i in range(0, runs_per_combination):
        file = open(f'./experiments/{case}/server_{i}.txt', "r")
        content = file.readlines()
        try:
            transfer_time = content[7].split(":")[1].strip().split(" ")[0]
            avg_transfer_time += float(transfer_time)
            avail_cnt += 1
        except:
            if avail_cnt == 0 and excep_cnt > 0:
                print(content, case, i)
            excep_cnt += 1
    avg_transfer_time /= avail_cnt
    details = case.split("_")
    path_1_col.append(details[0])
    delay_1_col.append(details[1][:len(details[1]) - 2] if "ms" in details[1] else details[1])
    loss_1_col.append(details[2])
    path_2_col.append(details[3])
    delay_2_col.append(details[4][:len(details[4]) - 2] if "ms" in details[4] else details[4])
    loss_2_col.append(details[5])
    split_ratios_list.append(details[6])
    tr_col.append(avg_transfer_time)

results_df['path_1_bw'], results_df['delay_1'], results_df['loss_1'], results_df['path_2_bw'], results_df['delay_2'],\
results_df['loss_2'] = path_1_col, delay_1_col, loss_1_col, path_2_col, delay_2_col, loss_2_col
results_df['split_ratio'], results_df['transfer_time'] = split_ratios_list, tr_col
results_df.to_csv("./intermediate_results.csv", index=False)
